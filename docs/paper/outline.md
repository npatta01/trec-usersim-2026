# Working paper outline

This is a writing scaffold, not a finished paper or a new experimental plan.
Use the [paper evidence map](README.md) for sources and unresolved requirements.

**Working title:** A prompted researcher simulator for TREC UserSim 2026.
Author list, affiliations and venue formatting remain unset.

1. **Introduction and task.** Explain that we generate the researcher, while
   the organizer runs the dataset-search assistant. Define Task 1's supplied
   prefix and Task 2's interactive session and autonomous stop decision. Frame
   the work as a baseline system account; avoid unmeasured claims of novelty
   or human equivalence.
2. **Data and development setting.** Describe the user-supplied official export,
   its checksum, schema and coverage; separate it from the supplementary
   collection. Explain correlated turns, unknown participant identities and
   absent positive researcher-stop supervision. State exactly which fields
   are rendered into the model request and how future-turn leakage is avoided.
3. **Submitted system.** Lead with the implemented diagram. Describe researcher
   chat-role mapping, persona/goal instructions and full utterance history;
   then one draft call and one editor call. Explain Task 1's narrow action-claim
   repair and Task 2's style editor, JSON stop signal and validation. Describe
   resets and transport recovery separately from simulated user behavior.
4. **Development evidence.** Select only comparisons that explain the final
   choices: local wrong-speaker diagnostics, hosted model continuation, editor
   action repair and small harder-case screens. State sample, control, review
   procedure and caveats for every reported preference. Put the full experiment
   inventory in an appendix; do not narrate every iteration.
5. **Official evaluation.** Identify both official run IDs. Report official
   metrics only once organizer reports are available. Separately present the
   current coverage/cost table and administrative error closures. Audit passing
   belongs in reproducibility/integration, not effectiveness.
6. **Limitations.** Discuss persona/style realism, unsupported knowledge/actions,
   excessive persistence, missing human stop labels, small repeated development
   samples, manual-review bias, model/provider reproducibility and operational
   closures. A preserved stop boolean does not prove semantic agreement.
7. **Reproducibility and conclusion.** Give requested model/provider configuration,
   source/frozen hashes and public code/tests. Explain private evidence custody
   and sharing restrictions, distinguish current code from frozen execution and
   terminal reconciliation, and summarize only supported findings.

Useful figures already exist: [task comparison](../images/task-comparison.svg),
[draft/editor flow](../images/researcher-pipeline.svg) and
[recovery flow](../images/recovery-flow.svg). Use the last only if transport
handling warrants paper space. The colorful [viewer](../run_viewer.md) is an
inspection aid, not an evaluation metric or a substitute for a labeled figure.

Primary references to verify when assembling the bibliography include the
[track guidelines](https://trec.usersim.ai/guidelines), organizer starter and
the literature sources listed in [method decisions](../research/method-decisions.md#literature-transfer-boundary)
and the [source refresh](../research/2026-10-03-research-refresh.md).
Preserve paper versions and pinned implementation commits. Do not describe
our adaptations as reproductions or claim the referenced systems were evaluated
in this track.
