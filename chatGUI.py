import tkinter as tk
from tkinter import ttk, scrolledtext
import json
from interactive_chat import InteractiveChatBot

class ChatGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Filter Chat Interface")
        self.geometry("900x700")
        
        # Instantiate the interactive chat bot.
        self.bot = InteractiveChatBot()
        
        # Create a scrolled text widget to display the conversation.
        self.conversation_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15)
        self.conversation_display.config(state=tk.DISABLED)
        self.conversation_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create a Treeview widget to display the current filter table.
        self.table_display = ttk.Treeview(self, columns=[], show="headings")
        self.table_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create an input frame for user messages.
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=10, fill=tk.X)
        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)
    
    def send_message(self):
        user_message = self.input_entry.get().strip()
        if not user_message:
            return
        self.append_conversation("User: " + user_message)
        self.input_entry.delete(0, tk.END)
        
        # Get the public response and current filter state from the bot.
        public_resp, current_state_text = self.bot.predict(user_message)
        self.append_conversation("Assistant: " + public_resp)
        self.update_table(current_state_text)
    
    def append_conversation(self, text):
        self.conversation_display.config(state=tk.NORMAL)
        self.conversation_display.insert(tk.END, text + "\n")
        self.conversation_display.see(tk.END)
        self.conversation_display.config(state=tk.DISABLED)
    
    def update_table(self, state_text):
        try:
            current_state = json.loads(state_text)
            headers = current_state.get("columns", [])
            courses = current_state.get("courses", [])
        except Exception as e:
            headers = []
            courses = []
        
        # Clear current Treeview items.
        for item in self.table_display.get_children():
            self.table_display.delete(item)
        
        self.table_display["columns"] = headers
        for col in headers:
            self.table_display.heading(col, text=col)
            self.table_display.column(col, width=120, anchor=tk.W)
        
        # Insert rows.
        for course in courses:
            row = [course.get(col, "") for col in headers]
            self.table_display.insert("", tk.END, values=row)

if __name__ == "__main__":
    app = ChatGUI()
    app.mainloop()
