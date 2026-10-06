"""Pure Task 2 state and rollout mechanics; no model or transport dependencies."""

from dataclasses import dataclass, replace
import json


def validate_text(text):
    if (
        not isinstance(text, str)
        or not text.strip()
        or "<think>" in text
        or "</think>" in text
    ):
        raise ValueError("Expected nonempty plain researcher text")
    return text


@dataclass(frozen=True)
class Turn:
    text: str
    is_final: bool

    def __post_init__(self):
        validate_text(self.text)
        if type(self.is_final) is not bool:
            raise ValueError("is_final must be a boolean")


def parse_turn(text):
    try:
        data = json.loads(text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("Expected JSON turn") from exc
    if not isinstance(data, dict) or set(data) != {"text", "is_final"}:
        raise ValueError("Turn must contain exactly text and is_final")
    return Turn(data["text"], data["is_final"])


@dataclass(frozen=True)
class Conversation:
    conversation_id: str
    scenario_json: str
    history: tuple = ()
    stopped: bool = False

    @classmethod
    def start(cls, conversation_id, scenario):
        if (
            not isinstance(conversation_id, str)
            or not conversation_id
            or not isinstance(scenario, dict)
            or not isinstance(scenario.get("goal"), dict)
        ):
            raise ValueError("Expected conversation ID and scenario with goal")
        return cls(conversation_id, json.dumps(scenario, ensure_ascii=False))

    def item(self):
        return {
            "conversation_id": self.conversation_id,
            "scenario": json.loads(self.scenario_json),
            "chat_messages": [
                {"participant_name": role, "text": text} for role, text in self.history
            ],
        }

    def append_user(self, turn):
        if self.stopped or (self.history and self.history[-1][0] != "agent"):
            raise ValueError("Not an active researcher turn")
        return replace(
            self, history=self.history + (("user", turn.text),), stopped=turn.is_final
        )

    def append_agent(self, text):
        validate_text(text)
        if self.stopped or not self.history or self.history[-1][0] != "user":
            raise ValueError("Not an active search-assistant turn")
        return replace(self, history=self.history + (("agent", text),))


def rollout(conversation, generate, agent, *, max_turns):
    """Callbacks receive current immutable state; operational cutoff is not success."""
    if type(max_turns) is not int or max_turns <= 0:
        raise ValueError("Positive turn limit required")
    if conversation.stopped:
        raise ValueError("Conversation already stopped")
    for count in range(1, max_turns + 1):
        turn = generate(conversation)
        conversation = conversation.append_user(turn)
        if turn.is_final:
            return {
                "conversation": conversation,
                "termination": "user_stop",
                "user_turns": count,
            }
        if count == max_turns:
            return {
                "conversation": conversation,
                "termination": "safety_cutoff",
                "user_turns": count,
            }
        conversation = conversation.append_agent(agent(conversation))
