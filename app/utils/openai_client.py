"""Utility for interacting with OpenAI's API."""

import openai


def chat_completion(messages, model="gpt-3.5-turbo", **kwargs):
    """Send a chat completion request."""
    response = openai.ChatCompletion.create(model=model, messages=messages, **kwargs)
    return response
