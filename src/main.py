# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:43:41 2023

@author: Guilherme Theis
"""

## Import space
import re
import urllib
from time import sleep
import json
import pandas as pd
import numpy as np
from itertools import chain

## functions space
# This method finds the urls for each of the rosters in the NBA using regexes.

def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

def generate_player_info(rosters): # already cleans up a lot
    table_roster_init = pd.read_html(rosters)[0]
    table_roster_links_init = pd.read_html(rosters,extract_links='body')[0] 
    table_roster_links = table_roster_links_init['Name']
    names = []
    espn_links = []
    for i in range(len(table_roster_links)):
        names.append(table_roster_links[i][0])
        espn_links.append(str(table_roster_links[i][1]))
    names = remove(names)
    table_roster_dropped = (table_roster_init.copy())

    name_link_dict = {}

    for i in range(len(table_roster_links)):
        name_link_dict[names[i]] = espn_links[i]
        
    table_roster_dropped = table_roster_dropped.drop(['Unnamed: 0'], axis=1)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace('$', '',regex=True)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace('--', '0',regex=True)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].str.replace(',', '', regex=True)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].astype(int)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].replace(0, np.nan)
    table_roster_dropped.sort_values(by='Salary', inplace=True, ascending=False)
    table_roster_dropped['Salary'] = table_roster_dropped['Salary'].div(1e6).round(decimals=1)
    table_roster_dropped['Name'] = table_roster_dropped['Name'].str.replace('\d+', '',regex=True)
    table_roster_dropped = table_roster_dropped.reset_index(drop=True)
        
    return table_roster_dropped,name_link_dict

# scrape player information from rosters

with open('../data/teamsUrls.json') as infile:
    rosters = json.load(infile)

all_players_general = dict()
all_players_links = dict()
for team in rosters.keys():
    print("Gathering player info for team: " + team)
    all_players_general[team], all_players_links[team] = generate_player_info(rosters[team])
    
all_players_df = pd.DataFrame()
for team in all_players_general.keys():
    team_df = all_players_general[team]
    team_df['team'] = team
    all_players_df = all_players_df.append(team_df)

all_players_df = all_players_df.reset_index(drop=True)#reset all indexes
all_players_df.to_csv('../data/general_info_players.csv')


print ("Now gathering career stats on all players (may take a while):")


career_stats_df = pd.DataFrame()
for index, row in all_players_df.iterrows():
    url = re.sub(r'(/player/)', r'\1stats/', all_players_links[row['team']][row['Name']])
    if len(pd.read_html(url)) > 2:
        career_stats_df = career_stats_df.append(pd.read_html(url)[1].iloc[-2])
    else:
        pass

