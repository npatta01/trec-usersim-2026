"""Validate organizer messages and transitions without network or persistence."""

import copy
import datetime as _dt
import json
from typing import Any


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def same_json(left: Any, right: Any) -> bool:
    return _canonical(left) == _canonical(right)


def utc_timestamp() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _message_role(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Message participant_name must be a string")
    role = value.strip().lower()
    if role == "user":
        return "user"
    if role in {"agent", "assistant"}:
        return "agent"
    raise ValueError("Unknown participant role")


def _validate_scenario(value: Any) -> dict:
    if not isinstance(value, dict) or not isinstance(value.get("goal"), dict):
        raise ValueError("Expected scenario with a goal object")
    return copy.deepcopy(value)


def _validate_message(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValueError("Chat message must be an object")
    role = _message_role(value.get("participant_name"))
    text = value.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Chat message must contain nonempty text")
    # Retain only the semantic fields consumed by the generator.  Timestamps,
    # sources and annotations are organizer metadata and are not history text.
    return {"participant_name": role, "text": text}


def _agent_final(value: Any) -> bool:
    """Read the transport's optional assistant closure marker strictly."""

    return (
        isinstance(value, dict)
        and _message_role(value.get("participant_name")) == "agent"
        and value.get("is_final") is True
    )


def _normalize_history(messages: Any) -> list[dict]:
    if messages is None:
        return []
    if not isinstance(messages, list):
        raise ValueError("chat_messages must be a list")
    normalized = [_validate_message(message) for message in messages]
    expected = "user"
    for message in normalized:
        if message["participant_name"] != expected:
            raise ValueError("Chat history has invalid speaker alternation")
        expected = "agent" if expected == "user" else "user"
    return normalized


def normalize_item(body: Any, *, allow_missing_history: bool = False) -> dict:
    if not isinstance(body, dict):
        raise ValueError("Organizer response must be a JSON object")
    conversation_id = body.get("conversation_id")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise ValueError("Organizer response has no conversation_id")
    scenario = _validate_scenario(body.get("scenario"))
    messages = body.get("chat_messages")
    if messages is None and not allow_missing_history:
        raise ValueError("Organizer response has no chat_messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and "conversation_id" in message:
                if message.get("conversation_id") != conversation_id:
                    raise ValueError(
                        "Chat message conversation_id differs from response"
                    )
    return {
        "conversation_id": conversation_id,
        "scenario": scenario,
        "chat_messages": _normalize_history(messages),
    }


def validate_start_response(status: int, body: Any) -> dict:
    """Validate and normalize a successful debug start response."""

    if status not in (200, 201):
        raise ValueError(f"Unexpected Task 2 debug start HTTP status {status}")
    item = normalize_item(body, allow_missing_history=True)
    if "utterance" in body and body["utterance"] is not None:
        raise ValueError("Start response unexpectedly contains an utterance")
    if item["chat_messages"]:
        raise ValueError("Start response unexpectedly contains history")
    return item


def build_continue_payload(
    run_id: str,
    conversation_id: str,
    text: str,
    is_final: bool,
    *,
    timestamp: str | None = None,
) -> dict:
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("run_id is required")
    if not isinstance(conversation_id, str) or not conversation_id:
        raise ValueError("conversation_id is required")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Generated text must be nonempty")
    if type(is_final) is not bool:
        raise ValueError("is_final must be a boolean")
    if not isinstance(timestamp, str) or not timestamp:
        timestamp = utc_timestamp()
    return {
        "run_id": run_id,
        "user_utterance": {
            "timestamp": timestamp,
            "conversation_id": conversation_id,
            "participant_name": "user",
            "text": text,
            "sources": [],
            "annotations": {},
            "is_final": is_final,
        },
    }


def _expected_history(current: dict, payload: dict) -> list[dict]:
    prior = current.get("chat_messages", [])
    utterance = payload.get("user_utterance", {})
    return prior + [{"participant_name": "user", "text": utterance.get("text", "")}]


def validate_continue_response(
    status: int, body: Any, current: dict, payload: dict
) -> dict:
    """Validate a continue response without silently rewriting organizer history.

    The 200 contract returns the complete history for the active conversation.
    The 201 contract starts a new conversation and must contain no history.  A
    response that omits, duplicates, changes, or relabels prior turns is unsafe
    to feed into the next model call and is rejected.
    """

    current = normalize_item(current)
    if status == 428:
        if not is_completion_for_run(status, body, payload.get("run_id")):
            raise ValueError("428 response is not an explicit completed-run response")
        return {"kind": "complete"}
    if status not in (200, 201):
        raise ValueError(f"Unexpected Task 2 debug continue HTTP status {status}")

    if not isinstance(body, dict):
        raise ValueError("Organizer response must be a JSON object")
    # Live service can return HTTP200 (not documented HTTP201) when it
    # advances to a new empty scenario. Require positive transition evidence;
    # a null reply on the same conversation is never permission to advance.
    if (
        status == 200
        and body.get("conversation_id") != current["conversation_id"]
        and "utterance" in body
        and body["utterance"] is None
    ):
        item = normalize_item(body, allow_missing_history=True)
        if item["chat_messages"]:
            raise ValueError("New conversation unexpectedly contains history")
        return {"kind": "new_conversation", "item": item}
    has_history = "chat_messages" in body
    has_utterance = "utterance" in body
    utterance = None
    if has_utterance and body["utterance"] is not None:
        if _agent_final(body["utterance"]):
            raise ValueError("Assistant is_final requires a 201 scenario transition")
        if not isinstance(body["utterance"], dict):
            raise ValueError("Incremental utterance must be an object")
        utterance_id = body["utterance"].get("conversation_id")
        response_id = body.get("conversation_id")
        if not isinstance(utterance_id, str) or not utterance_id:
            raise ValueError("Incremental utterance has no conversation_id")
        if not isinstance(response_id, str) or utterance_id != response_id:
            raise ValueError(
                "Incremental utterance conversation_id differs from response"
            )
        if status == 200 and utterance_id != current["conversation_id"]:
            raise ValueError("Incremental utterance changed the active conversation ID")
        utterance = _validate_message(body["utterance"])
        if utterance["participant_name"] != "agent":
            raise ValueError("Returned incremental utterance must be an agent turn")
    if status != 201 and not has_history and not has_utterance:
        raise ValueError("Continue response has neither full history nor utterance")
    if status == 201:
        item = normalize_item(body, allow_missing_history=True)
        if item["conversation_id"] == current["conversation_id"]:
            raise ValueError("201 response did not provide a new conversation ID")
        if item["chat_messages"]:
            raise ValueError("201 new conversation unexpectedly contains history")
        if utterance is not None:
            raise ValueError("201 new conversation unexpectedly contains an utterance")
        return {"kind": "new_conversation", "item": item}
    if has_history:
        raw_history = body.get("chat_messages")
        if isinstance(raw_history, list) and any(
            _agent_final(message) for message in raw_history
        ):
            raise ValueError("Assistant is_final requires a 201 scenario transition")
        item = normalize_item(body)
    else:
        # The currently served OpenAPI returns one incremental agent utterance
        # instead of chat_messages.  Reconstruct the full local history from
        # the exact prior item and that one returned turn.
        item = {
            "conversation_id": body.get("conversation_id"),
            "scenario": body.get("scenario"),
            "chat_messages": _expected_history(current, payload) + [utterance],
        }
        item = normalize_item(item)
    if status == 200:
        if payload.get("user_utterance", {}).get("is_final") is True:
            raise ValueError("Final user turn must produce a 201 scenario transition")
        if item["conversation_id"] != current["conversation_id"]:
            raise ValueError("200 response changed the active conversation ID")
        if not same_json(item["scenario"], current["scenario"]):
            raise ValueError("200 response changed the active scenario")
        expected_prefix = _expected_history(current, payload)
        actual = item["chat_messages"]
        if len(actual) != len(expected_prefix) + 1:
            raise ValueError("200 response does not contain exactly one new agent turn")
        if not same_json(actual[:-1], expected_prefix):
            raise ValueError("200 response rewrote, omitted, or duplicated history")
        if actual[-1]["participant_name"] != "agent":
            raise ValueError("200 response does not end with an agent turn")
        if utterance is not None and not same_json(actual[-1], utterance):
            raise ValueError("Incremental utterance conflicts with full history")
        return {"kind": "continue", "item": item}


def is_completion(status: int, body: Any) -> bool:
    """Recognize only the organizer's explicit run-complete 428 response."""

    if status != 428 or not isinstance(body, dict):
        return False
    detail = body.get("detail", "")
    if not isinstance(detail, str):
        return False
    # Unknown prose is not a completion protocol. In particular, substring
    # matches also accept "not completed" and "completed partially".
    return detail.strip().lower().rstrip(".!") in {
        "run was finished",
        "run completed",
    }


def is_completion_for_run(status: int, body: Any, run_id: str) -> bool:
    """Recognize canonical completions or the exact run-bound organizer variant."""

    if not isinstance(run_id, str) or not run_id:
        return False
    return is_completion(status, body) or (
        status == 428
        and body == {
            "detail": f'No more open goals for run "{run_id}". Run was finished!'
        }
    )
