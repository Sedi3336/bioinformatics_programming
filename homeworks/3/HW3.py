import xml.etree.ElementTree as ET
import re
'''

'''
xml_files = ['./XMLs/ERBB1.xml', './XMLs/ERBB2.xml', './XMLs/ERBB3.xml', './XMLs/ERBB4.xml']
names = []
results = {}
for xml_file in xml_files:
    result = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    namespace = re.match(r"{.*}", root.tag).group()
    elem = root.find(namespace+"entry")
    subelem = elem.findall(namespace+"dbReference")
    for child in subelem:
        if 'type' not in child.attrib:
            continue
        if child.attrib['type'] == 'GO':
            for Gchild in child:
                if Gchild.attrib['type'] == 'term':
                    result[child.attrib['id']] = Gchild.attrib['value']
    name = xml_file.replace("./XMLs/","").replace(".xml","")
    names.append(name)
    results[name] = result

def step3():
    with open("./common_in_4.tsv","w") as fh:
        fh.write("GO_ID\tGO_term\n")
        for k,v in results[names[0]].items():
            if k in (results[names[1]]) and k in (results[names[2]]) and k in (results[names[3]]):
                fh.write(k + "\t" + v + "\n")

step3()

def step4():
    with open("./common_in_2.tsv","w") as fh:
        found = []
        fh.write("Protein\tGO_ID\tGO_term\n")
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
                if cnt > 2:
                    found.append(k2)
                    fh.write(','.join(match) + "\t" + k2 + "\t" + v2 + "\n")
                    
step4()
list1 = []
for xml_file in xml_files:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    namespace = re.match(r"{.*}", root.tag).group()
    elem = root.find(namespace+"entry")
    subelem = elem.findall(namespace+"sequence")
    for el in subelem:
        if el.text:
            list1.append(el.text.rstrip())

rgx_list = []
rgx_list.append(r"[LIVMFYC][^A][HY].D[LIVMFY][RSTAC][^D][^PF]N[LIVMFYC]{3}")
rgx_list.append(r"[RK].{3}[DE].{2}Y")
rgx_list.append(r"[RK].{2}[DE].{3}Y")
def regex(rgx,seq,n):
    matches = re.finditer(rgx, seq)
    for match in matches:
        print("%s is located between indices %s of %s" %(match.group(), match.span(), names[n]))
for n,seq in enumerate(list1):
    for rgx in rgx_list:
        regex(rgx,seq,n)
