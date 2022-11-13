import json
import argparse


# Returns a list of courses that satisfy the specified gened.
def find_gened_courses(courses, gened):
    geneds = []
    for course in courses:
        if "gened" in course and course["gened"] == gened:
            geneds.append(course["course_id"])
    return geneds


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

    print(f"Populating the GenEds in wildcard courses file ...")
    for wc in wildcard_courses:
        wc_name = wc["course_id"][1:]     # Remove the "@" at the beginning
        wc_courses = find_gened_courses(courses, wc_name)
        # If the wildcard class is a gened
        if wc_courses:
            wc["associated_courses"] = wc_courses

    print(f"Writing the gened-populated wildcard classes into '{args.wildcard_json}'")
    with open(args.wildcard_json, "w") as wildcard_json:
        json.dump(wildcard_courses, wildcard_json, indent=2)
    
    print("Done")


if __name__ == "__main__":
    main()
