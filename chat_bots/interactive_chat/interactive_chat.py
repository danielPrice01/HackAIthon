import os
from dotenv import load_dotenv
import time
import json
import openai
from filter import Filter

class InteractiveChatBot:
    MAX_HISTORY = 5

    def __init__(self, env_file=".env", filter_inst=None, courses_file="courses/courses.json",
                 model="gpt-4o-mini", max_tokens=2000, temperature=0.7, top_p=0.95):
        load_dotenv(env_file)
        openai.api_key = os.environ.get("API_TOKEN")
        self.filter_instance = filter_inst
        self.history = []
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.system_prompt = (
            "You are a helpful assistant that manages course filters based on user input. "
            "You extract filtering instructions (such as courses taken, desired availability, or course units) "
            "and update the course list accordingly. After applying the filters, provide a helpful response."
        )
        self.filter_instruction_cache = {}

    def _limit_history(self):
        if len(self.history) > self.MAX_HISTORY:
            self.history = self.history[-self.MAX_HISTORY:]

    def get_filter_instructions(self, user_message):
        if user_message in self.filter_instruction_cache:
            return self.filter_instruction_cache[user_message]

        filter_prompt = (
            "You are a filter extractor. Your task is to analyze any user's message and determine if any course filter instructions should be added or deleted. "
            "Your output must be a valid JSON object with exactly two keys: 'add' and 'delete'. No matter how the user phrases their message, your output must follow this exact format and contain no additional text or commentary. "
            "If the user's message contains filter instructions, extract them as follows:\n\n"
            "1. The 'add' key must map to a list of objects. Each object must have:\n"
            "   - 'attribute': one of these allowed attributes: 'available', 'cu', 'prereq', 'labels', 'mutually exclusive'.\n"
            "   - 'value': a string representing the filter value to add. For 'available', valid values are: 'Fall', 'Spring', 'Fall or Spring', an empty string (\"\"), or 'Not offered every year'. "
            "For 'cu', valid values are: '1 Course Unit' or '0-0.5 Course Units'. For 'prereq', the value must be a course code in the format 'CIS' followed by a number (e.g., 'CIS 1200'). "
            "For 'labels', the value must be one or more of the following labels (if multiple apply, include them all):\n"
            "   \"Introductory Programming\", \"Advanced Programming\", \"Object-Oriented Programming\", \"Functional Programming\", \"Procedural Programming\", "
            "\"Programming Paradigms\", \"Data Structures\", \"Algorithms\", \"Algorithm Analysis\", \"Computational Complexity\", \"Theory of Computation\", "
            "\"Discrete Mathematics\", \"Mathematical Foundations\", \"Proof Techniques\", \"Logic and Reasoning\", \"Software Engineering\", \"Agile Development\", "
            "\"Test-Driven Development\", \"Software Design\", \"Software Architecture\", \"Software Systems\", \"Operating Systems\", \"Computer Architecture\", "
            "\"Digital Systems\", \"Embedded Systems\", \"Systems Programming\", \"Computer Networks\", \"Distributed Systems\", \"Internet and Web Systems\", "
            "\"Cloud Computing\", \"Big Data Analytics\", \"Data Mining\", \"Data Exploration\", \"Data Visualization\", \"Database Systems\", \"NoSQL Databases\", "
            "\"SQL and Relational Databases\", \"Human–Computer Interaction\", \"User Interface Design\", \"Interaction Design\", \"Visual Design\", "
            "\"Mobile App Development\", \"iOS Programming\", \"Android Programming\", \"Web Development\", \"Frontend Development\", \"Backend Development\", "
            "\"Full-Stack Development\", \"DevOps\", \"Cybersecurity\", \"Computer and Network Security\", \"Cryptography\", \"Ethical Hacking\", \"Privacy and Security\", "
            "\"Ethical Algorithm Design\", \"Artificial Intelligence\", \"Machine Learning\", \"Deep Learning\", \"Neural Networks\", \"Reinforcement Learning\", "
            "\"Natural Language Processing\", \"Computer Vision\", \"Image Processing\", \"Computational Photography\", \"Robotics\", \"Computer Animation\", "
            "\"Game Design\", \"Game Development\", \"Virtual Reality\", \"Augmented Reality\", \"Interactive Graphics\", \"GPU Programming\", \"Parallel Computing\", "
            "\"Scientific Computing\", \"Numerical Methods\", \"Simulation and Modeling\", \"Quantum Computing\", \"Quantum Information Science\", "
            "\"Blockchain Technology\", \"Distributed Ledger Technology\", \"Bioinformatics\", \"Computational Biology\", \"Biomedical Image Analysis\", "
            "\"Computational Neuroscience\", \"Cognitive Science\", \"Data Science\", \"Statistical Inference\", \"Probability and Statistics\", "
            "\"Stochastic Processes\", \"Optimization Techniques\", \"DevOps Practices\", \"Research Methods\", \"Independent Study\", \"Capstone Projects\", "
            "\"Senior Thesis\", \"Special Topics\", \"Seminar Courses\", \"Interdisciplinary Studies\", \"Ethics in Technology\", \"Policy and Technology\", "
            "\"Python Programming\", \"C++ Programming\", \"Java Programming\", \"JavaScript Programming\", \"Ruby on Rails\", \"Go Programming\", \"Haskell Programming\", "
            "\"C Programming\", \"Rust Programming\", \"OCaml Programming\", \"SQL Programming\", \"R Programming\", \"MATLAB Programming\", \"TypeScript\", "
            "\"Swift Programming\", \"PHP Programming\", \"Perl Programming\", \"Recursion Techniques\", \"Iterative Methods\", \"Unit Testing\", \"Debugging Techniques\", "
            "\"Code Optimization\", \"Code Profiling\", \"Object-Oriented Design Patterns\", \"Functional Design Patterns\", \"Concurrent Programming Techniques\", "
            "\"Parallel Processing Techniques\", \"Memory Management Techniques\", \"Compiler Design Techniques\", \"Heuristic Algorithms\", \"Graph Algorithms\", "
            "\"Dynamic Programming\", \"Randomized Algorithms\", \"Machine Learning Techniques\", \"Deep Learning Techniques\", \"NLP Techniques\", "
            "\"Image Processing Techniques\", \"Simulation and Modeling Techniques\".\n\n"
            "2. The 'delete' key must map to a list of attribute names (strings) that should be removed from the filters.\n\n"
            "Important: Your output must strictly be a valid JSON object with the following exact format, with no additional commentary:\n"
            "{\n"
            "  \"add\": [\n"
            "    {\"attribute\": \"ATTRIBUTE_NAME\", \"value\": \"VALUE_OR_EMPTY_STRING\"}\n"
            "  ],\n"
            "  \"delete\": [\n"
            "    \"ATTRIBUTE_NAME_TO_DELETE\"\n"
            "  ]\n"
            "}\n\n"
            "If no filter instructions are detected, simply output {}. Do not include any extra text or formatting."
        )


        messages = [
            {"role": "system", "content": filter_prompt},
            {"role": "user", "content": user_message}
        ]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=self.temperature,
            top_p=self.top_p
        )
        filter_text = response.choices[0].message.content
        try:
            instructions = json.loads(filter_text)
        except Exception as e:
            instructions = {}
        self.filter_instruction_cache[user_message] = instructions
        return instructions

    def public_response(self, filter_summary, original_message):
        public_prompt = (
            f"You are a chatbot that helps students filter their courses. "
            f"You have just updated the course filters as follows: {filter_summary}\n"
            f"Based on the student's original input: '{original_message}', please respond in a friendly and helpful tone. "
            f"Clearly indicate which changes you have made (for example, adding a new column for an attribute or removing a filter), "
            f"and ask if the student needs any further adjustments. Additionally, suggest some other filter options they might consider. "
            f"Remember, the available filter attributes are: '', 'available', 'cu', 'prereq', 'labels', and 'mutually exclusive'. "
            f"For 'available', valid values are 'Fall', 'Spring', 'Fall or Spring', an empty string, or 'Not offered every year'. "
            f"For 'cu', valid values are '1 Course Unit' or '0-0.5 Course Units'. "
            f"For 'prereq', the value should follow the format 'CIS' followed by a number (e.g., 'CIS 1200'). "
            f"For 'labels', choose from the provided list of possible labels. "
            f"Based on the context, generate your response, it should not be more than 15-20 words."
        )
        
        messages = [{"role": "system", "content": self.system_prompt}]
        if self.history:
            messages.extend(self.history)
        messages.append({"role": "user", "content": public_prompt})
    
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            stream=False  # disable streaming; get full response text
        )
        full_message = response.choices[0].message.content
        return full_message

    def predict(self, user_message):
        # First, process deletion instructions then addition instructions.
        instructions = self.get_filter_instructions(user_message)
    
        filter_summary = ""
        if "delete" in instructions and instructions["delete"]:
            for attr in instructions["delete"]:
                self.filter_instance.delete_filter(attr)
                filter_summary += f"Deleted filter: {attr}. "
        if "add" in instructions and instructions["add"]:
            for instr in instructions["add"]:
                attribute = instr.get("attribute")
                value = instr.get("value", "")
                if attribute:
                    self.filter_instance.add_filter(attribute, value)
                    filter_summary += f"Added filter: {attribute} contains '{value}'. "
    
        current_state = self.filter_instance.get_current_state()
        current_state_text = json.dumps(current_state, indent=2)
    
        public_resp = self.public_response(filter_summary, user_message)
    
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": filter_summary + "\n" + public_resp})
        self._limit_history()
    
        return public_resp, current_state_text
