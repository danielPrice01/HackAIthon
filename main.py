import json
from filter import Filter

def print_table(headers, rows):
    """
    Prints a table given the headers and rows.
    
    Parameters:
      headers (list): A list of header strings.
      rows (list of lists): Each inner list represents a row.
    """
    # Calculate column widths based on the longest item in each column.
    col_widths = [
        max(len(str(item)) for item in [header] + [row[i] for row in rows])
        for i, header in enumerate(headers)
    ]
    
    # Create header line and divider.
    header_line = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
    divider = "-+-".join("-" * width for width in col_widths)
    
    print(header_line)
    print(divider)
    for row in rows:
        row_line = " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths))
        print(row_line)

def main():
    # Initialize Filter with the JSON file inside the "courses" folder.
    filter_file_path = "courses/courses.json"
    course_filter = Filter(filter_file_path)
    
    # Step 1: Filter courses whose "prereq" field contains "CIS 1200".
    courses_with_prereq = course_filter.filter_courses("prereq", "CIS 1200")
    
    # Step 2: Print table of courses that have "CIS 1200" in prereqs.
    headers = ["ID", "Name", "Prereq", "Available"]
    rows = []
    for course in courses_with_prereq:
        rows.append([
            course.get("id", ""),
            course.get("name", ""),
            course.get("prereq", ""),
            course.get("available", "")
        ])
    
    print("Courses with 'CIS 1200' in prereq:")
    print_table(headers, rows)
    
    # Step 3: From these courses, filter those that are offered in "Spring".
    spring_courses = course_filter.filter_courses("available", "Spring")
    # Note: If you want to filter among the already filtered courses, you could use a list comprehension:
    # spring_courses = [course for course in courses_with_prereq if "Spring" in course.get("available", "")]
    
    # For clarity, let's assume we are filtering from courses_with_prereq:
    spring_courses = [course for course in courses_with_prereq if "Spring" in course.get("available", "")]
    
    # Step 4: Print a new table with class name, prereqs, and availability.
    headers2 = ["Name", "Prereq", "Available"]
    rows2 = []
    for course in spring_courses:
        rows2.append([
            course.get("name", ""),
            course.get("prereq", ""),
            course.get("available", "")
        ])
    
    print("\nSpring courses with 'CIS 1200' in prereq:")
    print_table(headers2, rows2)

if __name__ == "__main__":
    main()
