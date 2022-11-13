import json

def findPrereq(infile, outfile):
    read = open(infile, mode = "r")
    write = open(outfile, mode = "w")
    data = json.load(read)
    array = []
    for course in data:
        if 'description' in course:
            obj = {}
            description = course['description']
            if "Prerequisite: " in description:
                prereq = course['description'].split("Prerequisite: ")[-1]
                if"credit" in prereq:
                    prereq = prereq.split(".")[0]              
                obj['course_id'] = course['course_id']
                obj['prerequisite'] = prereq
                array.append(obj)
    json.dump(array, write, indent=2)
    read.close()
    write.close()

findPrereq('Data/Courses.json', 'Data/Prerequisite.json')

def findDiff(file1, file2):
    fp1 = open(file1, mode="r")
    fp2 = open(file1, mode="r")
    data1 = json.load(fp1)
    data2 = json.load(fp2)
    for obj in data1:
        id1 = obj['course_id']
        found = False
        for x in data2:
            if x['course_id'] == id1:
                found = True
        if not found: print(id1)
    fp1.close()
    fp2.close()

findDiff('Data/Prerequisite.json', 'Data/PrerequisiteManual.json')
findDiff('Data/PrerequisiteManual.json', 'Data/Prerequisite.json')