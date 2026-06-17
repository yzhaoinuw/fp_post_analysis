# Work Log

Prepend new session notes to the top of this file.

Rotation policy: the live log holds at most the **5 most recent unique calendar dates**. When a new date would push the file past 5 unique dates, move the oldest 5 dates as a chunk into a new file at `work_log_archive/work_log_<earliest>_to_<latest>.md`. The live file always holds at most 5 unique dates; each archive file always holds exactly 5.

If today's date already has a `## YYYY-MM-DD` header at the top, add a new `###` session subsection under it rather than starting a second `## YYYY-MM-DD` header for the same date.

Update this log at the end of any substantive work session unless the user explicitly asks not to document it. Substantive work includes file edits, meaningful validation or debugging, technical decisions or reversals, reusable discoveries, branch/PR/release state changes, or follow-up work that future agents need. Log useful experiments even when the code was reverted; skip casual Q&A, trivial one-off commands, and pure scratch work with no future coordination value.

## 2026-06-17

### Prepared docs commit and publish scope (GPT-5)

- Added `.gitignore` for Python cache files plus local `data/` and `plots/` artifacts.
- Kept raw `.mat` inputs and generated figures local rather than committing 68 MB of analysis artifacts without an explicit dataset-publish request.
- Included the current `plot_group_hist_normalized_overlay.py` figure-size change in the commit scope.
- Verification:
  - `Get-ChildItem *.py | ForEach-Object { C:\Users\yzhao\miniconda3\envs\fiber_photometry\python.exe -m py_compile $_.FullName }` passed.

## 2026-06-16

### Filled project docs and README (GPT-5)

- Documented `plot_group_hist_normalized_overlay.py` as the active script for grouped, density-normalized overlay histograms of `signal_A` and `signal_C`.
- Added concise descriptions of the neighboring scripts and how they differ from the main overlay workflow.
- Replaced template treaty docs with repo-specific guidance in `AGENTS.md`, `project_overview.md`, and `next_steps.md`.
- Added a short user-facing `README.md`.
- Marked this repository as Git-safe for the current Windows environment after Git reported dubious ownership.
- Verification:
  - `Get-ChildItem *.py | ForEach-Object { C:\Users\yzhao\miniconda3\envs\fiber_photometry\python.exe -m py_compile $_.FullName }` passed.

<!--
Each session entry follows this shape:

## YYYY-MM-DD

### Short title for what was done (model + version, effort/thinking mode, token budget if known)

- bullet describing what was added or changed
- another bullet — keep them high-level and user/agent-facing, not implementation play-by-play
- if relevant, intended profiling signal or measurement:
  - what to look for in logs / output
  - what numbers were observed
- Verification:
  - the exact command(s) that were actually run
  - what passed / what was confirmed

Model / effort / token info goes in the parentheses after the `###` title when available from the system. Use whatever the model or interface actually reports — do not estimate or hallucinate. Omit any field that the interface does not surface.

- **Model**: the version string the interface reports (e.g. `grok-4.3`, `gpt-4o`, `claude-opus-4-7`).
- **Effort / thinking mode**: the effort knob the interface reports (e.g. `high`, `low`, `extended thinking`). Omit if no such knob exists or its setting is not surfaced.
- **Token budget**: **output tokens for the session** (output + thinking/reasoning tokens for models that report them separately, e.g. Claude with extended thinking). This is the cleanest cross-agent proxy for "amount produced." Omit if the interface does not surface a count.

Purely human-driven work can use `(human)`. Mixed human + agent sessions can combine them, e.g. `(human + grok-4.3, high)`.

Keep the parenthetical compact. Examples:
- `(grok-4.3, high, ~18k out)`
- `(gpt-4o, high, ~22k out)`
- `(claude-opus-4-7, extended thinking, ~30k out)`
- `(grok-4.3, low)`

Newest entry goes on top. If the session did multiple distinct pieces of work, use multiple `###` subsections under one `##` date header.
-->
