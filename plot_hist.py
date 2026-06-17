# -*- coding: utf-8 -*-
"""
Created on Thu May 22 00:01:40 2025

@author: yzhao
"""

import os

import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt


pre_score0_dir = "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1_21-10-24_Score0_Presymptomatic"
score0_week22_dir = "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1_18-2-2025_Score0_Week_22"
score1_week26_dir = "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1-Score1_20-3-2025_Week_26"
score3_4_dir = "C:/Users/yzhao/python_projects/fp_post_analysis/data/SOD1-Score3-4_27-3-2025"

file_map = {
    pre_score0_dir: ["M1.mat", "M7.mat", "M11.mat"],
    score0_week22_dir: ["m92_105427.mat", "m92_110131.mat", "m92_110731.mat", "m95_142003.mat", "m95_142540"],
    score1_week26_dir: ["m88_of1.mat", "m88_of2.mat", "m88_of3.mat"],
    score3_4_dir: ["m88_103532.mat", "m88_104058.mat", "m88_104800.mat"]
}

#%%
#mat = loadmat(os.path.join(pre_score0_dir, "M1.mat"), squeeze_me=True)
# Step 1: Compute global value ranges (1st–99th percentile) for signal_A and signal_C
all_signal_A = []
all_signal_C = []

for dir_path, filenames in file_map.items():
    for fname in filenames:
        mat_path = os.path.join(dir_path, fname if fname.endswith(".mat") else fname + ".mat")
        data = loadmat(mat_path)
        A = data.get("signal_A", []).ravel()
        C = data.get("signal_C", []).ravel()
        if A.size > 0: all_signal_A.append(A)
        if C.size > 0: all_signal_C.append(C)

signal_A_all = np.concatenate(all_signal_A)
signal_C_all = np.concatenate(all_signal_C)

# Global value range for plotting: clip to 1st–99th percentile
A_min, A_max = np.percentile(signal_A_all, [1, 99])
C_min, C_max = np.percentile(signal_C_all, [1, 99])

# Step 2: Generate histograms for each file
for dir_path, filenames in file_map.items():
    for fname in filenames:
        mat_path = os.path.join(dir_path, fname if fname.endswith(".mat") else fname + ".mat")
        data = loadmat(mat_path)
        signal_A = data.get("signal_A", []).ravel()
        signal_C = data.get("signal_C", []).ravel()

        # Clip outliers to improve resolution
        signal_A_clipped = np.clip(signal_A, A_min, A_max)
        signal_C_clipped = np.clip(signal_C, C_min, C_max)

        # Plot
        plt.figure(figsize=(6, 8))

        plt.subplot(2, 1, 1)
        plt.hist(signal_A_clipped, bins=50, range=(A_min, A_max), edgecolor='black', facecolor='skyblue')
        plt.title("signal_A")
        plt.xlabel("Value")
        plt.ylabel("Frequency")

        plt.subplot(2, 1, 2)
        plt.hist(signal_C_clipped, bins=50, range=(C_min, C_max), edgecolor='black', facecolor='skyblue')
        plt.title("signal_C")
        plt.xlabel("Value")
        plt.ylabel("Frequency")

        plt.tight_layout()

        base_name = os.path.splitext(fname)[0]
        save_path = os.path.join(dir_path, base_name + "_hist.png")
        plt.savefig(save_path, dpi=200)
        plt.close()
