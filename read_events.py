# -*- coding: utf-8 -*-
"""
Created on Thu May  8 12:58:19 2025

@author: yzhao
"""

import os

import numpy as np
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt


def read_event_spreadsheet(event_file, fp_freq):
    df_events = pd.read_excel(event_file)
    df_events = df_events.dropna(axis=1, how='all')  # Drop columns with all NaNs
    df_events = df_events * fp_freq
    events = {col: df_events[col].dropna().round().astype(int).tolist() for col in df_events.columns}
    return events


def plot_perievent_signals(event, perievent_signals, nsec_before=60, nsec_after=60):
    event_count, seg_len = perievent_signals.shape
    
    # Time axis in seconds
    t = np.linspace(-nsec_before, nsec_after, seg_len)
    # Plot all signals in one plot
    plt.figure(figsize=(10, 6))
    for i in range(event_count):
        plt.plot(t, perievent_signals[i], label=f"Signal {i+1}")  # Offset vertically by 5 units for clarity
    
    # Add reference lines
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)  # Horizontal at y = 0
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)  # Vertical at x = 0
    plt.xlim(-nsec_before, nsec_after)
    plt.ylim(-10, 10)
    plt.xlabel("Time (s)", fontsize=14, fontweight='bold')
    plt.ylabel(f"{biosignal_name} (dF/F)", fontsize=14, fontweight='bold')
    plt.title(f"{fp_name}_{event}", fontsize=16, fontweight='bold')
    plt.tight_layout()
    return plt
    #plt.show()


def plot_mean_perievent_signals(event, perievent_signals, nsec_before=60, nsec_after=60):
    perievent_signals_mean = np.mean(perievent_signals, axis=0)
    seg_len = len(perievent_signals_mean)
    plt.figure(figsize=(10, 6))
    t = np.linspace(-nsec_before, nsec_after, seg_len)
    plt.plot(t, perievent_signals_mean)
    
    # Add reference lines
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)
    
    # Axis limits and labels
    plt.xlim(-nsec_before, nsec_after)
    plt.ylim(-10, 10)
    plt.xlabel("Time (s)", fontsize=14, fontweight='bold')
    plt.ylabel(f"mean {biosignal_name} (dF/F)", fontsize=14, fontweight='bold')
    plt.title(f"Mean_{fp_name}_{event}", fontsize=16, fontweight='bold')
    plt.tight_layout()
    return plt
    #plt.show()

def plot_perievent_heatmaps(event, perievent_signals, fp_freq, nsec_before=60, nsec_after=60):
    segment_size = round(fp_freq)
    time_sec = np.arange(nsec_before + nsec_after)
    start_indices = np.ceil(time_sec * fp_freq).astype(int)
    event_count, _ = perievent_signals.shape
    # Reshape start_indices to be a column vector (N, 1)
    start_indices = start_indices[:, np.newaxis]
    segment_array = np.arange(segment_size)
    # Use broadcasting to add the range_array to each start index
    indices = start_indices + segment_array
    perievent_signals_reshaped = perievent_signals[:, indices]
    perievent_signals_downsampled = np.mean(perievent_signals_reshaped, axis=-1)
    plt.figure(figsize=(10, 6))
    im = plt.imshow(
        perievent_signals_downsampled, 
        aspect='auto', 
        cmap='viridis', 
        origin='lower',
        extent=[-nsec_before, nsec_after, 0, event_count]
    )
    event_labels = [f"{i+1}" for i in range(event_count)]
    plt.yticks(np.arange(event_count) + 0.5, event_labels)
    plt.ylabel("Event Index", fontsize=14, fontweight='bold')
    plt.xlabel("Time (s)", fontsize=14, fontweight='bold')
    plt.title(f"{fp_name}_{event}", fontsize=16, fontweight='bold')
    plt.colorbar(im, label='(dF/F)')
    return plt

def make_perievent_segments(event_inds, fp_freq, nsec_before=60, nsec_after=60):
    window_segment = np.arange(round(-nsec_before*fp_freq), round((nsec_after+1)*fp_freq))
    perievent_segments = event_inds + window_segment
    return perievent_segments

#%%
DATA_PATH = "./data/"
fp_name = "F268"
fp_file = os.path.join(DATA_PATH, f"{fp_name}.mat")
fp_data = loadmat(fp_file, squeeze_me=True)
biosignal_names = fp_data["fp_signal_names"]
biosignal_name = 'NE2m'
biosignal = fp_data[biosignal_name]

event_file = os.path.join(DATA_PATH, "Transitions_F268.xlsx")
event = "sws_wake"
fp_freq = fp_data["fp_frequency"]
events = read_event_spreadsheet(event_file, fp_freq)
event_inds = np.array(events[event])
event_inds = np.expand_dims(event_inds, axis=1)
perievent_segments = make_perievent_segments(event_inds, fp_freq)
perievent_signals = biosignal[perievent_segments]

