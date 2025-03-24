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
    f = Filter(filter_file_path)
    
    # Function to extract rows based on current columns.
    def state_rows(state):
        # state["courses"] is a list of dictionaries; state["columns"] is the list of keys to display.
        return [[course.get(col, "") for col in state["columns"]] for course in state["courses"]]
    
    # --- Initial state: default columns ("id" and "name") for all courses ---
    state = f.get_current_state()
    print("Initial state:")
    print("Columns:", state["columns"])
    print_table(state["columns"], state_rows(state))
    print("\n---\n")
    
    # --- Add a filter for prereq "CIS 1200" ---
    f.add_filter("prereq", "CIS 1200")
    state = f.get_current_state()
    print("After adding filter: prereq contains 'CIS 1200'")
    print("Columns:", state["columns"])
    print_table(state["columns"], state_rows(state))
    print("\n---\n")
    
    # --- Add a filter for available "Spring" ---
    f.add_filter("available", "Spring")
    state = f.get_current_state()
    print("After adding filter: available contains 'Spring'")
    print("Columns:", state["columns"])
    print_table(state["columns"], state_rows(state))
    print("\n---\n")
    
    # --- Delete the "available" filter ---
    f.delete_filter("available")
    state = f.get_current_state()
    print("After deleting the 'available' filter")
    print("Columns:", state["columns"])
    print_table(state["columns"], state_rows(state))
    print("\n---\n")
    
    # --- Demonstrate the prompt_ai function ---
    print("Using prompt_ai:")
    f.prompt_ai("This is an example input for AI prompting")

if __name__ == "__main__":
    main()
