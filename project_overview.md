# Project Overview

## What This Repo Is

This repository is a small fiber photometry post-analysis workspace. It contains script-style Python analyses for loading MATLAB `.mat` files, pooling signals across experimental groups, and plotting histograms or peri-event views.

The main script is `plot_group_hist_normalized_overlay.py`. It compares grouped distributions for two signals by pooling files within each group, clipping outliers to a global 1st-99th percentile range, and drawing density-normalized overlay histograms.

Use the local `fp_analysis_dist` conda environment for this repository.

## Active Runtime Path

### 1. Configure Groups

`plot_group_hist_normalized_overlay.py`

- Edit `file_map` to point each group folder to the `.mat` files in that group.
- Edit `signal_A_name` and `signal_C_name` if the MATLAB field names change.

### 2. Load And Pool

`scipy.io.loadmat` loads each file. The script reads each signal, flattens it, skips missing or empty arrays, and concatenates values per group.

### 3. Normalize Plot Range

The script computes global 1st and 99th percentiles separately for `signal_A` and `signal_C`, clips all groups to those ranges, and plots density histograms. This makes groups comparable while reducing the visual impact of outliers.

### 4. Plot

The output is one figure with two stacked panels:

- top: normalized overlay histogram for `signal_A`
- bottom: normalized overlay histogram for `signal_C`

The script currently displays the figure. Uncomment `plt.savefig(...)` and point it at `plots/` to save the output.

## Repo Structure Map

```text
project_root/
|- AGENTS.md
|- README.md
|- project_overview.md
|- next_steps.md
|- work_log.md
|- work_log_archive/
|- data/
|  |- SOD1_*/*.mat
|  |- SOD1_*/*_hist.png
|- plots/
|  |- group_hist_normalized_overlay.png
|  |- group_hist_normalized_subplots.png
|- plot_group_hist_normalized_overlay.py
|- plot_group_hist_normalized_subplots.py
|- plot_group_hist_normalized_overlay_jaspreet.py
|- plot_hist.py
|- read_events.py
|- sketch.py
```

## What Looks Active vs. Secondary

### Active / relevant now

- `plot_group_hist_normalized_overlay.py` - main grouped overlay histogram for local `signal_A` and `signal_C` data.
- `plot_group_hist_normalized_subplots.py` - same local grouping idea, but draws separate rows per group and columns per signal instead of overlaying groups.

### Secondary or exploratory

- `plot_group_hist_normalized_overlay_jaspreet.py` - one-signal overlay variant for `ne`, with external `H:` drive paths and hard-coded color mapping for C57 control, SOD1 control, and SOD1 sick groups.
- `plot_hist.py` - older per-file histogram generator. It uses the same local SOD1 groups, computes global clipping ranges, then saves one `*_hist.png` next to each `.mat` file.
- `sketch.py` - exploratory sleep-stage analysis for one file. It segments wake/SWS/REM/micro-arousal intervals, extracts signal values, computes summary statistics, and plots stage histograms.
- `read_events.py` - peri-event helper script. It reads event times from Excel, converts them to sample indices, extracts windows around events, and provides line/mean/heatmap plotting helpers.

## Tests And Fixtures

There is no formal test suite. The practical smoke check is:

```powershell
Get-ChildItem *.py | ForEach-Object { python -m py_compile $_.FullName }
```

Local data lives under `data/`. Existing generated figures are under `plots/` and as `*_hist.png` files next to some input `.mat` files. These folders are ignored by Git by default.

## User Data Expectations

The main local histogram scripts expect MATLAB files with array-like fields named `signal_A` and `signal_C`. The scripts flatten these arrays before plotting.

`sketch.py` expects sleep score arrays and a photometry signal in a single `.mat` file. `read_events.py` expects a `.mat` file plus an Excel file whose columns contain event times in seconds.

## Practical Mental Model

Read files in this order:

1. `README.md`
2. `plot_group_hist_normalized_overlay.py`
3. `plot_group_hist_normalized_subplots.py`
4. `plot_hist.py`
5. `sketch.py` and `read_events.py` only when working on sleep-stage or event-centered analyses

## Questions Worth Clarifying Later

- Whether the Jaspreet `H:` drive workflow should become a configurable script or remain a local one-off variant.
- Whether output saving should be standardized so group plots always write to `plots/`.
- Whether the scripts should stay hard-coded and lightweight, or move toward command-line arguments/config files.
