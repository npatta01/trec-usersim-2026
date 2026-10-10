"""Optional attributed-rendering experiment; not used by the debug runner."""
from usersim.task2.generator import generate_turn
from usersim.task2.core import Turn
from usersim.prompts import build_messages

def generate_attributed_turn(conversation, call):
    """Opt-in experimental draft, grounded plan, and attributed render path."""
    draft = generate_turn(conversation, call, style_postedit=False)
    from experiments.attributed_renderer import attributed_revision
    evidence_messages = build_messages(conversation.item())
    if not conversation.history:
        # The Task 1 builder adds a synthetic start control for draft generation.
        # It is not an utterance and therefore is not attribution evidence.
        evidence_messages = evidence_messages[:1]
    rendered = attributed_revision(
        evidence_messages, draft.text, draft.is_final, call
    )
    return Turn(rendered, draft.is_final)
