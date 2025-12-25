#!/usr/bin/env python3
import asyncio
import json
from typing import List, Optional, Union

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mlx_lm import generate, load
from pydantic import BaseModel

app = FastAPI()

# Load model at startup
print("Loading model...")
model, tokenizer = load("mlx-community/Qwen2.5-Coder-14B-Instruct-4bit")
print("Model loaded and ready!")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = 500
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7


class CompletionRequest(BaseModel):
    model: str
    prompt: Union[str, List[str]]
    max_tokens: Optional[int] = 500
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.7


def format_chat_prompt(messages):
    """Format messages using Qwen's chat template"""
    formatted = ""
    for msg in messages:
        if msg.role == "system":
            formatted += f"<|im_start|>system\n{msg.content}<|im_end|>\n"
        elif msg.role == "user":
            formatted += f"<|im_start|>user\n{msg.content}<|im_end|>\n"
        elif msg.role == "assistant":
            formatted += f"<|im_start|>assistant\n{msg.content}<|im_end|>\n"
    formatted += "<|im_start|>assistant\n"
    return formatted


def clean_response(text, prompt):
    """Clean up the generated response"""
    if text.startswith(prompt):
        text = text[len(prompt) :]
    text = text.replace("<|im_end|>", "").replace("<|im_start|>", "").strip()
    return text


async def generate_stream_chat(prompt, max_tokens):
    """Stream generator for chat completions"""
    try:
        # Generate full response
        full_response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)  # noqa: E501

        # Clean response
        full_response = clean_response(full_response, prompt)

        # Stream word by word
        words = full_response.split()
        for i, word in enumerate(words):
            chunk_text = word + (" " if i < len(words) - 1 else "")
            chunk = {
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "created": 0,
                "model": "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": chunk_text},
                        "finish_reason": None,
                    }
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)

        # Final chunk
        final_chunk = {
            "id": "chatcmpl-123",
            "object": "chat.completion.chunk",
            "created": 0,
            "model": "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(final_chunk)}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Streaming error: {e}")


async def generate_stream_completion(prompt, max_tokens):
    """Stream generator for text completions"""
    try:
        full_response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)  # noqa: E501

        # Stream word by word
        words = full_response.split()
        for i, word in enumerate(words):
            chunk_text = word + (" " if i < len(words) - 1 else "")
            chunk = {
                "id": "cmpl-123",
                "object": "text_completion",
                "created": 0,
                "model": "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
                "choices": [{"text": chunk_text, "index": 0, "finish_reason": None}],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)

        yield "data: [DONE]\n\n"
    except Exception as e:
        print(f"Streaming error: {e}")


@app.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    prompt = format_chat_prompt(request.messages)

    if request.stream:
        return StreamingResponse(
            generate_stream_chat(prompt, request.max_tokens),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    # Non-streaming
    response = generate(model, tokenizer, prompt=prompt, max_tokens=request.max_tokens, verbose=False)  # noqa: E501
    response = clean_response(response, prompt)

    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 0,
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": response},
                "finish_reason": "stop",
            }
        ],
    }


@app.post("/v1/completions")
async def completion(request: CompletionRequest):
    """Text completion endpoint for Continue inline edits"""
    prompt = request.prompt if isinstance(request.prompt, str) else request.prompt[0]

    if request.stream:
        return StreamingResponse(
            generate_stream_completion(prompt, request.max_tokens),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    # Non-streaming
    response = generate(model, tokenizer, prompt=prompt, max_tokens=request.max_tokens, verbose=False)  # noqa: E501

    return {
        "id": "cmpl-123",
        "object": "text_completion",
        "created": 0,
        "model": request.model,
        "choices": [{"text": response, "index": 0, "finish_reason": "stop"}],
    }


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
                "object": "model",
                "created": 0,
                "owned_by": "local",
            }
        ],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
