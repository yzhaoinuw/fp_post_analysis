# -*- coding: utf-8 -*-
"""
Created on Thu May 22 01:16:39 2025

@author: yzhao
"""

from itertools import cycle
from pathlib import Path

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

#%% USER INPUT: Edit only this section.
# In file_map, keep all quotes, brackets, colons, and commas.
# Use r"C:\folder\file.mat" for an absolute Windows path.
# Use "./folder/file.mat" for a path relative to this script.
file_map = {
    "C57_Control": [  # Group name: edit only the text inside the quotes.
        "./data/groupby_sleepscores/C57M1_2025-06-11_11-18-19-341_PMC_sleepscored_16June2026.mat",  # One MAT file path.
        "./data/groupby_sleepscores/C57M2_2025-06-11_11-18-19-341_PMC_sleepscored_16June2026.mat",  # Add more paths on new lines.
    ],
    "SOD1_Control": [  # Start each additional group with its group name.
        "./data/groupby_sleepscores/CtrlSOD1_M130_2025-06-10_09-54-55-53_PMC_sleepscored_june2026.mat",
    ],
    "Sick": [
        "./data/groupby_sleepscores/SOD1_M194_sleep_2025-10-17_08-31-52-36_PMC_sleepscored_jun2026.mat",
        "./data/groupby_sleepscores/SOD1M164Score3_2025-07-14_10-05-28-148_PMC_sleepscored_16June2026.mat",
        "./data/groupby_sleepscores/SOD1M175SCORE4SLEEP_2025-07-22_11-15-32-993_PMC.mat",
    ],
}

# Save a PNG automatically after plotting.
save_figure = True  # Change to False if you only want to display the plot.
# This may also be an absolute path, such as r"C:\folder\my_plot.png".
figure_output_path = "./plots/jaspreet_group_hist_by_sleep_state.png"
figure_dpi = 300

# Do not edit below this line unless the MAT field names change.
signal_A_name = "ne"
sleep_scores_name = "sleep_scores"
signal_frequency_name = "ne_frequency"
sleep_score_labels = {
    0: "SWS",
    1: "Wake",
    2: "REM",
    3: "MA",
}

#%%
# Validate the user-entered group names and paths before loading large files.
script_directory = Path(__file__).resolve().parent
resolved_file_map = {}
configuration_errors = []

if not isinstance(file_map, dict) or not file_map:
    configuration_errors.append("file_map must contain at least one group.")
else:
    for group, file_paths in file_map.items():
        if not isinstance(group, str) or not group.strip():
            configuration_errors.append(
                "Every group name must be non-empty text inside quotes."
            )
            continue
        if not isinstance(file_paths, (list, tuple)) or not file_paths:
            configuration_errors.append(
                f"Group '{group}' must contain at least one file path inside [ ]."
            )
            continue

        resolved_file_map[group] = []
        for file_path in file_paths:
            if not isinstance(file_path, str) or not file_path.strip():
                configuration_errors.append(
                    f"Group '{group}' contains an empty or invalid file path."
                )
                continue

            mat_path = Path(file_path).expanduser()
            if mat_path.suffix.lower() != ".mat":
                mat_path = Path(f"{mat_path}.mat")
            if not mat_path.is_absolute():
                mat_path = script_directory / mat_path
            mat_path = mat_path.resolve()

            if not mat_path.is_file():
                configuration_errors.append(
                    f"File not found for group '{group}': {mat_path}"
                )
                continue
            resolved_file_map[group].append(mat_path)

if not isinstance(save_figure, bool):
    configuration_errors.append("save_figure must be either True or False.")
if save_figure:
    if not isinstance(figure_output_path, str) or not figure_output_path.strip():
        configuration_errors.append(
            "figure_output_path must be a non-empty path inside quotes."
        )
    if (
        isinstance(figure_dpi, bool)
        or not isinstance(figure_dpi, (int, float))
        or not np.isfinite(figure_dpi)
        or figure_dpi <= 0
    ):
        configuration_errors.append("figure_dpi must be a positive number.")

if configuration_errors:
    raise ValueError(
        "Please correct the file_map section:\n- "
        + "\n- ".join(configuration_errors)
    )

# Step 1: Pool signal_A per experimental group and sleep state
group_signals_A = {
    group: {sleep_score: [] for sleep_score in sleep_score_labels}
    for group in resolved_file_map
}
unscored_tail_summary = []

for group, file_paths in resolved_file_map.items():
    for mat_path in file_paths:
        data = loadmat(
            mat_path,
            variable_names=[
                signal_A_name,
                sleep_scores_name,
                signal_frequency_name,
            ],
        )
        A = np.asarray(data.get(signal_A_name, [])).ravel()
        sleep_scores = np.asarray(data.get(sleep_scores_name, [])).ravel()
        frequency_values = np.asarray(
            data.get(signal_frequency_name, [])
        ).ravel()

        if A.size == 0:
            print(f"Warning: {mat_path} has no '{signal_A_name}' data; skipping.")
            continue
        if sleep_scores.size == 0:
            print(f"Warning: {mat_path} has no '{sleep_scores_name}' data; skipping.")
            continue
        if frequency_values.size == 0:
            print(
                f"Warning: {mat_path} has no '{signal_frequency_name}' value; "
                "skipping."
            )
            continue

        signal_frequency = float(frequency_values[0])
        if not np.isfinite(signal_frequency) or signal_frequency <= 0:
            print(
                f"Warning: {mat_path} has invalid '{signal_frequency_name}' "
                f"value {signal_frequency}; skipping."
            )
            continue

        # sleep_scores contains one score per second. Assign each signal sample
        # to the corresponding scored second using the signal sampling rate.
        score_indices = np.floor(
            np.arange(A.size) / signal_frequency
        ).astype(np.int64)
        scored_samples = score_indices < sleep_scores.size
        aligned_A = A[scored_samples]
        aligned_sleep_scores = sleep_scores[score_indices[scored_samples]]

        unscored_sample_count = A.size - aligned_A.size
        if unscored_sample_count > 0:
            unscored_tail_summary.append(
                (mat_path.name, unscored_sample_count)
            )

        finite_scores = aligned_sleep_scores[np.isfinite(aligned_sleep_scores)]
        unknown_scores = np.setdiff1d(
            np.unique(finite_scores),
            np.array(list(sleep_score_labels)),
        )
        if unknown_scores.size > 0:
            print(
                f"Warning: ignored unknown sleep score(s) "
                f"{unknown_scores.tolist()} in {mat_path}."
            )

        for sleep_score in sleep_score_labels:
            stage_A = aligned_A[aligned_sleep_scores == sleep_score]
            if stage_A.size > 0:
                group_signals_A[group][sleep_score].append(stage_A)

if unscored_tail_summary:
    ignored_sample_count = sum(
        sample_count for _, sample_count in unscored_tail_summary
    )
    file_summary = ", ".join(
        f"{file_name}: {sample_count:,}"
        for file_name, sample_count in unscored_tail_summary
    )
    print(
        f"Note: ignored {ignored_sample_count:,} trailing "
        f"'{signal_A_name}' samples without sleep scores across "
        f"{len(unscored_tail_summary)} file(s): {file_summary}."
    )

for group, sleep_state_signals in group_signals_A.items():
    for sleep_score, pooled_signals in sleep_state_signals.items():
        pooled_A = (
            np.concatenate(pooled_signals)
            if pooled_signals
            else np.array([], dtype=float)
        )
        group_signals_A[group][sleep_score] = pooled_A
        print(
            f"{group} - {sleep_score_labels[sleep_score]}: "
            f"{pooled_A.size} signal samples"
        )

# Step 2: Global clipping range
all_A = [
    signal
    for sleep_state_signals in group_signals_A.values()
    for signal in sleep_state_signals.values()
    if signal.size > 0
]
if not all_A:
    raise ValueError("No signal data matched sleep scores 0, 1, 2, or 3.")

all_A = np.concatenate(all_A)
A_min, A_max = np.nanpercentile(all_A, [1, 99])

# Step 3: Prepare styling
colors = cycle(
    ["blue", "orange", "green"]
)  # C57 control = blue, SOD1 Control = orange, Sick = green
linestyles = cycle(["solid", "dashed", "dashdot", "dotted"])
group_styles = {
    group: (next(colors), next(linestyles))
    for group in group_signals_A
}

# Step 4: Plot
fig, axes = plt.subplots(
    len(sleep_score_labels),
    1,
    figsize=(7, 13),
    sharex=True,
    sharey=False,
)

for axis, (sleep_score, sleep_state) in zip(
    axes,
    sleep_score_labels.items(),
):
    plotted_group = False
    for group, sleep_state_signals in group_signals_A.items():
        signal = sleep_state_signals[sleep_score]
        if signal.size == 0:
            continue

        color, linestyle = group_styles[group]
        clipped = np.clip(signal, A_min, A_max)
        axis.hist(
            clipped,
            bins=50,
            range=(A_min, A_max),
            alpha=0.7,
            label=f"{group} (n={signal.size:,} signal samples)",
            density=True,
            histtype="step",
            color=color,
            linestyle=linestyle,
            linewidth=1.5,
        )
        plotted_group = True

    axis.set_title(f"{sleep_state} (sleep score {sleep_score})")
    axis.set_ylabel("Density")
    if plotted_group:
        axis.legend(fontsize="x-small")
    else:
        axis.text(
            0.5,
            0.5,
            "No matching samples",
            ha="center",
            va="center",
            transform=axis.transAxes,
        )

axes[-1].set_xlabel("Value")
fig.suptitle(
    f"Normalized Overlay of {signal_A_name} by Group and Sleep State"
)
plt.tight_layout(rect=(0, 0, 1, 0.97))

if save_figure:
    output_path = Path(figure_output_path).expanduser()
    if not output_path.is_absolute():
        output_path = script_directory / output_path
    if not output_path.suffix:
        output_path = output_path.with_suffix(".png")
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=figure_dpi, bbox_inches="tight")
    print(f"Saved figure: {output_path}")

if plt.get_backend().lower() != "agg":
    plt.show()
