"""Synthetic receipt accounting; no keys, transcripts or API calls."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.evidence.submissions import build_index, money
from tools.evidence.archive import archive


class SubmissionEvidenceTest(unittest.TestCase):
    def test_float_residue_does_not_report_negative_zero_cost(self):
        self.assertEqual(money('-0.000000000000000003'), '0.000000000')
        self.assertEqual(money('0.001656160'), '0.001656160')

    def test_receipts_include_calls_missing_from_checkpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source'
            run = source / 'example'
            (run / 'model').mkdir(parents=True)
            (run / 'state.json').write_text(json.dumps({
                'run_id': 'synthetic', 'status': 'halted', 'model_calls': 1,
                'spent_usd': 0.001, 'total_user_turns': 1}))
            for i in range(2):
                (run / 'model' / f'call-{i}.json').write_text(json.dumps({
                    'request': {'model': 'synthetic', 'max_completion_tokens': 10},
                    'response': {'usage': {'cost': 0.001}}}))
            snapshot = root / 'snapshot'
            archive({'synthetic-runs': source}, snapshot)
            spec = ((2, 'debug', 'synthetic-runs', 'example', 'synthetic', 'halted'),)
            with patch('tools.evidence.submissions.RUNS', spec):
                result = build_index(snapshot)
            record = result['runs'][0]
            self.assertEqual(record['model_call_receipts'], 2)
            self.assertEqual(record['checkpoint_model_calls'], 1)
            self.assertEqual(record['model_receipt_cost_usd'], '0.002000000')
            self.assertEqual(record['receipt_minus_checkpoint_cost_usd'], '0.001000000')
            self.assertIsNone(record['official_evaluation_score'])
            public = json.dumps(result)
            self.assertNotIn('response', public)
            self.assertNotIn('sources', result)


if __name__ == '__main__':
    unittest.main()
