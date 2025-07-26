"""Utility subpackage for emailAgent."""

from .mailer import send_flyer
from .formatter import format_message
from .openai_client import chat_completion, generate_flyer

__all__ = [
    "send_flyer",
    "format_message",
    "chat_completion",
    "generate_flyer",
]
