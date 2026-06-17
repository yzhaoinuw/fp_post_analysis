# -*- coding: utf-8 -*-
"""
Created on Thu May 22 01:29:49 2025

@author: yzhao
"""

import os

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


file_map = {
    "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1_21-10-24_Score0_Presymptomatic": ["M1.mat", "M7.mat", "M11.mat"],
    "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1_18-2-2025_Score0_Week_22": ["m92_105427.mat", "m92_110131.mat", "m92_110731.mat", "m95_142003.mat", "m95_142540"],
    "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1-Score1_20-3-2025_Week_26": ["m88_of1.mat", "m88_of2.mat", "m88_of3.mat"],
    "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1-Score3-4_27-3-2025": ["m88_103532.mat", "m88_104058.mat", "m88_104800.mat"]
}

# Step 1: Pool signals per group
group_signals_A = {}
group_signals_C = {}

for dir_path, filenames in file_map.items():
    pooled_A = []
    pooled_C = []
    for fname in filenames:
        mat_path = os.path.join(dir_path, fname if fname.endswith(".mat") else fname + ".mat")
        data = loadmat(mat_path)
        A = data.get("signal_A", []).ravel()
        C = data.get("signal_C", []).ravel()
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

# Step 3: Plot (rows = groups, cols = [signal_A, signal_C])
n_groups = len(file_map)
fig, axes = plt.subplots(n_groups, 2, figsize=(12, 3.2 * n_groups), sharex='col', sharey='col')

for i, (dir_path, _) in enumerate(file_map.items()):
    group_name = os.path.basename(dir_path)
    
    # signal_A (left column)
    ax_A = axes[i, 0] if n_groups > 1 else axes[0]
    signal_A = np.clip(group_signals_A[dir_path], A_min, A_max)
    ax_A.hist(signal_A, bins=50, range=(A_min, A_max), density=True,
              edgecolor='black', facecolor='steelblue')
    ax_A.set_ylabel("Density")
    
    fig.text(
        ax_A.get_position().x0 - 0.04,
        ax_A.get_position().y0 + ax_A.get_position().height / 2,
        os.path.basename(dir_path),
        va='center', 
        ha='right', 
        fontsize='small', 
        rotation=90
    )
    
    if i == n_groups - 1:
        ax_A.set_xlabel("signal_A")

    # signal_C (right column)
    ax_C = axes[i, 1] if n_groups > 1 else axes[1]
    signal_C = np.clip(group_signals_C[dir_path], C_min, C_max)
    ax_C.hist(signal_C, bins=50, range=(C_min, C_max), density=True,
              edgecolor='black', facecolor='indianred')
    if i == n_groups - 1:
        ax_C.set_xlabel("signal_C")

# Add column titles
axes[0, 0].set_title("Normalized signal_A")
axes[0, 1].set_title("Normalized signal_C")

plt.tight_layout(rect=[0.1, 0.03, 1, 1])
#plt.savefig("group_histograms_vertical_by_signal.png", dpi=300)
#plt.close()
