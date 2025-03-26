import asyncio
import openai
import os
from dotenv import load_dotenv
from filter import Filter  # Make sure this path is correct.
from agentic_swarm.swarm import AgenticSwarm  # Adjust import as needed.
from interactive_chat import InteractiveChatBot  # Adjust import as needed.

async def main():
    # Load environment variables and set the API key.
    load_dotenv(".env")
    openai.api_key = os.environ.get("API_TOKEN")
    
    # Create a Filter instance from the courses JSON file.
    filter_instance = Filter("courses/courses.json")
    # Optionally add a filter (for example, filtering courses that require "CIS 2400").
    filter_instance.add_filter("prereq", "CIS 2400")
    
    # Ask the user which mode they would like to use.
    print("Select mode:")
    print("1 - Interactive Chat")
    print("2 - Agentic Swarm")
    mode = input("Enter 1 or 2: ").strip()
    
    if mode == "1":
        # Instantiate InteractiveChatBot with the Filter instance.
        chatbot = InteractiveChatBot(filter_inst=filter_instance)
        user_message = input("Enter your message for the interactive chat: ")
        public_response, current_state_text = chatbot.predict(user_message)
        
        print("\nInteractive Chat Response:")
        print(public_response)
        print("\nCurrent Filter State:")
        print(current_state_text)
    
    elif mode == "2":
        # Instantiate AgenticSwarm with the Filter instance and extra options.
        swarm = AgenticSwarm("courses/courses.json", filter_instance, 
                              embedding_model="text-embedding-ada-002", 
                              chat_model="gpt-4-turbo", top_k=2)
        user_query = input("Enter your query for Agentic Swarm: ")
        results = await swarm.run_swarm(user_query)
        
        print("\nAgentic Swarm Results:")
        for course_id, answer in results.items():
            print(f"Course ID: {course_id} -> Answer: {answer}")
    
    else:
        print("Invalid selection. Please run the program again and choose either 1 or 2.")

if __name__ == "__main__":
    asyncio.run(main())
