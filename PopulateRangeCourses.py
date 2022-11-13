import json
import argparse
import re


# Returns a list of courses that are numbered higher than start.
def find_range_courses(courses, start):
    higher = []
    for course in courses:
        name = course["course_id"]
        if not name.startswith("COMPSCI"):
            continue
        course_num_str = name[8:]
        only_num = int(re.sub("\D", "", course_num_str))
        if only_num >= start:
            higher.append(name)
    return higher


def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("courses_json")
    parser.add_argument("wildcard_json")
    args = parser.parse_args()

    print(f"Parsing '{args.courses_json}' ...")
    with open(args.courses_json, "r") as courses_json:
        courses = json.load(courses_json)

    print(f"Parsing '{args.wildcard_json}' ...")
    with open(args.wildcard_json, "r") as wildcard_json:
        wildcard_courses = json.load(wildcard_json)

    print(f"Populating the Range Courses in wildcard courses file ...")
    for wc in wildcard_courses:
        wc_name = wc["course_id"][1:]     # Remove the "@" at the beginning
        # For now, only operate on range courses in the form "@n+"
        if wc_name[-1] == "+":
            range_start = int(wc_name[:-1])
            range_courses = find_range_courses(courses, range_start)
            wc["associated_courses"] = range_courses

    print(f"Writing the range course populated wildcard classes into '{args.wildcard_json}'")
    with open(args.wildcard_json, "w") as wildcard_json:
        json.dump(wildcard_courses, wildcard_json, indent=2)
    
    print("Done")


if __name__ == "__main__":
    main()
