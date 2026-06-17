# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 13:42:16 2025

@author: yzhao
"""

import os
    
import numpy as np
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt


def get_sleep_segments(sleep_scores):
    transition_indices = np.flatnonzero(np.diff(sleep_scores))
    transition_indices = np.append(transition_indices, len(sleep_scores) - 1)

    REM_end_indices = np.flatnonzero(sleep_scores[transition_indices] == 2)
    REM_start_indices = REM_end_indices - 1
    REM_end_indices = transition_indices[REM_end_indices]
    REM_start_indices = transition_indices[REM_start_indices] + 1

    wake_end_indices = np.flatnonzero(sleep_scores[transition_indices] == 0)
    wake_start_indices = wake_end_indices - 1
    wake_end_indices = transition_indices[wake_end_indices]
    wake_start_indices = transition_indices[wake_start_indices] + 1

    SWS_end_indices = np.flatnonzero(sleep_scores[transition_indices] == 1)
    SWS_start_indices = SWS_end_indices - 1
    SWS_end_indices = transition_indices[SWS_end_indices]
    SWS_start_indices = transition_indices[SWS_start_indices] + 1

    df_rem = pd.DataFrame()
    df_rem["sleep_scores"] = pd.Series(np.array([2] * REM_end_indices.size))
    df_rem["start"] = pd.Series(REM_start_indices)
    df_rem["end"] = pd.Series(REM_end_indices)

    df_wake = pd.DataFrame()
    df_wake["sleep_scores"] = pd.Series(np.array([0] * wake_end_indices.size))
    df_wake["start"] = pd.Series(wake_start_indices)
    df_wake["end"] = pd.Series(wake_end_indices)

    df_SWS = pd.DataFrame()
    df_SWS["sleep_scores"] = pd.Series(np.array([1] * SWS_end_indices.size))
    df_SWS["start"] = pd.Series(SWS_start_indices)
    df_SWS["end"] = pd.Series(SWS_end_indices)

    frames = [df_rem, df_wake, df_SWS]
    df = pd.concat(frames)
    df = df.sort_values(by=["end"], ignore_index=True)
    df.at[0, "start"] = 0
    df["duration"] = df["end"] - df["start"] + 1
    return df

def get_medians(*args):
    medians = [np.median(sleep_stage_values) for sleep_stage_values in args]
    return medians

def get_means(*args):
    means = [np.mean(sleep_stage_values) for sleep_stage_values in args]
    return means

def get_variances(*args):
    variances = [np.var(sleep_stage_values) for sleep_stage_values in args]
    return variances

def get_standard_deviations(*args):
    standard_deviations = [np.std(sleep_stage_values) for sleep_stage_values in args]
    return standard_deviations

def plot_hist(wake_values, sws_values, rem_values, title="", bins=None):
    if bins is None:
        bins = np.linspace(-10, 10, 41)
        
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(12, 6))
    axes[0].hist(wake_values, bins, density=True, edgecolor='black')
    axes[0].title.set_text('Wake')
    axes[0].set_ylabel("Density")
    axes[1].hist(sws_values, bins, density=True, edgecolor='black')
    axes[1].title.set_text('SWS')
    axes[1].set_ylabel("Density")
    axes[2].hist(rem_values, bins, density=True, edgecolor='black')
    axes[2].title.set_text('REM')
    axes[2].set_xlabel("Signal Value")
    axes[2].set_ylabel("Density")
    #fig.tight_layout()
    fig.suptitle(title)
    #plt.show()
    return fig
#%%
DATA_PATH = "./data/"

mat_file = "F268.mat"
#mat_file = "F268_FP-Data_sdreamer_post.mat"
fp_channel = "signal_a"
mat = loadmat(os.path.join(DATA_PATH, mat_file))
sleep_scores = mat.get("sleep_scores").flatten()
#sleep_scores = mat.get("pred_labels").flatten()
fp_signal = mat.get(fp_channel).flatten()
fp_frequency = None
if fp_signal is not None:
    fp_signal = fp_signal.flatten()
    if len(fp_signal) > 1:
        fp_frequency = mat.get("fp_frequency").item()

df = get_sleep_segments(sleep_scores)

#%%

MA_indices = np.flatnonzero(
    (df["sleep_scores"] == 0) & (df["duration"] < 15)
)
df.loc[MA_indices, "sleep_scores"] = 3

total_durations = df.groupby('sleep_scores')['duration'].sum()
# Find the class with the maximum total duration
prevalent_class = total_durations.idxmax()

df_wake = df[df["sleep_scores"] == 0]
df_sws = df[df["sleep_scores"] == 1]
df_rem = df[df["sleep_scores"] == 2]
df_ma = df[df["sleep_scores"] == 3]

#%%
wake_indices = np.concatenate([np.arange(round(start*fp_frequency), round((end+1)*fp_frequency)) for start, end in zip(df_wake["start"], df_wake["end"])])
sws_indices = np.concatenate([np.arange(round(start*fp_frequency), round((end+1)*fp_frequency)) for start, end in zip(df_sws["start"], df_sws["end"])])
rem_indices = np.concatenate([np.arange(round(start*fp_frequency), round((end+1)*fp_frequency)) for start, end in zip(df_rem["start"], df_rem["end"])])
ma_indices = np.concatenate([np.arange(round(start*fp_frequency), round((end+1)*fp_frequency)) for start, end in zip(df_ma["start"], df_ma["end"])])

wake_indices = wake_indices[wake_indices<fp_signal.size]
sws_indices = sws_indices[sws_indices<fp_signal.size]
rem_indices = rem_indices[rem_indices<fp_signal.size]
ma_indices = ma_indices[ma_indices<fp_signal.size]

ne_wake = fp_signal[wake_indices]
ne_sws = fp_signal[sws_indices]
ne_rem = fp_signal[rem_indices]
ne_ma = fp_signal[ma_indices]

medians = get_medians(ne_wake, ne_sws, ne_rem)
median = medians[prevalent_class]
means = get_means(ne_wake, ne_sws, ne_rem)
variances = get_variances(ne_wake, ne_sws, ne_rem)
standard_deviations = get_standard_deviations(ne_wake, ne_sws, ne_rem)

ne_wake_diff = ne_wake - median
ne_sws_diff = ne_sws - median
ne_rem_diff = ne_rem - median
means_diff = get_means(ne_wake_diff, ne_sws_diff, ne_rem_diff)
variances_diff = get_variances(ne_wake_diff, ne_sws_diff, ne_rem_diff)
standard_deviations_diff = get_standard_deviations(ne_wake_diff, ne_sws_diff, ne_rem_diff)

#%%

title = f"{mat_file.strip('.mat')} - {fp_channel}"
plot_hist(ne_wake, ne_sws, ne_rem, title=title)
plot_hist(ne_wake_diff, ne_sws_diff, ne_rem_diff, title=title+"_normalized")