"""Synthetic controls for the live run-bound completion contract."""
import json
import tempfile
import unittest
from pathlib import Path
from usersim.task2.debug import Task2DebugRunner
from usersim.task2.protocol import build_continue_payload,validate_continue_response
from usersim.task2.recovery import run_with_recovery
from test_task2_debug_runner import start_body


def finished(run_id):
    return {'detail':f'No more open goals for run "{run_id}". Run was finished!'}


def final_model(request):
    text=json.dumps({'text':'Done.','is_final':True}) if request.get('response_format') else 'Done.'
    return 200,{'choices':[{'finish_reason':'stop','message':{'content':text}}],'usage':{'cost':0.001}}


class RunCompletionTests(unittest.TestCase):
    def test_exact_run_bound_completion(self):
        payload=build_continue_payload('run','c1','Done.',True)
        self.assertEqual(validate_continue_response(428,finished('run'),start_body(),payload),{'kind':'complete'})

    def test_wrong_run_extended_or_unfinished_messages_block(self):
        payload=build_continue_payload('run','c1','Done.',True)
        for body,status in [(finished('wrong'),428),({**finished('run'),'other':True},428),({'detail':'Prefix '+finished('run')['detail']},428),({'detail':finished('run')['detail']+' suffix'},428),({'detail':'Run not completed'},428),(finished('run'),500)]:
            with self.subTest(body=body,status=status),self.assertRaises(ValueError):
                validate_continue_response(status,body,start_body(),payload)

    def test_final_transition_and_completed_resume_make_no_new_calls(self):
        with tempfile.TemporaryDirectory() as td:
            calls=[];model_calls=[]
            def post(path,payload):
                calls.append(path)
                return (200,start_body()) if path.endswith('/start') else (428,finished('run'))
            def model(request):
                model_calls.append(request);return final_model(request)
            runner=Task2DebugRunner(Path(td),run_id='run',organizer_post=post,model_post=model,source_files=[])
            state=run_with_recovery(runner,lambda:self.fail('Unexpected recovery GET'))
            self.assertEqual((state['status'],state['completed_conversations'],state['user_stops'],state['total_user_turns']),('complete',1,1,1))
            self.assertEqual(state.get('skipped_conversations',0),0)
            self.assertEqual(len(calls),2);self.assertEqual(len(model_calls),2)
            self.assertEqual(run_with_recovery(runner,lambda:self.fail('Unexpected GET')),state)
            self.assertEqual(len(calls),2);self.assertEqual(len(model_calls),2)

    def test_unclassified_protocol_error_retains_original_exception(self):
        with tempfile.TemporaryDirectory() as td:
            calls=[]
            def post(path,payload):
                calls.append(path)
                return (200,start_body()) if path.endswith('/start') else (428,{'detail':'Unknown completion'})
            runner=Task2DebugRunner(Path(td),run_id='run',organizer_post=post,model_post=final_model,source_files=[])
            with self.assertRaisesRegex(ValueError,'not an explicit completed-run response'):
                run_with_recovery(runner,lambda:self.fail('Unexpected recovery GET'))
            self.assertEqual(calls,['/task2/debug/start','/task2/debug/continue'])
            self.assertEqual(runner._load_state()['status'],'halted')


if __name__=='__main__':unittest.main()
