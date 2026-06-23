# Guidelines and Tips for Agents

Read this file first when joining work on this repository. It is the collaboration guide for the Agent Collab Treaty docs in this project.

## Startup Rule

Do not automatically read every markdown file. Use the map below:

- `project_overview.md` for the codebase map and active-vs-secondary scripts.
- `next_steps.md` for open follow-ups.
- `work_log.md` for recent decisions and verification breadcrumbs.
- `README.md` for the user-facing quick start.

## Runtime Environment

Use the local conda environment:

```powershell
conda activate fp_analysis_dist
```

The environment is expected to provide `numpy`, `scipy`, `matplotlib`, `pandas`, and Excel support for `pandas.read_excel` when using `read_events.py`.

## Common Tasks

Generate the main group overlay plot:

```powershell
python plot_group_hist_normalized_overlay.py
```

Before running, edit the script's `file_map`, `signal_A_name`, and `signal_C_name` section if the groups, files, or signal keys changed. The script currently displays the plot interactively; uncomment the `savefig` line to write a PNG.

Generate the grouped subplot variant:

```powershell
python plot_group_hist_normalized_subplots.py
```

Compile-smoke the scripts:

```powershell
Get-ChildItem *.py | ForEach-Object { python -m py_compile $_.FullName }
```

There is no formal test suite in this repo yet.

## When To Update Treaty Docs

At the end of any substantive session, update `work_log.md` unless the user explicitly asks not to. Substantive work includes file edits, validation, debugging, reusable discoveries, branch or environment state changes, or concrete follow-up work.

When a session creates future work, update `next_steps.md` in the same pass.

## Branch Handoff Discipline

Before switching branches, check:

```powershell
git status --short --branch
git log --oneline --left-right --cherry-pick main...HEAD
```

If Git reports dubious ownership for this repo, mark only this repository as safe:

```powershell
git config --global --add safe.directory C:/Users/yzhao/python_projects/fp_post_analysis
```

## Project-Specific Reminders

- `plot_group_hist_normalized_overlay.py` is the main script to preserve and understand first.
- The histogram scripts are script-style analyses, not packaged modules. Prefer small, explicit edits over broad refactors.
- Input `.mat` files are grouped through hard-coded `file_map` dictionaries. A filename may omit `.mat`; the scripts append it automatically.
- Main local data currently expects `signal_A` and `signal_C` arrays. The Jaspreet variant expects an `ne` array and external `H:` drive paths.
- `plot_hist.py` writes per-file `*_hist.png` outputs into the data folders. Do not regenerate or overwrite these unless intended.
- Keep generated figures under `plots/` when adding new saved group outputs.
- `data/` and `plots/` are local artifacts ignored by Git unless the user explicitly asks to publish a dataset or generated figure.
