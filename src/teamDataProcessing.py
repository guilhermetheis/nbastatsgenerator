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
listStats = ['3P%','3PTA','3PTM','AST','BLK','DR','FG%','FGA','FGM','FT%','FTA','FTM','GP','GS','MIN','OR','PF','PTS','REB','STL','Team','TO']
# Get the list of JSON files in the directory
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

for json_file in json_files:
    with open(os.path.join(json_dir, json_file), 'r') as f:
        player_stats = json.load(f)
        playe_statsDF = pd.json_normalize(player_stats, 'Name', listStats)
