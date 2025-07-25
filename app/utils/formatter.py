"""Simple helper to format chat messages."""


def format_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}
