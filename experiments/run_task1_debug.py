"""One checkpointed Task 1 debug run. No official submission routes."""
import argparse
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import requests
from experiments.run_researcher_role_diagnostic import make_messages

ROOT=Path(__file__).resolve().parents[1]
BASE='http://f03-iim-lin1.cit-f03.fh-koeln.de/api'
RUN_ID='np-labs-luna-task1-debug-20261005-v1'
OUT=ROOT/'data/official/task1-debug-luna'
CAP=1.0

def build_messages(item):
    r=copy.deepcopy(item)
    assert r.get('conversation_id') and isinstance(r.get('scenario'),dict)
    r['chat_messages']=r.get('chat_messages') or []
    for m in r['chat_messages']:
        role=m.get('participant_name','').lower()
        if role not in ('user','agent','assistant'):raise ValueError('Unknown participant role')
        m['participant_name']='User' if role=='user' else 'Agent'
        if not isinstance(m.get('text'),str):raise ValueError('Missing text')
    if r['chat_messages'] and r['chat_messages'][-1]['participant_name']!='Agent':
        raise ValueError('Prefix does not end with search assistant')
    scenario=r['scenario']; persona=scenario.get('persona') or {}
    scenario['persona']={k:persona.get(k) or {} for k in ('general_info','experience_with_ai','individual_traits')}
    pgi=scenario.get('persona_goal_interaction') or {}
    scenario['persona_goal_interaction']={'domain_familiarity':pgi.get('domain_familiarity'),'known_datasets':pgi.get('known_datasets') or []}
    index=len(r['chat_messages']);r['chat_messages'].append({'participant_name':'User','text':''})
    return make_messages(r,index)

def save(path,data):
    tmp=path.with_suffix('.tmp')
    with tmp.open('w') as f:json.dump(data,f,indent=2);f.flush();os.fsync(f.fileno())
    tmp.replace(path)

def model_payload(messages):
    return {'model':'openai/gpt-6-luna','messages':messages,'stream':False,
            'provider':{'only':['openai'],'allow_fallbacks':False,'max_price':{'prompt':0.1,'completion':0.5},'require_parameters':True,'data_collection':'deny'},
            'max_completion_tokens':4096}

def continue_payload(item,text):
    if not text.strip() or '<think>' in text or '</think>' in text:raise ValueError('Invalid generated text')
    return {'run_id':RUN_ID,'user_utterance':{'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'conversation_id':item['conversation_id'],'participant_name':'user','text':text,'sources':[],'annotations':{},'is_final':False}}

def is_completion(code, body):
    detail=str(body.get("detail", "")).lower()
    return code == 428 and "not exist" not in detail and ("completed" in detail or "run was finished" in detail)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--run',action='store_true');a=parser.parse_args()
    if not a.run:print('Requires --run; only Task 1 debug endpoints are implemented.');return
    os.umask(0o077);OUT.mkdir(parents=True,exist_ok=True)
    statepath=OUT/'state.json';pending=OUT/'inflight.json'
    if pending.exists():raise RuntimeError('Uncertain prior request; reconcile saved state before resuming')
    session=requests.Session();session.headers['Authorization']='Bearer '+(Path.home()/'.config/trec-usersim/organizer.key').read_text().strip()
    modelkey=(Path.home()/'.config/trec-usersim/openrouter.key').read_text().strip()
    def get(path):
        r=session.get(BASE+path,timeout=60,allow_redirects=False)
        if r.status_code!=200:raise RuntimeError('Organizer GET HTTP '+str(r.status_code))
        return r.json()
    assert get('/auth/verify')['team_id']=='NP Labs'
    state=json.loads(statepath.read_text()) if statepath.exists() else {'run_id':RUN_ID,'submitted':0,'spent_usd':0,'reserved_usd':0,'status':'not_started'}
    if state['status']=='complete':print('Already complete');return
    def post(path,payload):
        assert path in ('/task1/debug/start','/task1/debug/continue')
        save(pending,{'path':path,'payload':payload})
        r=session.post(BASE+path,json=payload,timeout=180,allow_redirects=False)
        try:body=r.json()
        except ValueError:body={'detail':'Non-JSON response'}
        save(OUT/'last_http_response.json',{'status':r.status_code,'body':body})
        return r.status_code,body
    if state['status']=='not_started':
        save(OUT/'budget_before.json',get('/budget/check'))
        code,item=post('/task1/debug/start',{'run_id':RUN_ID,'team_id':'NP Labs','task_name':'next_utterance_prediction',
            'description':'Debug only: direct GPT-6 Luna with persona/goal and supplied history, researcher mapped to model assistant; no retrieval or revision.'})
        if code not in (200,201):raise RuntimeError('Debug start HTTP '+str(code))
        build_messages(item)
        state.update(status='running',item=item);save(statepath,state);pending.unlink()
    try:
        while state['submitted']<1000:
            item=state['item'];messages=build_messages(item);payload=model_payload(messages)
            reserve=(len(json.dumps(messages,ensure_ascii=False).encode())+4096)*1e-7+4096*5e-7
            if state['reserved_usd']+reserve>CAP:raise RuntimeError('Conservative model budget cap reached')
            casepath=OUT/f"case-{state['submitted']:04d}.json"
            if casepath.exists():record=json.loads(casepath.read_text());assert record['item']==item
            else:
                save(pending,{'path':'openrouter_chat','case':state['submitted']})
                response=requests.post('https://openrouter.ai/api/v1/chat/completions',json=payload,
                    headers={'Authorization':'Bearer '+modelkey},timeout=180,allow_redirects=False)
                if response.status_code!=200:raise RuntimeError('Model HTTP '+str(response.status_code))
                raw=response.json();record={'item':item,'request':payload,'response':raw,'reserve_usd':reserve};save(casepath,record);pending.unlink()
            raw=record['response'];choice=raw['choices'][0]
            if choice['finish_reason']!='stop':raise RuntimeError('Model did not finish normally')
            text=choice['message']['content'];request=continue_payload(item,text)
            code,body=post('/task1/debug/continue',request)
            # 428 is ambiguous unless body explicitly says completed, after a known active start.
            if code==428:
                if not is_completion(code,body):raise RuntimeError('Ambiguous 428; inspect saved response')
                state['status']='complete'
            elif code in (200,201):build_messages(body);state['item']=body
            else:raise RuntimeError('Debug continue HTTP '+str(code))
            state['submitted']+=1;state['spent_usd']+=raw.get('usage',{}).get('cost',0) or 0
            state['reserved_usd']+=record['reserve_usd'];save(statepath,state);pending.unlink()
            print(json.dumps({k:state[k] for k in ('status','submitted','spent_usd')}),flush=True)
            if state['status']=='complete':save(OUT/'budget_after.json',get('/budget/check'));return
        raise RuntimeError('Turn safety limit reached')
    except Exception as e:
        save(OUT/'error.json',{'type':type(e).__name__,'message':str(e) if isinstance(e,(RuntimeError,ValueError)) else 'Transport or schema error; inspect private checkpoint'})
        raise RuntimeError('Debug runner stopped; inspect private checkpoint') from None

if __name__=='__main__':main()
