import xml.etree.ElementTree as ET
import re
'''
Extracting Gene Ontology (GO) ID’s and term from each UniProt file using the ElementTree module. . 
'''
xml_files = ['./XMLs/ERBB1.xml', './XMLs/ERBB2.xml', './XMLs/ERBB3.xml', './XMLs/ERBB4.xml']
names = []
results = {}
for xml_file in xml_files:
    result = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()# extracting the root
    namespace = re.match(r"{.*}", root.tag).group()
    root_entry = root.find(namespace+"entry")
    elem = root_entry.findall(namespace+"dbReference")
    for subelem in elem:
        if 'type' not in subelem.attrib:
            continue
        if subelem.attrib['type'] == 'GO':
            for child in subelem:
                if child.attrib['type'] == 'term':
                    result[subelem.attrib['id']] = child.attrib['value']
    name = xml_file.replace("./XMLs/","").replace(".xml","")
    names.append(name)
    results[name] = result
def step3():
    with open("./common_in_4.tsv","w") as fh:# A tab delimited file is created
        fh.write("GO_ID\tGO_term\n") # Headers are written in the table
        for k,v in results[names[0]].items():# Checking if there are GO IDs common in all 4 proteins
            if k in (results[names[1]]) and k in (results[names[2]]) and k in (results[names[3]]):
                fh.write(k + "\t" + v + "\n") # Writing a table (tab delimited) containing GO ID’s and terms in common across all 4 proteins. 

step3()

def step4():
    with open("./common_in_2.tsv","w") as fh: # A tab delimited file is created 
        found = []
        fh.write("Protein\tGO_ID\tGO_term\n")# Headers are written in the table
        for k,v in results.items():
            for k2,v2 in v.items():
                if k2 in found:
                    continue
                cnt = 0
                match = []
                for name in names:
                    if k2 in results[name]:
                        match.append(name)
                        cnt += 1
                if cnt > 1: # If there are more than one match for GO IDs in 4 proteins , the GO IDs will be added to found list 
                    found.append(k2)
                    fh.write(','.join(match) + "\t" + k2 + "\t" + v2 + "\n") # Writing a table (tab delimited) containing GO ID’s and terms in common across at least 2 proteins. 
                    
step4()
'''
extracting the protein sequence from each protein's XML file using the ElementTree module.
'''
list1 = []
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    namespace = re.match(r"{.*}", root.tag).group()
    elem = root.find(namespace+"entry")
    subelem = elem.findall(namespace+"sequence")
    for child in subelem:
        if child.text:
            list1.append(child.text.rstrip())
'''
Creating a list for RegEx of the PROSITE patterns 
'''
rgx_list = []
rgx_list.append(r"[LIVMFYC][^A][HY].D[LIVMFY][RSTAC][^D][^PF]N[LIVMFYC]{3}")
rgx_list.append(r"[RK].{3}[DE].{2}Y")
rgx_list.append(r"[RK].{2}[DE].{3}Y")
'''
A function is written  to search each protein sequence for the PROSITE patterns.
'''
def regex(rgx,seq,n):
    matches = re.finditer(rgx, seq)
    for match in matches: # If matches are found, the matching sequence and the location of each match is printed out to the screen. 
        print("%s is located between indices %s of %s" %(match.group(), match.span(), names[n]))
for n,seq in enumerate(list1): #calling the regex() function
    for rgx in rgx_list:
         regex(rgx,seq,n)
