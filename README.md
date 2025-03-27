---
sdk: gradio
app_file: app.py
---

# Course Filter Chat Application

This application allows students to interactively filter course data using two modes: **Interactive Chat** and **Agentic Swarm**. After each interaction, the current filter state (columns and courses) is printed.

## Components

### Filter Class (filter.py)

- **Purpose:**  
  Loads course data from a JSON file and applies filters.
- **Key Methods:**
  - `add_filter(attribute, value)`: Adds or updates a filter.
  - `delete_filter(attribute)`: Removes a filter.
  - `get_current_state()`: Returns a dictionary containing:
    - `"columns"`: Current column headers.
    - `"courses"`: Current filtered course rows.
  - `add_column(class_ids, attribute, values)`: Adds a new column (e.g., swarm answers) to all courses.
  - `delete_column(attribute)`: Removes an additional column from the filter.

### InteractiveChatBot Class (interactive_chat.py)

- **Purpose:**  
  Manages an interactive chat session.
- **Flow:**
  1. Extracts filter instructions from the user’s message using OpenAI.
  2. Updates the Filter instance (first processing deletion instructions, then additions).
  3. Returns a public response along with the current filter state.
- **Usage:**  
  When mode 1 is selected, the user’s message is processed and the chatbot outputs a public response and the updated filter table.

### AgenticSwarm Class (swarm.py)

- **Purpose:**  
  Processes a query against a limited set of courses (maximum 15).
- **Flow:**
  1. Retrieves courses from the current Filter state.
  2. For each course, a `CourseBot` processes the query asynchronously.
  3. Collects responses and adds a new column (e.g., `"swarm_answer"`) to the Filter.
- **Usage:**  
  When mode 2 is selected, the swarm processes the query, returns results for each course, and updates the filter table.

### Main Loop (app.py)

- **Functionality:**  
  The main loop repeatedly:
  1. Prompts the user to select a mode:
     - **1:** Interactive Chat
     - **2:** Agentic Swarm
  2. Processes the user's input using the selected mode.
  3. Prints the public response.
  4. Prints the current filter state (columns and course rows).
  5. Re-prompts the user for a mode selection.
  - The loop continues until the user types "quit" or "exit".

## Usage

1. **Configure Environment:**  
   Create an environment file (e.g., `.env` or `api.env`) with your API key:
   ```env
   API_TOKEN=your_api_key_here
   ```
