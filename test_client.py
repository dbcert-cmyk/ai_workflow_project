from openai import OpenAI

# 1. Initialize the client to talk to your local MLX server
# base_url must include the /v1 path as confirmed by logs
client = OpenAI(api_key="not-needed", base_url="http://localhost:8080/v1")

# 2. Define the exact model ID used by your MLX server
MODEL_ID = "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit"

print(f"Connecting to {client.base_url} using model {MODEL_ID}...")
print("-" * 30)

try:
    # 3. Request a streamed chat completion
    stream = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": "Write a single-paragraph explanation of why local LLMs are useful for developers.",
            }
        ],
        stream=True,
    )

    # 4. Print the streamed response token by token
    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_response += content

except Exception as e:
    print(f"\n\nAn error occurred: {e}")

print("\n\n--- Finished ---")
