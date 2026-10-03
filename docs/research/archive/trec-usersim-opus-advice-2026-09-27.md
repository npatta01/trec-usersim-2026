> Historical note from September 27, 2026. Preserved for provenance; recommendations and source versions may be superseded. Start with the [current research summary](../README.md) and [October 3 refresh](../2026-10-03-research-refresh.md). Advisor opinions are not experimental results.

# TREC UserSim: independent Opus advice

Date: 2026-09-27. Requested model: Claude Opus alias (`opus`), max effort. Authentication: first-party claude.ai subscription. Status: successful. Read-only review of a frozen public-source packet. These are advisor conclusions, not independently verified results; recalled references are explicitly marked. The primary synthesis must not treat speculative code effects or claimed near-certainty of winning as established.

## VERDICT

Tags: **V** = verified in the packet (claims about the code come from reading the excerpts; nothing was run). **I** = my inference. **U** = unknown. **L** = a paper I recall but did not look up, so the title, year or venue may be wrong.

- **The prior ranking has the right pieces in the wrong order, and it overstates how new they are.** What gets scored is visible behaviour: whether human raters can spot the simulator, and how utterance length, turn count, clarifications and dialogue acts are distributed [V]. The best bet for the October 7 deadline, in order [I]:
  1. Fix the baseline's defects and add a way for the simulated user to stop.
  2. Add real human example conversations to the prompt (in-context learning, "ICL").
  3. Calibrate visible behaviour to the human logs: length, acts, how much of the goal is revealed, and when to stop.
  4. Pick among candidate replies using a detector that separates human from simulated turns.
- **Rejected:**
  - The knowledge / unmet-needs / frustration state machine as the main bet. Nothing in the packet supports it, and older simulators already did this (agenda-based and emotion-aware ones [L]).
  - Think-aloud supervision in a submitted run. Nobody has looked at that data yet [U].
  - Stopping presented as new research, or held back to run 4 only.
  - Retrieval presented as new research.
  - Fine-tuning a small model without first checking that the data is big enough.
- **What is most likely to win by October 7 is not original. The most original asset, the think-aloud data, is the least likely to pay off by October 7.** No approach has been tested on dataset search. The only evidence comparing methods is ConvApparel, which is about apparel shopping.

## STRONGEST EVIDENCE

1. **The score measures behaviour, not task success** [V, E1]. It covers rater identification plus the distributions of length, turn count, clarifications and dialogue acts. Outcome metrics are postponed to a later year, and the weights are unknown.
2. **The public baseline has real defects** [V, from reading E5]:
   - **Roles are swapped.** `LLMStrategy` tags the simulator's own past turns as `user` and the agent's turns as `assistant`, then asks for the next message. So the model writes in the slot labelled as the agent.
   - **The agent's last turn is sent twice.** It is already in `chat_history` (via `add_agent_message`) and gets appended again, so the prompt ends with two identical `assistant` messages.
   - **Later conversations use the wrong goal.** `self.scenario` is only set in `initiate_run` or on resume. `initiate_conversation` never updates it, so every conversation after the first in a run uses the first scenario's persona and goal.
   - **The user never stops.** `is_final` is always `False`, so there is no user-side stop decision. Turn counts are decided by the agent or the server.
   - **Errors go out as user turns.** A failure is sent as "I'm sorry, I couldn't generate a response right now."
   - **Weak defaults.** The default model is `qwen3:0.6b`, and the example run uses `RandomStrategy`, which sends canned lines that ignore the goal.
   - **Possible early exit.** When the agent sends `is_final`, the whole run loop ends, not just that conversation. Whether that is intended is [U].
3. **ConvApparel** [V, E2]:
   - Compared with a plain prompt, ICL (3 retrieved example conversations) improved distribution fit (KS test) on 9/11 and 10/11 metrics. Fine-tuning improved 8/11 and 9/11, so it did not win on count. The packet does not give effect sizes.
   - No method closed the gap to humans, and all scored very low on human-likeness.
   - Detection: a simple word-pair classifier got 0.92 accuracy and a trained classifier 0.99. So there are strong word-level giveaways.
   - An LLM prompted to detect got 0.57, close to chance. So a prompted LLM judge is a poor way to measure detectability during development.
4. **Conditioning on persona or traits is not new** [V, E3/E4]. USP's sampling of user profiles from a distribution is the nearest earlier work on making the simulated population varied.

## FAILURE MECHANISM OR DECISION LOGIC

Why the prior plan can lose [I]:
- **It aims at hidden reasoning; the score looks at surface behaviour.** A state machine does not remove the usual giveaways of an LLM playing a user:
  - long messages
  - assistant style: markdown, thanking every turn
  - stating the whole goal in turn 1
  - being overly cooperative
  - never quitting
- **Actions chosen by an LLM cluster on the most likely option.** Acts and lengths come out too uniform, which hurts distribution scores even when the averages are right. The pooled human distribution also mixes terse and wordy people, and one prompt style cannot reproduce that spread.
- **Forcing one act label per turn is too rigid.** Real turns often do several things at once ("thanks — county level? free?"). The team's own act categories may not match the organizers' [U], so matching your own act histogram may not improve theirs.
- **Pipelines with several LLM calls per turn** add delay and let errors pile up in the live Task 2 conversations.
- **Stopping only in run 4** handicaps runs 1–3 on something that is scored, and muddies the comparison between runs.
- **Think-aloud data is uncertain.** Its size and alignment to turns are unknown. Thinking aloud slows people down (L: Ericsson & Simon; Fox et al. 2011), so those sessions may not look like the sessions the score is based on.
- **Outcome metrics are postponed** [V]. Effort spent on making the user reach goals rationally earns nothing this year.

The most direct lever for each scored item [I]:

| Scored item | Most direct lever |
|---|---|
| Length | A writing-style profile per simulated user; pick replies by length band |
| Turn count | A user-side stopping model fitted to the logs |
| Clarifications | Control how much of the goal the first turn reveals; how the user answers clarifying questions |
| Dialogue acts | Target act frequencies taken from the human logs (use the organizers' categories if published) |
| Rater identification | Human examples; removing giveaways; detector-picked replies; a model trained to write as the user; novices don't name datasets they wouldn't know |

## RECOMMENDATION

Ranked shortlist. Each item shows its evidence type, its value by October 7, and how new it is.

0. **Prerequisites.** Engineering, not research [V].
   - Fix the defects above, use a stronger model, and retry on errors instead of sending the fallback text.
   - Add a check that strips giveaways, and user-side stopping in every Task 2 run.
   - Value by Oct 7: high. Novelty: none.
1. **Human example conversations in the prompt (ICL).** Supported in apparel only, so a hypothesis to test here [V].
   - Compare situation-matched examples against randomly chosen ones. Unless situation-matched wins, retrieval is not a research contribution.
   - Matching by situation needs a live act tagger, which adds delay and its own errors.
   - Examples copied too closely can carry the wrong dataset names.
   - Value by Oct 7: medium-high. Novelty: low.
2. **Calibrate by choosing among candidates.** This replaces the state machine. My inference, using standard statistics.
   - Per conversation, borrow a real user's writing style: words per turn, capitalisation, punctuation, thanking habits.
   - Per turn:
     1. Generate N candidate replies at temperature ≈1.
     2. Tag each with its act and length band.
     3. Draw a target band from the human logs, given the turn number and the agent's last act.
     4. Keep the candidate in that band that the detector rates most human.
   - Stopping: at each turn, predict the chance the user quits from:
     - turn number
     - whether the agent delivered datasets
     - agent failure
     - the persona's patience
   - Fit that stopping model on the logs, treating sessions the agent ended as "user had not quit yet" (not as a user stop).
   - This only works if some candidates already look like human turns. The examples or the base model supply that range; the selection step fixes the proportions.
   - Value by Oct 7: high. Novelty: low to moderate.
3. **Pick replies with a detector.** Use a simple word-pair classifier to rank candidates, and judge the result with a different type of detector. Inference; that the signal exists is shown by ConvApparel.
   - Value by Oct 7: medium. Novelty: low to moderate.
4. **Task 1: learn from the real user's earlier turns.** In Task 1 the supplied history contains that user's own messages. Match their length, capitalisation, punctuation and what they showed they know. Inference.
   - Value by Oct 7: high for Task 1. Novelty: low.
5. **Use a model trained to write as the user.** A hypothesis borrowed from other work [L].
   - A model trained specifically on user turns (L: UserLM-8b), used as-is or lightly fine-tuned.
   - Full fine-tuning only if more data keeps improving results.
   - After the deadline: preference training that ranks human turns above the model's own (SPIN-style [L]).
   - Value by Oct 7: high but uncertain. Novelty: moderate.
6. **Use think-aloud to check, not to train** [U].
   - Code the reasons people stop or give up, and how much of their goal they reveal, to set the simulator's starting assumptions.
   - Test whether states inferred from the dialogue alone agree with what people said while thinking aloud.
   - Value by Oct 7: low. Novelty: possibly high; I have not searched to confirm.
7. **The knowledge / needs / frustration state machine.** Already done in earlier work [L].
   - Shrink it to a small tracker: which constraints have been revealed, plus a frustration flag feeding the stopping model.
   - Value by Oct 7: low to medium. Novelty: low.

Run plan. Each run adds one thing, so gains can be attributed:
- **Task 2:**
  - R1: prerequisites + stopping model.
  - R2: R1 + human examples.
  - R3: R2 + calibrated, detector-picked replies.
  - R4: R3 on the user-trained model if development tests favour it; otherwise R3 with a different stopping model.
- **Task 1:**
  - R1: prerequisites + learning from the prefix.
  - R2: R1 + human examples.
  - R3: R2 + calibrated selection.
  - R4: a version of the best run that always predicts the single most likely reply. This covers you if Task 1 is scored turn by turn rather than by distribution.
- If only the best single run matters, swap R1 for a second model choice.

Possible research findings for the write-up [I; not checked for novelty]:
- Situation-matched versus random examples.
- Differences between users versus within one user, and how that affects distribution scores.
- Whether stopping carries over to an assistant left out of calibration.
- Over-optimising against one detector versus a different detector and blind human raters.
- Think-aloud as a check on inferred user states.
- Dataset-search checking behaviour. If think-aloud shows users test links or access, a simulator with a link checker could produce "that link is dead" turns.

Literature the focused review missed. These are recalled, not looked up; check before citing.
- **Models trained to write user turns:**
  - Naous, Laban, Xu, Neville, "Flipping the Dialogue: Training and Evaluating User Language Models" (arXiv 2025) [L-moderate].
  - Kong et al., PlatoLM (ACL 2024) [L-moderate].
- **Where LLM-played users fall short:**
  - Dou et al., "SimulatorArena" (2025) [L-moderate/low].
  - Ivey et al., "Real or Robotic?" (arXiv 2024) — close to Task 1 [L-moderate/low].
  - Yoon et al. (NAACL 2024) [L-moderate].
  - Zhu et al., "How Reliable is Your Simulator?" (WWW 2024) [L-low].
- **Earlier work that already did item 7:**
  - Schatzmann et al., agenda-based simulation (NAACL 2007) [L-high].
  - Lin et al., GenTUS (SIGDIAL 2022) and EmoUS (SIGIR 2023) [L-moderate].
- **Clarifications:** Sekulić, Aliannejadi, Crestani, USi (WSDM 2022) [L-high].
- **Scoring simulators by distribution:**
  - Pietquin & Hastie survey (Knowledge Engineering Review 2013) [L-moderate].
  - Williams, Cramér–von Mises divergence (Speech Communication 2008) [L-moderate].
- **Matching distributions and using detectors:**
  - SPIN (ICML 2024) [L-moderate/high].
  - Li et al., adversarial dialogue generation (EMNLP 2017) [L-high].
  - "Verbalized Sampling" (arXiv 2025) [L-moderate].
- **Rationale data similar to think-aloud:**
  - "Beyond Believability" (arXiv 2025) [L-moderate].
  - OPeRA (2025) [L-low].
  - Ericsson & Simon, *Protocol Analysis* (1993) [L-high].
  - Fox, Ericsson & Best (Psychological Bulletin 2011) [L-moderate].
- **Stopping:**
  - Maxwell et al., "Searching and Stopping" (CIKM 2015) [L-moderate].
  - Sun et al., simulating user satisfaction (SIGIR 2021) [L-moderate].
- **How people search for datasets:**
  - Koesten et al. (CHI 2017) [L-moderate].
  - Chapman et al., "Dataset search: a survey" (VLDB Journal 2020) [L-high].

Searches to run:
- `"user language model" simulat*` (2025–26)
- `"user simulator" (human-likeness OR indistinguishab* OR Turing)`
- `"think-aloud" (LLM OR "language model") simulat*`
- `Sim4IA 2025 shared task`
- `"mode collapse" OR "distributional alignment" user simulation`
- `"dataset search" conversational assistant 2024..2026`
- The organizers' own papers on this test setup.

## WHAT COULD CHANGE THE RECOMMENDATION

- **Task 1 is scored turn by turn against the true next turn:** predict the single most likely reply and drop sampling there.
- **The organizer baseline is this public code:** beating it is near-certain, so aim for rank among teams and a clean finding. If the baseline is a separate, stronger system, the realism levers matter more.
- **Training data size:**
  - A few thousand user turns or more: move item 5 up to second place.
  - Only a few hundred: stick to human examples and calibration with few parameters.
- **Think-aloud is aligned to turns and large enough:** a think-aloud-based variant can compete for R4, once development tests support it.
- **The organizers publish their act and clarification definitions:** target them directly.
- **The data use agreement forbids sending logs to hosted APIs:** use open models run locally only. That changes both the model choice and the example-in-prompt design.
- **Tight rate limits:** generate fewer candidates and make fewer calls per turn.

Experiments that could overturn my ranking:
1. **Do the fixes matter?** On Task 1 development data, compare the baseline as-is against the fixed version. If length fit, act fit and detector score don't move, the defects don't matter; spend the effort elsewhere.
2. **Does choosing among candidates help?** Compare it with telling the model the target act/length, and with no control. If distribution fit doesn't improve, or the detector finds the output easier to spot, drop item 2. First check that candidates cover human-like lengths and acts.
3. **Does retrieval by situation help?** Compare no examples, 3 random, 3 situation-matched and 3 topic-matched. If random does as well as situation-matched, the value is just exposure to human style; drop situation matching.
4. **Which stopping works?** Compare no stopping, LLM-decided, the fitted model and a mix. Measure turn-count fit against human sessions with the same assistant, and repeat with one assistant held out.
5. **Does the state machine react like a human?** Following ConvApparel, make the assistant worse on purpose. If the state-machine version doesn't shift turns, frustration and quitting toward human patterns more than plain prompting does, drop item 7.
6. **Are we just fooling one detector?** Pick replies with the word-pair classifier, then score with a separately trained detector plus a blind human check of about 40 items.
7. **Which model?** Compare a chat model, a base (non-chat) model and a user-trained model at temperature 1, on length fit and detector score. Also try a private "think first" step on and off; it may make users more rational and less human.
8. **Is think-aloud data typical?** Compare length and turn statistics for think-aloud versus normal sessions. If they differ, don't mix them into the examples or training data.

## RISKS AND UNKNOWNS

- **Unknown scoring details:** the formula and weights, whether raters see single turns or whole conversations, and whether they rate every run.
- **Unknown test setup:** whether the test assistants are the same ones as in the training logs.
- **Who produced the logs:** whether they came from real researchers or from people acting out assigned scenarios. This changes how much to trust the persona fields.
- **Leakage:** Task 1 test histories may come from the same sessions as the training logs.
  - Split by session or user.
  - Never retrieve from the same session.
  - Don't take advantage of any overlap you find.
- **Calibration may not carry over to new assistants.** Condition on what the agent did, not just on the turn number.
- **Faking human traits:**
  - Over-optimising against one detector.
  - Adding typos or terseness from stereotypes instead of the logs.
  - The LLM's broad knowledge leaking into novice personas.
- **Schedule:** 10 days left, TREC credentials still needed for the logs, possible API outages near the deadline. Small test sets make differences between runs noisy.
- **Code I could not see:** I did not read `api_client.py` or `scenario.py`.
  - Check that Task 1's supplied history actually reaches the prompt. The normal path adds only `response.utterance`; `chat_messages` is read only when resuming.
  - Check whether qwen3's `<think>` reasoning text leaks through Ollama (depends on the version).
- **Coverage:** the papers above are recalled, not searched for; the list is not complete.

## FIRST BOUNDED ACTION

Build the development measuring setup before any method work (at most 1 day):
- [ ] Confirm log access and that the data use agreement allows the model hosting you plan to use. If you can't get the logs yet, stop here; that is the only step.
- [ ] Look in the guidelines for the act categories and the definition of a clarification.
- [ ] Split the human logs by session (about 80/20) and compute reference numbers:
  - [ ] histogram of user-turn lengths
  - [ ] turns per conversation
  - [ ] act and clarification rates, using a fixed tagger
- [ ] On about 100 Task 1 development histories, run three versions:
  - [ ] (a) the public `LLMStrategy` unchanged
  - [ ] (b) the same model with roles swapped back, the duplicate turn removed and the scenario refreshed
  - [ ] (c) version (b) on a stronger model at temperature ≈1
- [ ] Score each version:
  - [ ] length fit (KS)
  - [ ] act fit (Jensen–Shannon divergence)
  - [ ] a held-out word-pair detector
- [ ] Decision: the best version becomes the base for all runs. Run the retrieval comparison next.