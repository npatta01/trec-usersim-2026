"""Experimental native-chat replay; does not modify the organizer strategy."""
import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path
from types import SimpleNamespace

from run_offline_baseline import ROOT, prepare, strategies

ROLE_INSTRUCTION = (
    '\n\nYou are the researcher seeking datasets, not the search assistant. '
    'This research goal belongs to you. In the history below, assistant-role '
    'messages are your past researcher utterances; user-role messages come '
    'from the dataset-search assistant. Write only your next researcher message '
    'reacting to the latest search-assistant reply. Do not write the search '
    "assistant's next answer."
)


def make_messages(record, index):
    scenario, history, last = prepare(record, index)
    captured = []
    def capture(**kwargs):
        captured.extend(dict(m) for m in kwargs['messages'])
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='CAPTURED'))])
    original = strategies.completion
    try:
        strategies.completion = capture
        # Keep the capture call outside ``assert``: optimized Python removes
        # assertions, which would otherwise skip the call and leave no
        # messages to inspect during the dry-run/contract path.
        captured_response = strategies.LLMStrategy().generate_response(
            scenario.persona, history, last, scenario
        )
        assert captured_response == 'CAPTURED'
    finally:
        strategies.completion = original
    prefix = record['chat_messages'][:index]
    if index:
        assert [m['content'] for m in captured[1:]] == [m['text'] for m in prefix]
    else:
        assert len(captured) == 2 and captured[1]['role'] == 'user'
        assert captured[1]['content'] == 'Please start the conversation based on the goal and your persona.'
    captured[0]['content'] += ROLE_INSTRUCTION
    if not index:
        return captured
    for msg in captured[1:]:
        msg['role'] = 'assistant' if msg['role'] == 'user' else 'user'
    assert captured[0]['role'] == 'system'
    assert captured[-1]['role'] == 'user'
    assert [m['role'] for m in captured[1:]] == [
        'assistant' if m['participant_name'].lower() == 'user' else 'user' for m in prefix]
    return captured


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    data = ROOT / 'data/official/final_dataset_curation_v1.jsonl'
    manifest_path = ROOT / 'docs/research/expanded-development-cases.json'
    manifest = json.loads(manifest_path.read_text())
    assert hashlib.sha256(data.read_bytes()).hexdigest() == manifest['dataset_sha256']
    records = [json.loads(line) for line in data.read_text().splitlines()]
    out = ROOT / 'data/official/baseline-runs/expanded-researcher-role.jsonl'
    assert args.dry_run or not out.exists(), 'Refusing to overwrite results'
    for case in manifest['cases']:
        record = records[case['row_1_based'] - 1]
        messages = make_messages(record, case['target_message_index'])
        request = {'model': 'qwen3:8b', 'messages': messages, 'stream': False, 'options': {'seed': 42}}
        start = time.monotonic()
        if not args.dry_run:
            req = urllib.request.Request('http://localhost:11434/api/chat',
                data=json.dumps(request).encode(), headers={'Content-Type': 'application/json'})
            response = json.loads(urllib.request.urlopen(req, timeout=300).read())
            content = response['message'].get('content') or ''
            result = {**case, 'request': request, 'raw_response': response,
                      'seconds': time.monotonic() - start,
                      'dataset_sha256': manifest['dataset_sha256'],
                      'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                      'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'empty': not content.strip(), 'stray_marker': '<think>' in content or '</think>' in content}
            with out.open('a') as f:
                f.write(json.dumps(result) + '\n')
        print(json.dumps({'case': case['case'], 'dry_run': args.dry_run,
                          'seconds': round(time.monotonic() - start, 2)}), flush=True)

if __name__ == '__main__':
    main()
