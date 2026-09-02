import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path('data')

REGIONS = {
    'CR2b': '2b_control_region_only',
    'SR2b': '2b_signal_region_only',
    'CR3b': '3b_control_region_only',
    'SR3b': '3b_signal_region_only',
    'CR4b': '4b_control_region_only',
    'SR4b': '4b_signal_region_only',
}
ERA_FILES = ['data_2022EE.root', 'data_2022preEE.root']
VAR = 'HT'
BINS = np.linspace(200, 1200, 40)

data = {}
for name, folder in REGIONS.items():
    dfs = []
    for era_file in ERA_FILES:
        path = DATA_DIR / folder / era_file
        tree = uproot.open(path)['tree']
        dfs.append(tree.arrays([VAR], library='pd'))
    data[name] = pd.concat(dfs, ignore_index=True)

fig, ax = plt.subplots(figsize=(7, 5))
for name in ['CR2b', 'CR3b', 'CR4b']:
    ax.hist(data[name][VAR], bins=BINS, density=True, histtype='step', linewidth=1.8, label=name)

ax.set_xlabel(f'{VAR} [GeV]')
ax.set_ylabel('a.u. (normalized)')
ax.legend()
fig.savefig('ht_distribution.png', dpi=150)