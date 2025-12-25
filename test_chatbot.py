import os
from openai import OpenAI

# Configuration based on your confirmed working setup:
MODEL_ID = "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit"
BASE_URL = "http://localhost:8080/v1"

# Initialize the client
client = OpenAI(
    api_key="not-needed", 
    base_url=BASE_URL
)

# Initialize message history
messages = [
    {"role": "system", "content": "You are a helpful, brief, and friendly local AI assistant."}
]

print(f"--- Qwen Coder Chatbot ({MODEL_ID}) ---")
print(f"Connected to: {BASE_URL}")
print("Type 'quit' or 'exit' to end the chat.")
print("-" * 40)

def chat_loop():
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Chatbot closing. Goodbye!")
            break
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        try:
            # Send the entire message history (NO STREAMING)
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                stream=False,  # Changed from True
                max_tokens=500
            )
            
            # Get the response content
            full_response = response.choices[0].message.content
            
            # Print the response
            print(f"Qwen: {full_response}")

            # Add model response to history for context in the next turn
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"\n\nAn API error occurred. Is your PM2 server running? Error: {e}")
            # Remove the last user message to prevent loop in error
            messages.pop()

# Start the chat loop
chat_loop()
