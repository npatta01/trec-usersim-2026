"""Pure model-request construction and response validation."""


def model_payload(messages):
    """Return the frozen OpenRouter payload used by the debug baselines."""

    return {
        "model": "openai/gpt-6-luna",
        "messages": messages,
        "stream": False,
        "provider": {
            "only": ["openai"],
            "allow_fallbacks": False,
            "max_price": {"prompt": 0.1, "completion": 0.5},
            "require_parameters": True,
            "data_collection": "deny",
        },
        "max_completion_tokens": 4096,
    }


def validate(raw):
    """Validate and return plain model text using the existing semantics."""

    choice = raw["choices"][0]
    text = choice["message"].get("content")
    if (
        choice["finish_reason"] != "stop"
        or not isinstance(text, str)
        or not text.strip()
        or "<think>" in text
        or "</think>" in text
    ):
        raise RuntimeError("Invalid output; review before resume")
    return text


__all__ = ["model_payload", "validate"]
