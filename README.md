# Fiber Photometry Post Analysis

Small Python workspace for plotting fiber photometry `.mat` outputs. The main workflow compares signal distributions across experimental groups.

## Quick Start

```powershell
conda activate fiber_photometry
python plot_group_hist_normalized_overlay.py
```

Edit the configuration block at the top of `plot_group_hist_normalized_overlay.py` to change groups, input files, or signal field names. By default the script displays the plot; uncomment `plt.savefig(...)` to save a PNG.

## Main Scripts

- `plot_group_hist_normalized_overlay.py` - main script. Pools `signal_A` and `signal_C` by group, clips each signal to a global 1st-99th percentile range, and overlays density-normalized histograms.
- `plot_group_hist_normalized_subplots.py` - same grouped data, but one row per group and one column per signal.
- `plot_group_hist_normalized_overlay_jaspreet.py` - one-signal `ne` overlay variant for external `H:` drive data.
- `plot_hist.py` - older per-file histogram generator that saves `*_hist.png` beside each input `.mat`.
- `sketch.py` - exploratory sleep-stage histogram analysis.
- `read_events.py` - peri-event signal extraction and plotting helpers.

## Data

Local input data is expected under `data/`. Main grouped histogram scripts expect `.mat` files with `signal_A` and `signal_C` arrays.

Generated group figures belong in `plots/`. Both `data/` and `plots/` are local artifacts by default.
