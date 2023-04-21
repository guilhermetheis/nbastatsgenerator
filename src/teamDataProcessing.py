# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 11:34:22 2023

@author: Guilherme
"""


# imports

import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# Directory where the JSON files are located
json_dir = 'data/bostonceltics'  # Update with your actual directory path

# Get the list of JSON files in the directory
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
data = []
for json_file in json_files:
    with open(os.path.join(json_dir, json_file), 'r') as f:
        player_stats = pd.read_json(f,keep_default_dates=True)
        player_stats = player_stats.pivot(index='Date', columns='Name', values='PTS')
        data.append(player_stats)
        
df = pd.concat(data, axis=0)
df.plot()
plt.show()
