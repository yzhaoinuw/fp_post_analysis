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
#file_map = {
 #   'H:/CTN/FP and Opto/FP with EEG and EMG/Send to Fazla/Brain/Control': [
  #      "CtrlSOD1_M130_2025-06-10_09-54-55-532_PMC-sleepscored.mat",
   #     "C57M1_2025-06-11_11-18-19-341_PMC_sleepscored.mat",
    #    "C57M2_2025-06-11_11-18-19-341_PMC-sleepscored.mat",
     #   "CtrlSOD1_M126_2025-06-10_09-54-55-532_PMC-sleepscored_new.mat"
      #  ],
    #'H:/CTN/FP and Opto/FP with EEG and EMG/Send to Fazla/Brain/Sick': [
     #   "SOD1_M194_sleep_2025-10-17_08-31-52-368_PMC-sleepscored.mat",
      #  "SOD1M164Score3_2025-07-14_10-05-28-148_PMC_sleepscored.mat",
       # "SOD1M175SCORE4SLEEP_2025-07-22_11-15-32-993_PMC-sleepscored-reana.mat"
        #]
  
file_map = {
        r'H:\CTN\FP and Opto\FP with EEG and EMG\Send to Fazla\Brain\18May2026_REM_to_NREM check_FINAL\BS\C57_Control': [ 
           "C57M1_2025-06-11_11-18-19-341_BS_sleepscored_18May2026.mat",
            "C57M2_2025-06-11_11-18-19-341_BS-sleepscored_18May2026.mat"
            ],
        r'H:\CTN\FP and Opto\FP with EEG and EMG\Send to Fazla\Brain\18May2026_REM_to_NREM check_FINAL\BS\SOD1_Control': [ 
           "CtrlSOD1_M126_2025-06-10_09-54-55-532_BS-sleepscored.mat",
            "CtrlSOD1_M130_2025-06-10_09-54-55-532_BS-sleepscored.mat"
            ],
        r'H:\CTN\FP and Opto\FP with EEG and EMG\Send to Fazla\Brain\18May2026_REM_to_NREM check_FINAL\BS\SOD1_Sick': [
            "SOD1_M194_sleep_2025-10-17_08-31-52-368-BS_sleepscored.mat",
            "SOD1M164Score3_2025-07-14_10-05-28-148_BS-sleepscored_18May2026.mat",
            "SOD1M175SCORE4SLEEP_2025-07-22_11-15-32-993_BS-sleepscore.mat"
            ]
        
    
    #"./data/SOD1_21-10-24_Score0_Presymptomatic": ["M1.mat", "M7.mat", "M11.mat"],
    #"./data/SOD1_18-2-2025_Score0_Week_22": ["m92_105427.mat", "m92_110131.mat", "m92_110731.mat", "m95_142003.mat", "m95_142540"],
    #"./data/SOD1-Score1_20-3-2025_Week_26": ["m88_of1.mat", "m88_of2.mat", "m88_of3.mat"],
    #"./data/SOD1-Score3-4_27-3-2025": ["m88_103532.mat", "m88_104058.mat", "m88_104800.mat"]
}
signal_A_name = "ne"

#%%
# Step 1: Pool signal_A and signal_C per group
group_signals_A = {}

for dir_path, filenames in file_map.items():
    pooled_A = []
    for fname in filenames:
        mat_path = os.path.join(dir_path, fname if fname.endswith(".mat") else fname + ".mat")
        data = loadmat(mat_path)
        A = data.get(signal_A_name, []).ravel()
      
        if A.size > 0:
            pooled_A.append(A)
    group_signals_A[dir_path] = np.concatenate(pooled_A)

# Step 2: Global clipping range
all_A = np.concatenate(list(group_signals_A.values()))
A_min, A_max = np.nanpercentile(all_A, [1, 99])

# Step 3: Prepare styling
#colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])  # default matplotlib colors
colors = cycle(['blue', 'orange', 'green'])  # C57 control = blue, SOD1 Control = Orange, Sick = green
linestyles = cycle(['solid', 'dashed', 'dashdot', 'dotted'])  # different line styles

# Step 4: Plot
plt.figure(figsize=(6, 8))

# signal_A normalized overlay
plt.subplot(1, 1, 1)
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



plt.tight_layout()
#plt.savefig("group_overlay_hist_normalized.png", dpi=300)
#plt.close()
