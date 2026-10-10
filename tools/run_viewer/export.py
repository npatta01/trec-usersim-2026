"""Read-only, offline projection of saved UserSim receipts for a private viewer."""

import base64
import copy
import hashlib
import json
import re
from pathlib import Path

ASSETS = Path(__file__).parent
REQUEST_FIELDS = {
    'model', 'messages', 'stream', 'provider', 'max_completion_tokens',
    'response_format', 'temperature', 'seed', 'reasoning_effort',
}
SECRET = re.compile(
    r'sk-or-v1-[A-Za-z0-9]{20,}|\bsk-[A-Za-z0-9_-]{20,}|'
    r'gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN [^-]*PRIVATE KEY-----|'
    r'Bearer\s+[A-Za-z0-9._-]{20,}', re.IGNORECASE
)


def deny_auth_fields(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in {'authorization', 'api_key', 'access_token', 'secret', 'headers', 'password', 'credentials'}:
                raise ValueError('Authentication-like field detected; refuse export')
            deny_auth_fields(item)
    elif isinstance(value, list):
        for item in value:
            deny_auth_fields(item)


def read(path):
    return json.loads(path.read_text())


def model_call(path):
    receipt = read(path)
    request = receipt['request']
    deny_auth_fields(request)
    if set(request) - REQUEST_FIELDS:
        raise ValueError('Unknown model request fields; inspect before exporting')
    response = receipt['response']
    choice = response['choices'][0]
    content = choice['message']['content']
    if not isinstance(content, str):
        raise ValueError('Expected a text model response')
    usage = response.get('usage') or {}
    return {
        'request': copy.deepcopy(request), 'output': content,
        'finish_reason': choice.get('finish_reason'),
        'usage': {k: usage[k] for k in ('prompt_tokens', 'completion_tokens', 'cost') if k in usage},
        'request_sha256': receipt.get('request_sha256'),
    }


def turn(run, key, item, incoming, submitted, receipt):
    draft = model_call(run / 'model' / f'{key}-draft.json')
    edit = model_call(run / 'model' / f'{key}-edit.json')
    utterance = submitted['user_utterance']
    if edit['output'].strip() != utterance['text']:
        raise ValueError(f'Editor/submission mismatch: {key}')
    if key.startswith('turn-'):
        parsed = json.loads(draft['output'])
        if parsed['is_final'] is not utterance['is_final']:
            raise ValueError(f'Stop mismatch: {key}')
    return {
        'id': key, 'input': copy.deepcopy(item),
        'organizer_input': copy.deepcopy(incoming), 'draft': draft, 'edit': edit,
        'submitted': copy.deepcopy(utterance),
        'submission_payload': copy.deepcopy(submitted),
        'receipt': {'status': receipt['status'], 'body': copy.deepcopy(receipt['body'])},
    }


def task1(run):
    cases = []
    for path in sorted(run.glob('case-[0-9][0-9][0-9][0-9].json')):
        case = read(path)
        key = path.stem
        n = int(key.split('-')[1])
        receipt = read(run / 'organizer' / f'continue-{n:04d}.json')
        if receipt['payload'] != case['submission_request']:
            raise ValueError(f'Case/receipt mismatch: {key}')
        t = turn(run, key, case['item'], case['item'], case['submission_request'], receipt)
        if t['edit']['output'].strip() != case['selected'] or t['draft']['output'].strip() != case['draft']:
            raise ValueError(f'Case/model mismatch: {key}')
        history = case['item'].get('chat_messages') or []
        cases.append({'id': key, 'title': f'Case {n+1} · '+('Opening' if not history else f'{len(history)} preceding messages'),
                      'complete': False, 'turns': [t]})
    if not cases:
        raise ValueError('No Task 1 cases found')
    return {'task': 1, 'label': 'Task 1 · official', 'run': run.name,
            'note': 'Independent supplied prefixes. These predictions do not form one generated conversation.',
            'conversations': cases}


def task2(run, ordinal):
    """Export one ordinary, complete conversation; refuse gaps in its evidence."""
    groups = {}
    for path in sorted((run / 'organizer').glob('continue-[0-9][0-9][0-9][0-9].json')):
        receipt = read(path)
        cid = receipt['payload']['user_utterance']['conversation_id']
        groups.setdefault(cid, []).append((path, receipt))
    if ordinal > len(groups):
        raise ValueError('Requested conversation not available')
    cid, receipts = list(groups.items())[ordinal - 1]
    first = int(receipts[0][0].stem.split('-')[1])
    previous = run / 'organizer' / ('start.json' if first == 0 else f'continue-{first-1:04d}.json')
    prior = read(previous)
    if prior['status'] not in (200, 201):
        raise ValueError('Fresh-conversation input has no successful receipt')
    incoming = prior['body']
    if incoming.get('conversation_id') != cid or incoming.get('utterance') is not None or incoming.get('chat_messages'):
        raise ValueError('No verified fresh-conversation input')
    scenario = incoming['scenario']
    turns, history = [], []
    for offset, (path, receipt) in enumerate(receipts):
        n = int(path.stem.split('-')[1])
        if n != first + offset or receipt['status'] not in (200, 201):
            raise ValueError('Missing/error receipt within selected conversation')
        submitted = receipt['payload']
        utterance = submitted['user_utterance']
        item = {'conversation_id': cid, 'scenario': scenario, 'chat_messages': copy.deepcopy(history)}
        t = turn(run, f'turn-{n:04d}', item, incoming, submitted, receipt)
        messages = t['draft']['request']['messages'][1:]
        expected_messages = [{'role': 'assistant' if m['participant_name'].lower()=='user' else 'user',
                              'content': m['text']} for m in history]
        if history and messages != expected_messages:
            raise ValueError('Reconstructed history differs from the recorded model request')
        turns.append(t)
        history.append(copy.deepcopy(utterance))
        incoming = receipt['body']
        if offset == len(receipts) - 1:
            if (not incoming.get('conversation_id') or incoming.get('conversation_id') == cid
                    or utterance['is_final'] is not True
                    or not isinstance(incoming.get('scenario'), dict)
                    or incoming.get('utterance') is not None or incoming.get('chat_messages')):
                raise ValueError('Selected conversation did not end naturally with a new scenario')
        else:
            reply = incoming.get('utterance')
            if incoming.get('conversation_id') != cid or not isinstance(reply, dict) or reply.get('conversation_id') != cid:
                raise ValueError('Missing same-conversation assistant reply')
            history.append(copy.deepcopy(reply))
    return {'task': 2, 'label': 'Task 2 · official', 'run': run.name,
            'note': 'One complete saved conversation, from opening to a natural researcher stop. Not a quality score.',
            'conversations': [{'id': f'conversation-{ordinal:02d}',
                               'title': f'Conversation {ordinal} · {len(turns)} researcher turns',
                               'complete': True, 'turns': turns}]}


def render(data, output):
    """Bundle only normalized evidence and local assets; no fetches or credentials."""
    deny_auth_fields(data)
    encoded = json.dumps(data, ensure_ascii=False)
    if SECRET.search(encoded):
        raise ValueError('Credential-like material detected; no HTML written')
    encoded = (encoded.replace('&', '\\u0026').replace('<', '\\u003c')
               .replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))
    css = (ASSETS / 'viewer.css').read_text()
    js = (ASSETS / 'viewer.js').read_text()
    def digest(text):
        return base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()
    policy = (f"default-src 'none'; script-src 'sha256-{digest(js)}'; style-src 'sha256-{digest(css)}'; "
              "img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'")
    html = (ASSETS / 'viewer.html').read_text()
    for key, value in [('__CSP__', policy), ('__CSS__', css), ('__JS__', js), ('__DATA__', encoded)]:
        html = html.replace(key, value)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)
