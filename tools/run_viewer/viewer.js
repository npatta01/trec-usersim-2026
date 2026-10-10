(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('viewer-data').textContent);
  const $ = id => document.getElementById(id);
  const el = (tag, text, className) => { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (className) n.className = className; return n; };
  const pretty = value => JSON.stringify(value, null, 2);
  const label = key => key.replaceAll('_', ' ');
  // All recorded material is inert. Never use innerHTML, eval, external embeds or images.
  function inline(text, parent) {
    const pattern = /\*\*([^*]+)\*\*|`([^`]+)`|\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
    let last = 0, match;
    while ((match = pattern.exec(text))) {
      parent.append(document.createTextNode(text.slice(last, match.index)));
      if (match[1]) parent.append(el('strong', match[1]));
      else if (match[2]) parent.append(el('code', match[2]));
      else { const a = el('a', match[3]); a.href = match[4]; a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a); }
      last = pattern.lastIndex;
    }
    parent.append(document.createTextNode(text.slice(last)));
  }
  function markdown(text) {
    const root = el('div', undefined, 'markdown');
    const lines = String(text ?? '').replaceAll('\r\n', '\n').split('\n');
    let i = 0;
    while (i < lines.length) {
      if (!lines[i].trim()) { i++; continue; }
      if (/^```/.test(lines[i])) {
        const code = []; i++; while (i < lines.length && !/^```/.test(lines[i])) code.push(lines[i++]); i++;
        const pre = el('pre'); pre.append(el('code', code.join('\n'))); root.append(pre); continue;
      }
      const heading = lines[i].match(/^#{1,6}\s+(.+)/);
      if (heading) { const h = el('h4'); inline(heading[1], h); root.append(h); i++; continue; }
      if (i+1 < lines.length && lines[i].includes('|') && /^\s*\|?[ :|-]+\|[ :|-]*$/.test(lines[i+1])) {
        const table = el('table'), wrap = el('div', undefined, 'table-wrap'); let head = true;
        while (i < lines.length && lines[i].includes('|') && lines[i].trim()) {
          const line = lines[i++]; if (/^\s*\|?[ :|-]+\|[ :|-]*$/.test(line)) continue;
          const tr = el('tr'); line.replace(/^\s*\||\|\s*$/g, '').split('|').forEach(cell => { const td = el(head?'th':'td'); inline(cell.trim(),td); tr.append(td); });
          table.append(tr); head = false;
        } wrap.append(table); root.append(wrap); continue;
      }
      if (/^\s*(?:[-*+] |\d+[.)] )/.test(lines[i])) {
        const list = el(/^\s*\d/.test(lines[i]) ? 'ol' : 'ul');
        while (i < lines.length && /^\s*(?:[-*+] |\d+[.)] )/.test(lines[i])) { const li = el('li'); inline(lines[i++].replace(/^\s*(?:[-*+] |\d+[.)] )/,''),li); list.append(li); }
        root.append(list); continue;
      }
      const parts = [lines[i++]];
      while (i < lines.length && lines[i].trim() && !/^(?:```|#{1,6}\s|\s*[-*+] |\s*\d+[.)] )/.test(lines[i])) parts.push(lines[i++]);
      const p = el('p'); inline(parts.join('\n'),p); root.append(p);
    }
    return root;
  }
  function details(title, content, open=false) { const d = el('details'); d.open = open; d.append(el('summary',title),content); return d; }
  function raw(title, object) { return details(title,el('pre',pretty(object))); }
  function fields(value) {
    const dl = el('dl');
    for (const [key, item] of Object.entries(value || {})) {
      dl.append(el('dt',label(key))); const dd = el('dd');
      if (item && typeof item==='object' && !Array.isArray(item)) dd.append(fields(item));
      else dd.textContent = Array.isArray(item) ? (item.join(', ') || 'None supplied') : String(item ?? 'Not supplied');
      dl.append(dd);
    } return dl;
  }
  function message(title, text, role='search') { const box = el('article',undefined,`message ${role}`); box.append(el('div',title,'message-label'),markdown(text)); return box; }
  function panel(kind, title, caption) {
    const root = el('section',undefined,`panel ${kind}`), head = el('div',undefined,'panel-title'), body = el('div',undefined,'panel-body');
    head.append(el('h2',title),el('p',caption)); root.append(head,body); return [root,body];
  }
  function promptMessage(m, n) {
    const role = m.role==='system'?'system':m.role==='assistant'?'researcher':'search';
    const name = m.role==='system'?'System instruction':m.role==='assistant'?'Researcher history · API assistant':'Search assistant / input · API user';
    const box = el('div',undefined,`message ${role}`); box.append(el('div',`${n+1}. ${name}`,'message-label'));
    if (m.role==='user') {
      let evidence; try { evidence = JSON.parse(m.content); } catch (_) {}
      if (evidence && Array.isArray(evidence.original_request_messages)) {
        box.append(el('p','Editor input: original model context, prior researcher voice, and the draft.','preview'));
        const originals = el('div'); evidence.original_request_messages.forEach((x,j)=>originals.append(promptMessage(x,j)));
        box.append(details('Original request messages',originals));
        const voice = el('div'); evidence.researcher_last_two_messages.forEach(x=>voice.append(markdown(x)));
        box.append(details('Last two researcher messages',voice));
        box.append(details('Draft supplied to editor',markdown(evidence.draft)));
        if (typeof evidence.fixed_is_final==='boolean') box.append(el('p',`Fixed stop decision: ${evidence.fixed_is_final}`,'decision'));
        box.append(details('Exact editor input text',el('pre',m.content))); return box;
      }
    }
    if (m.content.length>650) { box.append(el('p',m.content.slice(0,220)+'…','preview')); box.append(details('Read complete message',markdown(m.content))); }
    else box.append(markdown(m.content));
    return box;
  }
  function callBody(call, title) {
    const root = el('div'); root.append(el('h3',title),el('p',`Model: ${call.request.model}`,'muted'));
    call.request.messages.forEach((m,i)=>root.append(promptMessage(m,i)));
    root.append(raw('Exact model request JSON',call.request)); return root;
  }
  const query = new URLSearchParams(location.search);
  let ri = Math.max(0,data.runs.findIndex(r=>String(r.task)===query.get('task'))), ci=0, ti=0, whole=false;
  const chosen = data.runs[ri].conversations.findIndex(c=>c.id===query.get('case'));
  if (chosen>=0) ci=chosen;
  const askedTurn = Number(query.get('turn'))-1;
  if (Number.isInteger(askedTurn) && askedTurn>=0 && askedTurn<data.runs[ri].conversations[ci].turns.length) ti=askedTurn;
  whole = query.get('view')==='conversation' && data.runs[ri].task===2;
  function options(select, entries, selected) { select.replaceChildren(); entries.forEach(([value,text])=>{const o=el('option',text);o.value=value;select.append(o)}); select.value=selected; }
  function syncURL() { const r=data.runs[ri], c=r.conversations[ci]; history.replaceState(null,'',`?task=${r.task}&case=${encodeURIComponent(c.id)}&turn=${ti+1}&view=${whole?'conversation':'turn'}`); }
  function renderFlow(t, task) {
    const [input, ib] = panel('input','1 · Organizer input','Supplied scenario and the available conversation');
    ib.append(el('h3','Research goal'),markdown(t.input.scenario.goal.topic));
    ib.append(details('Goal context and discipline',fields(t.input.scenario.goal)));
    ib.append(details('All supplied persona fields',fields({persona:t.input.scenario.persona,persona_goal_interaction:t.input.scenario.persona_goal_interaction})));
    const h = el('div'), prefix=t.input.chat_messages || [];
    if (!prefix.length) h.append(el('p','Opening: no previous messages were supplied.'));
    prefix.forEach((m,i)=>h.append(message(`${i+1} · ${m.participant_name.toLowerCase()==='user'?'Researcher':'Search assistant'}`,m.text,m.participant_name.toLowerCase()==='user'?'researcher':'search')));
    ib.append(details(`Conversation so far · ${prefix.length} messages`,h, prefix.length>0 && prefix.length<=2));
    if(task===2) ib.append(el('p','The endpoint sends the new scenario or latest assistant utterance. Our runner retains the prior turns shown here.','muted'));
    ib.append(raw('Exact organizer input JSON',t.organizer_input));
    if(task===2) ib.append(raw('Context assembled by our runner',t.input));
    const [prompt,pb] = panel('prompt','2 · Our prompt','Separate chat messages, followed by one editor call');
    pb.append(el('p','API assistant = researcher. API user = dataset-search assistant. The system message gives instructions.','muted'));
    pb.append(callBody(t.draft,'Draft request'));
    pb.append(details('Editor request · inspect instructions and evidence',callBody(t.edit,'Editor request')));
    const [output,ob] = panel('response','3 · Our response','Model draft → edit → exact submitted message');
    let draft = t.draft.output; try { const parsed=JSON.parse(draft); if(typeof parsed.text==='string') draft=parsed.text; } catch (_) {}
    ob.append(el('h3','Draft'),markdown(draft),details('Raw draft output',el('pre',t.draft.output)));
    ob.append(el('h3','Submitted researcher reply')); const final=el('div',undefined,'final-response'); final.append(markdown(t.submitted.text)); ob.append(final);
    const same = draft.trim()===t.submitted.text;
    ob.append(el('p',same?'Editor kept the draft unchanged.':'Editor changed the wording; inspect both texts above.','muted'));
    if(task===2) ob.append(el('p',t.submitted.is_final?'Stop decision: researcher chose to end.':'Stop decision: continue the conversation.','decision'));
    const usage = [t.draft,t.edit].filter(x=>x.usage?.cost!==undefined).reduce((v,x)=>v+x.usage.cost,0);
    if(!data.synthetic) ob.append(el('p',`Saved model cost for this turn: $${usage.toFixed(6)} · draft + editor`,'usage'));
    ob.append(raw('Exact submission payload',t.submission_payload));
    const body=t.receipt.body;
    ob.append(el('h3',task===1?'Organizer acknowledgement':'Organizer response'));
    if(task===1) ob.append(el('p',`HTTP ${t.receipt.status}: the next independent prefix was supplied.`,'muted'));
    else if(body.conversation_id!==t.input.conversation_id) ob.append(el('p',`HTTP ${t.receipt.status}: organizer moved to a new conversation. The next scenario is not part of this thread.`,'notice'));
    else if(body.utterance) ob.append(message('Search assistant · organizer',body.utterance.text));
    ob.append(raw('Exact organizer receipt body',body));
    $('flow').replaceChildren(input,prompt,output);
  }
  function renderThread(c) {
    const root=$('thread');root.replaceChildren();
    const goal=el('div',undefined,'goal');goal.append(el('h2',c.title),markdown(c.turns[0].input.scenario.goal.topic),details('Persona and background',fields(c.turns[0].input.scenario))); root.append(goal);
    c.turns.forEach((t,i)=>{
      const user=message(`Turn ${i+1} · Our researcher${t.submitted.is_final?' · final':''}`,t.submitted.text,'researcher');
      const b=el('button',`Inspect input, prompts & response for turn ${i+1}`,'inspect');b.type='button';b.addEventListener('click',()=>{ti=i;whole=false;render();syncURL();window.scrollTo({top:0,behavior:'instant'})});user.append(b);root.append(user);
      const body=t.receipt.body;
      if(body.conversation_id===t.input.conversation_id && body.utterance) root.append(message(`Turn ${i+1} · Organizer search assistant`,body.utterance.text));
    });
    root.append(el('p',c.complete?'Conversation ended naturally. The organizer then supplied a new scenario.':'This is a supplied prefix, not a complete generated conversation.','thread-end'));
  }
  function render() {
    const run=data.runs[ri], c=run.conversations[ci], t=c.turns[ti];
    options($('run'),data.runs.map((r,i)=>[i,r.label]),ri);
    options($('conversation'),run.conversations.map((x,i)=>[i,x.title]),ci);
    options($('turn'),c.turns.map((x,i)=>[i,`Turn ${i+1}${x.submitted.is_final?' · final':''}`]),ti);
    $('turn-label').hidden=run.task===1; $('whole').hidden=run.task===1;
    if(run.task===1) whole=false;
    $('provenance').textContent=data.synthetic?'Synthetic walkthrough · invented example, not an organizer run or measured model output.':'Private official-run reading copy · saved requests and receipts, no new calls.';
    $('source').textContent=`${data.source} Source run: ${run.run}.`;
    $('context-note').textContent=run.note;
    $('selection').textContent=`${c.title} · ${t.id} · ${t.input.chat_messages.length} preceding messages${data.synthetic?' · illustrative text':''}`;
    $('previous').disabled=run.task===1?ci===0:ti===0; $('next').disabled=run.task===1?ci===run.conversations.length-1:ti===c.turns.length-1;
    $('one-turn').setAttribute('aria-pressed',String(!whole)); $('whole').setAttribute('aria-pressed',String(whole));
    $('flow').hidden=whole;$('thread').hidden=!whole; renderFlow(t,run.task); if(run.task===2) renderThread(c);
  }
  $('run').addEventListener('change',e=>{ri=Number(e.target.value);ci=ti=0;whole=false;render();syncURL()});
  $('conversation').addEventListener('change',e=>{ci=Number(e.target.value);ti=0;render();syncURL()});
  $('turn').addEventListener('change',e=>{ti=Number(e.target.value);whole=false;render();syncURL()});
  $('previous').addEventListener('click',()=>{if(data.runs[ri].task===1)ci--;else ti--;render();syncURL()});
  $('next').addEventListener('click',()=>{if(data.runs[ri].task===1)ci++;else ti++;render();syncURL()});
  $('one-turn').addEventListener('click',()=>{whole=false;render();syncURL()});
  $('whole').addEventListener('click',()=>{whole=true;render();syncURL()});
  render();
})();
