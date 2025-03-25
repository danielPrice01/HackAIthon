import json
from interactive_chat import InteractiveChatBot

def print_table(headers, rows):
    """
    Prints a table given the headers and rows.
    
    Parameters:
      headers (list): A list of header strings.
      rows (list of lists): Each inner list represents a row.
    """
    col_widths = [
        max(len(str(item)) for item in [header] + [row[i] for row in rows])
        for i, header in enumerate(headers)
    ]
    header_line = " | ".join(header.ljust(width) for header, width in zip(headers, col_widths))
    divider = "-+-".join("-" * width for width in col_widths)
    
    print(header_line)
    print(divider)
    for row in rows:
        row_line = " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths))
        print(row_line)

def main():
    bot = InteractiveChatBot()
    print("Welcome to the Course Filter Chat Interface (Command-line version)!")
    print("Type your message and press Enter. Type 'exit' or 'quit' to stop.")
    print("-" * 60)

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break

        public_resp, current_state_text = bot.predict(user_input)
        print("\nAssistant: " + public_resp)
        print("\n[Current Filter Table]")
        current_state = json.loads(current_state_text)
        headers = current_state.get("columns", [])
        courses = current_state.get("courses", [])
        rows = []
        for course in courses:
            row = [course.get(col, "") for col in headers]
            rows.append(row)
        print_table(headers, rows)
        print("-" * 60)

if __name__ == "__main__":
    main()
