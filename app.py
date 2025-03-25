import os
from dotenv import load_dotenv
import time
import json
import openai
from filter import Filter

load_dotenv()
openai.api_key = os.environ.get("API_TOKEN")

# Global Filter instance (using your courses JSON file)
filter_instance = Filter("courses/courses.json")

def get_filter_instructions(user_message, model, max_tokens, temperature, top_p):
    """
    Calls OpenAI to extract filter instructions from the user's message.
    Expects GPT to return a JSON object with keys "add" and "delete".
    For example, if the user says "I took CIS 1200", GPT should return:
      {"add": [{"attribute": "prereq", "value": "CIS 1200"}], "delete": []}
    If nothing is to be done, an empty JSON object {} is returned.
    """
    filter_prompt = (
        "You are a filter extractor. Given the user's message, "
        "return a JSON object with two keys: 'add' and 'delete'. "
        "'add' should be a list of objects with keys 'attribute' and 'value' "
        "representing filters to add. 'delete' should be a list of attribute names "
        "that should be removed. For example, if the user says 'I took CIS 1200', "
        "return {\"add\": [{\"attribute\": \"prereq\", \"value\": \"CIS 1200\"}], \"delete\": []}. "
        "If no filter instructions are found, return {}."
    )
    messages = [
        {"role": "system", "content": filter_prompt},
        {"role": "user", "content": user_message}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=150,
        temperature=temperature,
        top_p=top_p,
    )
    filter_text = response["choices"][0]["message"]["content"]
    try:
        instructions = json.loads(filter_text)
    except Exception as e:
        print("Warning: Could not parse filter instructions. Received:", filter_text)
        instructions = {}
    return instructions

def public_response(history, filter_summary, original_message, system_prompt, model, max_tokens, temperature, top_p):
    """
    Calls OpenAI to generate a public response after the filter changes have been applied.
    The prompt includes a summary of the filtering actions.
    Returns a generator that yields streaming response chunks.
    """
    public_prompt = (
        f"The following filter changes have been applied: {filter_summary}\n"
        f"Based on your original input: '{original_message}', provide a helpful response."
    )
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": public_prompt})
    
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True  # enable streaming
    )
    full_message = ""
    first_chunk_time = None
    last_yield_time = None
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta and delta.get("content"):
            if first_chunk_time is None:
                first_chunk_time = time.time() - start_time
            full_message += delta["content"]
            current_time = time.time()
            # Print each chunk (or simply yield updates)
            print(delta["content"], end="", flush=True)
            if last_yield_time is None or (current_time - last_yield_time >= 0.25):
                yield full_message
                last_yield_time = current_time
    total_time = time.time() - start_time
    full_message += f" (First chunk: {first_chunk_time:.2f}s, Total: {total_time:.2f}s)"
    yield full_message
    # Return the complete message (if needed)
    return full_message

def predict(user_message, history, system_prompt, model, max_tokens, temperature, top_p):
    """
    Main prediction function.
    
    Step 1: Call GPT to extract filter instructions from the user's message.
            Update the Filter instance accordingly (without printing these instructions).
    Step 2: Call GPT a second time (streaming) to generate a public response that informs the user
            what filter changes have been made and provides further assistance.
    """
    # --- Step 1: Extract filter instructions ---
    instructions = get_filter_instructions(user_message, model, max_tokens, temperature, top_p)
    
    filter_summary = ""
    if "add" in instructions and instructions["add"]:
        for instr in instructions["add"]:
            attribute = instr.get("attribute")
            value = instr.get("value", "")
            if attribute:
                filter_instance.add_filter(attribute, value)
                filter_summary += f"Added filter: {attribute} contains '{value}'. "
    if "delete" in instructions and instructions["delete"]:
        for attr in instructions["delete"]:
            filter_instance.delete_filter(attr)
            filter_summary += f"Deleted filter: {attr}. "
    
    # --- Step 2: Generate public response ---
    # (The first call is not printed; only the second call's output is shown to the user.)
    response_gen = public_response(history, filter_summary, user_message, system_prompt, model, max_tokens, temperature, top_p)
    return response_gen

def main():
    # Set your system prompt and default parameters.
    system_prompt = (
        "You are a helpful assistant that manages course filters based on user input. "
        "You extract filtering instructions (such as courses taken, desired availability, or course units) "
        "and update the course list accordingly. After applying the filters, provide a helpful response."
    )
    history = []
    model = "gpt-4o-mini"  # Change to your desired model
    max_tokens = 2000
    temperature = 0.7
    top_p = 0.95

    print("Welcome to the Course Filter Chat Interface (Command-line version)!")
    print("Type your message and press Enter. Type 'exit' or 'quit' to stop.")
    print("-" * 60)

    while True:
        user_input = input("User: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            break

        print("Assistant: ", end="", flush=True)
        # Get a generator for the public response
        response_generator = predict(user_input, history, system_prompt, model, max_tokens, temperature, top_p)
        full_response = ""
        for chunk in response_generator:
            full_response = chunk  # Update until final chunk is received
        print("\n" + "-" * 60)
        # Update conversation history
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
