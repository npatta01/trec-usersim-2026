"""Task 2 prompt/response adapter. Model caller injected; no network or persistence."""

import copy
import json
from usersim.task2.core import Turn, parse_turn, validate_text
from usersim.prompts import build_messages
from usersim.requests import model_payload
from usersim.prompts import editor_messages

STOP_INSTRUCTION = """\n\nThis is an ongoing interaction. Decide what this researcher would say next and whether they would end this conversation now. Use the supplied persona, goal and actual history. They may finish because the available help is sufficient, or abandon an unproductive search. They may continue when something still matters to them. Do not require perfect information, force a fixed number of turns, or keep inventing extra requirements to prolong the search. Do not claim downloads or other external actions you did not observe. Keep the message consistent with the stop decision. Return JSON with exactly "text" (the researcher message) and "is_final" (boolean). Emit no reasoning or extra fields."""
SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "researcher_turn",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"text": {"type": "string"}, "is_final": {"type": "boolean"}},
            "required": ["text", "is_final"],
            "additionalProperties": False,
        },
    },
}


def generate_turn(conversation, call, *, style_postedit=True):
    if conversation.stopped:
        raise ValueError("Cannot generate after stopping")
    original = build_messages(conversation.item())
    messages = copy.deepcopy(original)
    messages[0]["content"] += STOP_INSTRUCTION
    request = model_payload(messages)
    request["response_format"] = copy.deepcopy(SCHEMA)
    draft = parse_turn(call("draft", request))
    if not style_postedit:
        return draft
    edit_messages = editor_messages(original, draft.text)
    edit_messages[0][
        "content"
    ] += " The supplied fixed_is_final decision must not change. If true, preserve closure and do not add a request that expects another reply; if false, preserve continuation. Output only the edited message text, not JSON."
    evidence = json.loads(edit_messages[1]["content"])
    evidence["fixed_is_final"] = draft.is_final
    edit_messages[1]["content"] = json.dumps(evidence, ensure_ascii=False)
    edited = validate_text(call("edit", model_payload(edit_messages)))
    return Turn(edited, draft.is_final)
