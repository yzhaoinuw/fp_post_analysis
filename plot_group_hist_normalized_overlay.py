# -*- coding: utf-8 -*-
"""
Created on Thu May 22 01:16:39 2025

@author: yzhao
"""

import os
from itertools import cycle

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

#%% Change inside this section as needed
file_map = {
    "./data/SOD1_21-10-24_Score0_Presymptomatic": ["M1.mat", "M7.mat", "M11.mat"],
    "./data/SOD1_18-2-2025_Score0_Week_22": ["m92_105427.mat", "m92_110131.mat", "m92_110731.mat", "m95_142003.mat", "m95_142540"],
    "./data/SOD1-Score1_20-3-2025_Week_26": ["m88_of1.mat", "m88_of2.mat", "m88_of3.mat"],
    "./data/SOD1-Score3-4_27-3-2025": ["m88_103532.mat", "m88_104058.mat", "m88_104800.mat"]
}
signal_A_name = "signal_A"
signal_C_name = "signal_C"

#%%
# Step 1: Pool signal_A and signal_C per group
group_signals_A = {}
group_signals_C = {}

for dir_path, filenames in file_map.items():
    pooled_A = []
    pooled_C = []
    for fname in filenames:
        mat_path = os.path.join(dir_path, fname if fname.endswith(".mat") else fname + ".mat")
        data = loadmat(mat_path)
        A = data.get(signal_A_name, []).ravel()
        C = data.get(signal_C_name, []).ravel()
        if A.size > 0:
            pooled_A.append(A)
        if C.size > 0:
            pooled_C.append(C)
    group_signals_A[dir_path] = np.concatenate(pooled_A)
    group_signals_C[dir_path] = np.concatenate(pooled_C)

# Step 2: Global clipping range
all_A = np.concatenate(list(group_signals_A.values()))
all_C = np.concatenate(list(group_signals_C.values()))
A_min, A_max = np.percentile(all_A, [1, 99])
C_min, C_max = np.percentile(all_C, [1, 99])

# Step 3: Prepare styling
colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])  # default matplotlib colors
linestyles = cycle(['solid', 'dashed', 'dashdot', 'dotted'])  # different line styles

# Step 4: Plot
plt.figure(figsize=(6, 8))

# signal_A normalized overlay
plt.subplot(2, 1, 1)
for dir_path, signal in group_signals_A.items():
    color = next(colors)
    linestyle = next(linestyles)
    clipped = np.clip(signal, A_min, A_max)
    label = os.path.basename(dir_path)
    plt.hist(clipped, bins=50, range=(A_min, A_max), alpha=0.7, label=label,
             density=True, histtype='step', color=color, linestyle=linestyle, linewidth=1.5)

plt.title(f"Normalized Overlay of {signal_A_name} by Group")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend(fontsize='x-small')

# Reset style iterators
colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
linestyles = cycle(['solid', 'dashed', 'dashdot', 'dotted'])

# signal_C normalized overlay
plt.subplot(2, 1, 2)
for dir_path, signal in group_signals_C.items():
    color = next(colors)
    linestyle = next(linestyles)
    clipped = np.clip(signal, C_min, C_max)
    label = os.path.basename(dir_path)
    plt.hist(clipped, bins=50, range=(C_min, C_max), alpha=0.7, label=label,
             density=True, histtype='step', color=color, linestyle=linestyle, linewidth=1.5)

plt.title(f"Normalized Overlay of {signal_C_name} by Group")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend(fontsize='x-small')

plt.tight_layout()
#plt.savefig("group_overlay_hist_normalized.png", dpi=300)
#plt.close()
