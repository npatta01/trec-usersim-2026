# Historical experiments

These replay scripts and optional generators preserve the research trail. They
are not dependencies of the supported Task 2 runner. The runtime is in
`usersim/`, the supported CLI is `scripts/run_task2_debug.py`, and offline tests
are in `tests/`.

Run an experiment module from the repository root with `python -m experiments.NAME`
only when that experiment is separately authorized. Most require private data,
case manifests, prior results, and credentials that are deliberately absent from
git. Some entry points make paid calls; importing them is not authorization to run
them. Old source hashes and frozen result directories must remain unchanged.

- `run_offline_baseline`, `run_researcher_role_diagnostic`: organizer baseline and
  role-mapping diagnostics.
- `run_single_call_prompt_comparison`, `run_prompt_iteration_b21`,
  `run_prompt_iteration_b22`, `run_style_postedit`: historical prompt/editor studies.
- `run_task1_debug`: historical Task 1 debug implementation, retained for provenance.
- `attributed_generator`, `attributed_renderer`, `fidelity_reviser`: unselected
  experimental generation path.

The old prompt builders remain here as research provenance. Live code uses the
pure builders in `usersim/prompts.py`; it never imports these experiment modules.
