import asyncio
import json
import os
from dotenv import load_dotenv
import openai
from filter import Filter
from chat_bots.interactive_chat.interactive_chat import InteractiveChatBot
from chat_bots.agentic_swarm.swarm import AgenticSwarm

async def main():
    # Load environment variables and set API key.
    load_dotenv(".env")
    openai.api_key = os.environ.get("API_TOKEN")
    
    # Create a Filter instance.
    filter_instance = Filter("courses/courses.json")
    
    while True:
        print("Select mode:")
        print("1 - Interactive Chat")
        print("2 - Agentic Swarm")
        mode = input("Enter 1 or 2 (or type 'quit' to exit): ").strip()
        if mode.lower() in ["quit", "exit"]:
            break

        if mode == "1":
            # Instantiate InteractiveChatBot with the Filter instance.
            chatbot = InteractiveChatBot(filter_inst=filter_instance)
            user_message = input("Enter your message for the interactive chat: ")
            if user_message.strip().lower() in ["exit", "quit"]:
                break
            public_response, current_state_text = chatbot.predict(user_message)
            
            print("\nInteractive Chat Response:")
            print(public_response)
            print("\nCurrent Filter State:")
            state = json.loads(current_state_text)
            headers = state.get("columns", [])
            courses = state.get("courses", [])
            print("Columns:", headers)
            for course in courses:
                row = [course.get(col, "") for col in headers]
                print(row)
            print("-" * 60)
        
        elif mode == "2":
            # Instantiate AgenticSwarm with the Filter instance and extra options.
            swarm = AgenticSwarm("courses/courses.json", filter_instance,
                                  embedding_model="text-embedding-ada-002", 
                                  chat_model="gpt-4-turbo", top_k=2)
            user_query = input("Enter your query for Agentic Swarm: ")
            if user_query.strip().lower() in ["exit", "quit"]:
                break
            results = await swarm.run_swarm(user_query)
            
            print("\nAgentic Swarm Results:")
            for course_id, answer in results.items():
                print(f"Course ID: {course_id} -> Answer: {answer}")
            
            current_state = filter_instance.get_current_state()
            print("\nCurrent Filter State:")
            headers = current_state.get("columns", [])
            courses = current_state.get("courses", [])
            print("Columns:", headers)
            for course in courses:
                row = [course.get(col, "") for col in headers]
                print(row)
            print("-" * 60)
        
        else:
            print("Invalid selection. Please choose either 1 or 2.\n")

if __name__ == "__main__":
    asyncio.run(main())
