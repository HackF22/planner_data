import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

#Add Course Offering Data

def add_cics_course(filename):
    course_offering_plan = 'https://www.cics.umass.edu/content/course-offering-plan'
    resp = requests.get(course_offering_plan)
    page = BeautifulSoup(resp.text, "html.parser")
    tables = page.find_all("tbody")

    file = open(filename, mode = "r+")
    array = []
    #This function should only work when the file is empty
    mypath = Path(filename)
    if(not mypath.stat().st_size == 0): return

    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            course = {}
            tds = tr.find_all("td")
            course_id = tds[0].text + " " + tds[1].text
            course['course_id'] = course_id
            course['name'] = tds[2].text
            course['credits'] = int(tds[3].text)
            course['semesters'] = tds[4].text
            array.append(course)
    json.dump(array, file, indent=2)
    file.close()

#Add Gen Eds
def add_geneds(filename):
    gened_url = 'https://www.umass.edu/registrar/students/general-educationacademic-requirements/gen-ed-list'
    resp = requests.get(gened_url)
    page = BeautifulSoup(resp.text, "html.parser")
    rows = page.find_all("table")[1].find_all("tr")

    file = open(filename, mode = "r+")
    old = json.load(file)
    array = []
    #This function should not run if the file already has gened courses
    for obj in old:
        if 'gened' in obj:
            return

    for row in rows:
        course = {}
        first = True
        tds = row.find_all("td")
        id = tds[1].get_text().strip()
        gened = tds[0].get_text().strip()
        for obj in array:
            if(obj['course_id'] == id): first = False
        if(first):
            course['course_id'] = id
            course['gened'] = [gened]
            course['name'] = tds[2].get_text().strip()
            course['credits'] = 4
            array.append(course)
        elif(gened not in obj['gened']):
            obj['gened'].append(gened)
        
    
    old = old + array
    file.truncate(0)
    file.seek(0)
    json.dump(old, file, indent=2)
    file.close()

def add_ece_course(filename):
    url = 'https://ece.umass.edu/ece-course-descriptions'
    resp = requests.get(url)
    page = BeautifulSoup(resp.text, "html.parser").find('div', class_='field-item even')
    #print(content)

    file = open(filename, mode = "r+")
    old = json.load(file)
    #This function should not run if the file already has ECE courses
    for obj in old:
        if 'ECE' in obj['course_id']:
            return

    next = page.find('h2')
    while(next):
        next = next.find_next('h2')
        if(next is None): break
        if('ECE' not in next.get_text()): continue
        course = {}
        course['course_id'] = next.get_text().split(':')[0].strip()
        course['name'] = next.get_text().split(':')[1]
        course['description'] = next.next_sibling.next_sibling.get_text().strip()
        old.append(course)
        
    file.truncate(0)
    file.seek(0)
    json.dump(old, file, indent=2)
    file.close()

def add_math_course(filename):
    url = 'https://www.math.umass.edu/course-descriptions'
    resp = requests.get(url)
    page = BeautifulSoup(resp.text, "html.parser").find('div', class_='view-content')

    file = open(filename, mode = "r+")
    old = json.load(file)
    array = []
    #This function should not run if the file already has ECE courses
    for obj in old:
        if 'MATH 412' in obj['course_id']:
            print(obj)
            return

    next = page.find('h3')
    while(next is not None):
        if('MATH' in next.get_text()): 
            course = {}
            first = True
            id = next.get_text().split(':')[0].strip()
            if('.' in id):
                first = True
                id = id.split('.')[0]
                for obj in array:
                    if(obj['course_id'] == id): first = False
            course['course_id'] = id
            course['name'] = next.get_text().split(':')[1].strip()
            locator = next.find_next('span', class_='field-label')
            while('Description' not in locator.get_text()):
                locator = locator.find_next('span', class_='field-label')
            course['description'] = locator.find_next('p').get_text().strip()
            if (first): array.append(course)
        next = next.find_next('h3')
        
    old = old + array
    file.truncate(0)
    file.seek(0)
    json.dump(old, file, indent=2)
    file.close()


#Update the existing courses given an url array
#The array should be arranged from newest to oldest
def update_semesters(filename, urlArray):

    file = open(filename, mode = "r+")
    old = json.load(file)
    #Will not run if file is empty
    mypath = Path(filename)
    if(mypath.stat().st_size == 0): return

    counter = 4
    for url in urlArray:
        if(counter == 0): break #Up to four semesters
        description = requests.get(url)
        page = BeautifulSoup(description.text, "html.parser")
        next = page.find('h2')
        #print(page.find_all("div", class_="field-item even"))
        while(next):
            next = next.find_next('h2')
            if(not next): break
            if(type(next.contents[0]) == 'NavigableString'): 
                break
            hasInstructor = False
            course_id = next.get_text().split(':')[0]
            if(next.next_sibling.next_sibling.name == 'h3'): hasInstructor = True
            for obj in old: 
                if(obj['course_id'] == course_id):
                    if(hasInstructor):
                        instructor_field = next.next_sibling.next_sibling
                        description = instructor_field.next_sibling.next_sibling.get_text()
                        instructors = instructor_field.get_text().strip().split(': ')[1].split(', ')
                        if('past_instructors' not in obj): obj['past_instructors'] = instructors
                        else: obj['past_instructors'] = obj['past_instructors'] + instructors
                        if ('description' not in obj): obj['description'] = description
                    if(not hasInstructor):
                        if ('description' not in obj): 
                            description = next.next_sibling.next_sibling.get_text()
                            obj['description'] = description
        file.truncate(0)
        file.seek(0)
        json.dump(old, file, indent=2)
        counter -= 1
    file.close()

#Helper Function
def countFreq(arr):
    mp = dict()
    for i in range(len(arr)):
        if arr[i] in mp.keys():
            mp[arr[i]] += 1
        else:
            mp[arr[i]] = 1             
    return mp

def count_instructors(filename):
    file = open(filename, mode = "r+")
    old = json.load(file)
    #Will not run if file is empty
    mypath = Path(filename)
    if(mypath.stat().st_size == 0): return

    for course in old:
        if 'past_instructors' in course:
            instructors = course['past_instructors']
            mp = countFreq(instructors)
            if(len(mp) >= 2):
                sortedMp = {k: v for k, v in sorted(mp.items(), key=lambda item: item[1])}
                course['past_instructors'] = [list(sortedMp)[0], list(sortedMp)[1]]
            else:
                course['past_instructors'] = [list(mp)[0]]

    file.truncate(0)
    file.seek(0)
    json.dump(old, file, indent=2)
    file.close()

def add_prerequisites(prereqFile, coursesFile):
    outfile = open(coursesFile, mode = "r+")
    readfile = open(prereqFile, mode = "r+")
    old = json.load(outfile)
    data = json.load(readfile)
    for obj in old:
        #Delete old prerequisites
        if 'prerequisite' in obj:
            del obj['prerequisite']
        for p in data:
            pID = p['course_id']
            if(pID == obj['course_id']):
                obj['prerequisite'] = p['prerequisite']
    outfile.truncate(0)
    outfile.seek(0)
    json.dump(old, outfile, indent=2)
    readfile.close()
    outfile.close()

            
add_cics_course("Data/Courses.json")
add_geneds("Data/Courses.json")

sp23 = 'https://www.cics.umass.edu/content/spring-23-course-descriptions'
fa22 = 'https://www.cics.umass.edu/content/fall-22-course-descriptions'
sp22 = 'https://www.cics.umass.edu/content/spring-22-course-descriptions'
fa22 = 'https://www.cics.umass.edu/content/fall-21-course-descriptions'
sp21 = 'https://www.cics.umass.edu/content/spring-21-course-descriptions'
urlArray = [sp23, fa22, sp22, fa22, sp21]
update_semesters("Data/Courses.json", urlArray)

count_instructors("Data/Courses.json")

add_prerequisites("Data/PrerequisiteManual.json", "Data/Courses.json")

add_ece_course("Data/Courses.json")
add_math_course("Data/Courses.json")