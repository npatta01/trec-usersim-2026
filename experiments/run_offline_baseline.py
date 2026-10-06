"""Offline replay of the unchanged organizer LLMStrategy; private outputs only."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from simulator.src import response_strategies as strategies
from simulator.src.scenario import (Goal, Persona, PersonaGeneralInfo, PersonaExperience,
                                   PersonaTraits, PersonaGoalInteraction, Scenario)


def prepare(record, index):
    raw = record['scenario']
    p = raw['persona']
    scenario = Scenario(
        goal=Goal(**{k: raw['goal'].get(k) for k in ('context', 'topic', 'discipline')}),
        persona=Persona(PersonaGeneralInfo(**(p.get('general_info') or {})),
                        PersonaExperience(**(p.get('experience_with_ai') or {})),
                        PersonaTraits(**(p.get('individual_traits') or {}))),
        persona_goal_interaction=PersonaGoalInteraction(**raw['persona_goal_interaction']))
    assert record['chat_messages'][index]['participant_name'].lower() == 'user'
    prefix = record['chat_messages'][:index]
    history = [{'role': 'user' if m['participant_name'].lower() == 'user' else 'assistant',
                'content': m['text']} for m in prefix]
    # Strategy appends the latest agent reply itself: pass it exactly once.
    last = history.pop()['content'] if history else ''
    return scenario, history, last


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='ollama/qwen3:0.6b')
    parser.add_argument('--limit', type=int, default=20)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    dataset = ROOT / 'data/official/final_dataset_curation_v1.jsonl'
    records = [json.loads(line) for line in dataset.read_text().splitlines()]
    manifest = json.loads((ROOT / 'docs/research/baseline-development-cases.json').read_text())
    assert hashlib.sha256(dataset.read_bytes()).hexdigest() == manifest['dataset_sha256']
    cases = manifest['cases'][:args.limit]
    out = ROOT / 'data/official/baseline-runs' / (args.model.replace('/', '_').replace(':', '_') + '.jsonl')
    assert not out.exists() or args.dry_run, 'Refusing to overwrite an existing run'
    real_completion = strategies.completion
    strategy = strategies.LLMStrategy(model=args.model)
    for case in cases:
        record = records[case['row_1_based'] - 1]
        scenario, history, last = prepare(record, case['target_message_index'])
        capture = {}
        def complete(**kwargs):
            capture['messages'] = kwargs['messages']
            expected = record['chat_messages'][:case['target_message_index']]
            actual = kwargs['messages'][1:]
            if expected:
                assert [m['content'] for m in actual] == [m['text'] for m in expected]
                assert [m['role'] for m in actual] == ['user' if m['participant_name'].lower() == 'user' else 'assistant' for m in expected]
            else:
                assert len(actual) == 1 and 'Please start' in actual[0]['content']
            if args.dry_run:
                from types import SimpleNamespace
                return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='DRY_RUN'))])
            response = real_completion(**kwargs)
            capture['response'] = response.model_dump()
            return response
        strategies.completion = complete
        started = time.monotonic()
        output = strategy.generate_response(scenario.persona, history, last, scenario)
        if args.dry_run:
            assert output == 'DRY_RUN', 'Input-integrity check failed inside strategy'
        if not args.dry_run:
            result = {'case': case['case'], 'row': case['row_1_based'],
                      'target_index': case['target_message_index'], 'model': args.model,
                      'seconds': time.monotonic() - started, 'output': output,
                      'dataset_sha256': hashlib.sha256(dataset.read_bytes()).hexdigest(),
                      'strategy_sha256': hashlib.sha256(Path(strategies.__file__).read_bytes()).hexdigest(),
                      'success': 'response' in capture, **capture}
            with out.open('a') as f:
                f.write(json.dumps(result) + '\n')
            if not result['success']:
                raise RuntimeError('Model call failed; fallback recorded as failure, not a prediction')
        print(json.dumps({'case': case['case'], 'dry_run': args.dry_run, 'seconds': round(time.monotonic()-started, 2)}), flush=True)

if __name__ == '__main__':
    main()
