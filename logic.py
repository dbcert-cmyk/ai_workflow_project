import ollama  # Add this line

def get_pulse(thought):
    response = ollama.qwen2.5_coder_7b(thought)
    return {
        'question': thought,
        'answer': response
    }
