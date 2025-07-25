"""Utility for interacting with OpenAI's API."""

import json
import openai
from openai import OpenAIError


def chat_completion(messages, model="gpt-3.5-turbo", **kwargs):
    """Send a chat completion request.

    Parameters
    ----------
    messages : list
        Chat messages to send to the API.
    model : str, optional
        The model name to use.

    Returns
    -------
    Any
        The API response object.

    Raises
    ------
    RuntimeError
        If the OpenAI API request fails.
    """
    try:
        return openai.ChatCompletion.create(model=model, messages=messages, **kwargs)
    except OpenAIError as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc}") from exc


def generate_flyer(data: dict) -> dict:
    """Generate an email flyer using OpenAI's ChatCompletion API.

    The input ``data`` dictionary should contain the keys ``address``, ``price``,
    ``features``, ``agent_name``, ``agent_phone`` and ``agent_email``. The
    function requests ``gpt-3.5-turbo`` to craft a short subject line and an
    HTML formatted email using those values.

    Parameters
    ----------
    data: dict
        Property and agent information.

    Returns
    -------
    dict
        A dictionary with ``subject`` and ``html_body`` keys containing the
        generated text.
    """

    address = data.get("address", "")
    price = data.get("price", "")
    features = data.get("features", [])
    agent_name = data.get("agent_name", "")
    agent_phone = data.get("agent_phone", "")
    agent_email = data.get("agent_email", "")

    bullet_features = "\n".join(f"- {feat}" for feat in features)

    prompt = (
        f"Create a property listing email flyer.\n"
        f"Address: {address}\n"
        f"Price: {price}\n\n"
        f"Key features:\n{bullet_features}\n\n"
        f"Agent Name: {agent_name}\n"
        f"Agent Phone: {agent_phone}\n"
        f"Agent Email: {agent_email}\n\n"
        "The email body should be HTML and include the address and price, a "
        "bulleted list of 3-5 key features, a short paragraph inviting other "
        "agents to schedule a showing, and the listing agent's contact "
        "information. Return a JSON object with keys 'subject' and 'html_body'."
    )

    messages = [{"role": "user", "content": prompt}]

    try:
        response = chat_completion(messages)
    except RuntimeError:
        # Propagate API errors to the caller
        raise

    content = response["choices"][0]["message"]["content"]

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"subject": "", "html_body": content}

    return result
