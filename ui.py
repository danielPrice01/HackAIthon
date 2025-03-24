import tkinter as tk
from tkinter import ttk
from filter import Filter

class FilterUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Filter UI")
        self.geometry("800x600")
        
        # Initialize the Filter with the JSON file inside the "courses" folder.
        filter_file = "courses/courses.json"
        self.filter_obj = Filter(filter_file)
        
        # Create the table (Treeview) for displaying courses.
        self.tree = ttk.Treeview(self, columns=[], show="headings")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a frame for adding filters.
        add_frame = tk.Frame(self)
        add_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Label(add_frame, text="Attribute:").pack(side=tk.LEFT)
        self.attr_entry = tk.Entry(add_frame)
        self.attr_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(add_frame, text="Value (optional):").pack(side=tk.LEFT)
        self.value_entry = tk.Entry(add_frame)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(add_frame, text="Add Filter", command=self.add_filter).pack(side=tk.LEFT, padx=5)
        
        # Create a frame for deleting filters.
        del_frame = tk.Frame(self)
        del_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Label(del_frame, text="Delete Filter (attribute):").pack(side=tk.LEFT)
        self.del_attr_entry = tk.Entry(del_frame)
        self.del_attr_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(del_frame, text="Delete Filter", command=self.delete_filter).pack(side=tk.LEFT, padx=5)
        
        # Create a frame for prompt_ai functionality.
        prompt_frame = tk.Frame(self)
        prompt_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Label(prompt_frame, text="Prompt AI:").pack(side=tk.LEFT)
        self.prompt_entry = tk.Entry(prompt_frame, width=50)
        self.prompt_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(prompt_frame, text="Run prompt_ai", command=self.run_prompt_ai).pack(side=tk.LEFT, padx=5)
        
        # Create a Text widget to display the prompt_ai output.
        self.prompt_result = tk.Text(self, height=3)
        self.prompt_result.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Initially update the table with the default state.
        self.update_table()
    
    def update_table(self):
        """
        Update the Treeview based on the current state of the Filter.
        """
        # Retrieve the current state (a dict with "columns" and "courses").
        state = self.filter_obj.get_current_state()
        columns = state["columns"]
        courses = state["courses"]
        
        # Clear current table: remove all headings and items.
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.W)
        
        # Insert each course row.
        for course in courses:
            row = [course.get(col, "") for col in columns]
            self.tree.insert("", tk.END, values=row)
    
    def add_filter(self):
        """
        Add a new filter (and update the table).
        """
        attr = self.attr_entry.get().strip()
        value = self.value_entry.get().strip()
        if attr:
            self.filter_obj.add_filter(attr, value)
            self.update_table()
        self.attr_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
    
    def delete_filter(self):
        """
        Delete a filter based on the attribute (and update the table).
        """
        attr = self.del_attr_entry.get().strip()
        if attr:
            self.filter_obj.delete_filter(attr)
            self.update_table()
        self.del_attr_entry.delete(0, tk.END)
    
    def run_prompt_ai(self):
        """
        Tokenize the input from the prompt entry and display the tokens in the text widget.
        """
        input_str = self.prompt_entry.get().strip()
        tokens = input_str.split()
        result = "Tokens: " + str(tokens)
        self.prompt_result.delete("1.0", tk.END)
        self.prompt_result.insert(tk.END, result)

if __name__ == "__main__":
    app = FilterUI()
    app.mainloop()
