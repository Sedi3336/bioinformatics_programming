from lxml import etree
import requests
import re
from io import StringIO
## Get the code from the url
html = requests.get("https://en.wikipedia.org/wiki/Nucleic_acid_notation").text
parser = etree.HTMLParser()
tree = etree.parse(StringIO(html),parser)
'''
extracting  the nucleotides represented by the IUPAC nucleotide codes W, S, M, K, R, and Y from the table in the Wikipedia page
'''
trs = tree.xpath('//table/tbody/tr[@bgcolor="#e8e8e8"]')# Extracting parts of the table with a specific background color (tr attribute).
dict1 = {}
for tr in trs:
    l1 = []
    for td in tr.xpath('./td'): # Finding td elements in tr
        if td.keys():# Skipping td with any number of attributes
            continue
        l1.append(td.text)# text of tds with no attribute are added in the l1 list
    # Create a dictionary with the key of b's text (b is a child element of td) and value of part of items of l1 list.
    for b in tr.xpath('./td/b'):
        dict1[b.text] = [i for i in l1 if i in ["A", "T", "C", "G"]]
#print(dict1)
# A subclass for the exception class is created that can be raised when a sequence is something other than DNA
class SeqTypeError(Exception):
    def __init__(self, seq):
        self.seq = seq 
    def __str__(self):
        return ("%s is not a DNA!" %(str(self.seq)))
# DNAorNot function gets a sequence of the string type and raises exception if it is not a DNA.
def DNAorNot(seq):
    s = set(seq.upper()) - set(['A', 'T', 'C', 'G'])
    if len(s) != 0:
        raise SeqTypeError(seq)
# Creating the regular expressions for the recognition sites of each enzyme
ResEnzymeDict0 = {"EcoRI": "GAATTC" , "EalI": "YGGCCR" , "ErhI": "CCWWGG" , "EcaI": "GGTNACC" , "FblI": "GTMKAC"}
for k,v in ResEnzymeDict0.items():
    rgx = ""
    for ch in v:
        if ch not in ["A", "T", "C", "G"]:
            rgx += "[" + "".join(dict1[ch]) + "]"
            continue # To not include the key characters into the regex
        rgx += ch # Add A,T,C,G in the regex
    ResEnzymeDict0[k] = rgx # Rewrite the value of the current key
class sequence:
    ResEnzymeDict = ResEnzymeDict0 # a class attribute called ResEnzymeDict, which is a dictionary of restriction enzymes and their recognition sites (as regular expression patterns)
    def __init__(self, sq): # init will be run anytime that an object is created
        DNAorNot(sq) # checking whether the sequence is DNA and raise the exception if not
        self.DNA = sq # an instance attribute to hold a DNA sequence
    def restriction_sites(self):# a method, called "restriction_sites" that searches the DNA sequence for the restriction enzyme recognition sites
        for Enzyme,rgx in self.ResEnzymeDict.items():
            m = re.finditer(rgx, self.DNA)
            if m:
                for x in m:
                        print(Enzyme, x.group()) # printing out those enzymes whose recognition sites exist in the DNA sequence along with the sequence that matched the recognition site pattern.
# Testing my code
seqObj = sequence("TGGCCGAATTCCGGCCGCGGCCA")
seqObj.restriction_sites()
