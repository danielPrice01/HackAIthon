import os
import json
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai

# Import your existing classes exactly as before
from filter import Filter
from chat_bots.interactive_chat.interactive_chat import InteractiveChatBot
from chat_bots.agentic_swarm.swarm import AgenticSwarm

app = Flask(__name__)

# 1. Load environment variables and set the OpenAI API key
load_dotenv(".env")
openai.api_key = os.environ.get("API_TOKEN")

# 2. Create a global Filter instance (same as in app.py)
filter_instance = Filter("courses/courses.json")

# 3. Instantiate the InteractiveChatBot (mode=1 in your old code)
chatbot = InteractiveChatBot(filter_inst=filter_instance)

# 4. Instantiate the AgenticSwarm (mode=2 in your old code)
swarm = AgenticSwarm(
    "courses/courses.json",
    filter_instance,
    embedding_model="text-embedding-ada-002",
    chat_model="gpt-4-turbo",
    top_k=2
)

@app.route('/interactive_chat', methods=['POST'])
def interactive_chat():
    """
    Equivalent to 'mode=1' in the original code.
    - Accepts JSON with a 'message' field.
    - Passes the message to the InteractiveChatBot.
    - Returns the chatbot's response and the current filter state.
    """
    data = request.json or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "No user message provided"}), 400

    # If you want to preserve the "quit" check from your CLI code, you can do so here:
    if user_message.lower() in ["exit", "quit"]:
        # Up to you how to handle quitting in a web context. 
        # Typically you'd let the frontend handle that.
        return jsonify({"message": "User requested exit"}), 200

    # Same logic as app.py -> mode=1
    public_response, current_state_text = chatbot.predict(user_message)

    # Parse the current filter state (JSON string) into a Python dict
    state = json.loads(current_state_text)

    # Return the chatbot response and the state in JSON
    return jsonify({
        "response": public_response,
        "columns": state.get("columns", []),
        "courses": state.get("courses", [])
    })

@app.route('/agentic_swarm', methods=['POST'])
def agentic_swarm():
    """
    Equivalent to 'mode=2' in the original code.
    - Accepts JSON with a 'query' field.
    - Passes the query to the AgenticSwarm.
    - Returns the swarm results and the current filter state.
    """
    data = request.json or {}
    user_query = data.get('query', '').strip()

    if not user_query:
        return jsonify({"error": "No user query provided"}), 400

    # If you want to preserve the "quit" check from your CLI code, you can do so here:
    if user_query.lower() in ["exit", "quit"]:
        return jsonify({"message": "User requested exit"}), 200

    # The swarm's run_swarm is asynchronous, so we need an event loop to run it
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(swarm.run_swarm(user_query))
    finally:
        loop.close()

    # After the swarm finishes, get the updated filter state
    current_state = filter_instance.get_current_state()

    return jsonify({
        "results": results,
        "columns": current_state.get("columns", []),
        "courses": current_state.get("courses", [])
    })

if __name__ == '__main__':
    # Run Flask on localhost:5000 (or any port you prefer)
    app.run(debug=True, port=5000)