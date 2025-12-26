import ollama


def get_pulse(thought: str) -> dict:
    """
    Fetches a response from the local Ollama model.
    """
    try:
        response = ollama.chat(
            model='qwen2.5-coder:7b',
            messages=[{'role': 'user', 'content': thought}]
        )
        return {
            'question': thought,
            'answer': response['message']['content']
        }
    except Exception as e:
        return {
            'question': thought,
            'answer': f"Error: {e}"
        }
