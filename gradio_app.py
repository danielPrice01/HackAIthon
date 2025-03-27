import gradio as gr
import pandas as pd
from dotenv import load_dotenv
import os
import json
import openai
import asyncio

from filter import Filter
from chat_bots.interactive_chat.interactive_chat import InteractiveChatBot
from chat_bots.agentic_swarm.swarm import AgenticSwarm

# Load environment variables and set API key
load_dotenv(".env")
openai.api_key = os.environ.get("API_TOKEN")

# Initialize global instances
filter_instance = Filter("courses/courses.json")
chatbot = InteractiveChatBot(filter_inst=filter_instance)
agentic_swarm = AgenticSwarm("courses/courses.json", filter_instance,
                             embedding_model="text-embedding-ada-002", 
                             chat_model="gpt-4-turbo", top_k=2)

def get_course_table():
    """
    Retrieve the current course table as a pandas DataFrame.
    Reads the current state from the Filter instance and excludes the 'labels' column.
    """
    state = filter_instance.get_current_state()
    headers = state.get("columns", [])
    courses = state.get("courses", [])

    # Exclude the "labels" column
    headers = [h for h in headers if h != "labels"]
    
    if courses:
        df = pd.DataFrame(courses)
        if headers:
            # Reorder columns according to the headers list
            df = df[headers]
        
        # Rename columns according to the mapping
        column_mapping = {
            'id': 'Course',
            'name': 'Name',
            'prereq': 'Prerequisite(s)',
            'available': 'Term',
            'swarm_answer': 'AI Attribute'
        }
        df = df.rename(columns=column_mapping)
    else:
        df = pd.DataFrame()
    return df

async def process_chat_message(chat_history, user_message, mode):
    """
    Process the user message:
    - Depending on the selected mode, use either the InteractiveChatBot or AgenticSwarm.
    - Append the exchange as (user_message, bot_response) to the chat history.
    - Update and return both the chat history and the course table.
    """
    if chat_history is None:
        chat_history = []
    
    if mode == "Filter":
        public_response, _ = chatbot.predict(user_message)
    elif mode == "Generate Attribute":
        if len(get_course_table()) < 15:
            await agentic_swarm.run_swarm(user_message)
            public_response = "Done! Check the table for your results."
        else:
            public_response = "More than 15 courses are currently selected! Please narrow down your course list before using Agentic Swarm mode."
    else:
        public_response = "Unknown mode selected."

    # Append the conversation as dictionaries
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": public_response})
    
    # Update the course table view
    updated_table = get_course_table()
    
    return chat_history, updated_table, ""

with gr.Blocks() as demo:
    # Title and description at the top
    gr.Markdown(
        """
        # Ask @ Penn 
    
        ## Find the right course, quickly.
        """
    )
    
    with gr.Row():
        # Left column: Course table view (wider)
        with gr.Column(scale=3):
            course_table = gr.Dataframe(value=get_course_table(), interactive=False, wrap=True, elem_id="course_table")
        
        # Right column: Chat panel (narrower)
        with gr.Column(scale=1):
            # Mode selection toggle
            mode_selector = gr.Radio(choices=["Filter", "Generate Attribute"], label="Select Mode", value="Filter")
            chatbot_ui = gr.Chatbot(label="Chatbot", type="messages")
            # Textbox: press Enter to submit and auto-clear on submit.
            user_input = gr.Textbox(
                placeholder="I want to take...",
                label="Your prompt"
            )
            send_btn = gr.Button("Send")
    
    # Wire up the callback for both button click and Enter submit.
    send_btn.click(
        fn=process_chat_message, 
        inputs=[chatbot_ui, user_input, mode_selector], 
        outputs=[chatbot_ui, course_table, user_input]
    )
    
    user_input.submit(
        fn=process_chat_message, 
        inputs=[chatbot_ui, user_input, mode_selector], 
        outputs=[chatbot_ui, course_table, user_input]
    )

    # Inject custom CSS for the table styling
    # gr.HTML(
    #     """
    #     <style>
    #     /* Fix the 'Course' column width and allow text wrapping */
    #     #course_table table th:nth-child(1),
    #     #course_table table td:nth-child(1) {
    #         width: 100px;
    #         white-space: normal;
    #         word-wrap: break-word;
    #     }
    #     </style>
    #     """
    # )
    
# Launch the Gradio app.
demo.launch()