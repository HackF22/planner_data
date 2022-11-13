import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

#Get AP Credit Lists
ap_credits = 'https://www.umass.edu/registrar/students/transfer-information/transferring-credit/advanced-placement-test-university-recommended'
outfile = open("./data/PreCollege.json", mode = "w")
resp = requests.get(ap_credits)
page = BeautifulSoup(resp.text, "html.parser")
rows = page.find_all("tr")
APs = []
for row in rows[2:]:
    superscripts = row.find("sup")
    if(superscripts): superscripts.extract()
    fields = row.find_all("td")
    AP = {}
    test = fields[0].get_text().strip()
    score = fields[1].get_text().strip()
    genedfield = fields[3].get_text().strip()
    gened = ''
    filteredChars = ''.join((filter(lambda x: x.isupper() or x.isnumeric(), genedfield)))
    for i in range(0, len(filteredChars) - 1, 2): 
        gened += filteredChars[i] + filteredChars[i + 1] + ', '
    gened = gened[:-2]
    AP['name'] = "AP " + test + " with score of " + score
    AP['credits'] = fields[2].get_text().strip()
    if len(gened) > 0: AP['gened'] = gened
    APs.append(AP)
json.dump(APs, outfile, indent=2)
outfile.close()

#Manually add corresponding courses
outfile = open("./data/PreCollege.json", mode = "r+")
old = json.load(outfile)
array = []
for AP in old:
    if(AP['name'] == "AP Calculus AB with score of 4 or 5") or (AP['name'] == "AP Calculus BC - AB subscore with score of 4 or 5"):
        AP['corresponding_course'] = 'MATH 131'
    if(AP['name'] == "AP Calculus BC with score of 4 or 5"):
        AP['corresponding_course'] = ["MATH 131", "MATH 132"]
    if(AP['name'] == "AP Computer Principles with score of 4 or 5"):
        AP['corresponding_course'] = 'INFO 101'
    if(AP['name'] == "AP Comp Sci A with score of 4 or 5"):
        AP['corresponding_course'] = 'COMPSCI 121'
    if(AP['name'] == "AP Physics C - Mechanics with score of 4 or 5"):
        AP['corresponding_course'] = 'PHYSICS 151'
    if(AP['name'] == "AP Physics C - Elec & Mag with score of 4 or 5"):
        AP['corresponding_course'] = 'PHYSICS 152'
    #Fixes AP Sapnish
    if(AP['name'] == "AP Spanish Literature with score of 4 or 5"):
        AP['gened'] = 'AL'
    array.append(AP)
outfile.seek(0)
json.dump(array, outfile, indent=2)
outfile.close()

