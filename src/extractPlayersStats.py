# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:43:41 2023

@author: Guilherme Theis
"""

## Import space
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime
import time


start = time.time() # check time elapsed
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

with open('data/teamsUrls.json') as infile:
    rosters = json.load(infile)

all_players_general = dict()
all_players_links = dict()
for team in rosters.keys():
    print('Gathering player info for team: ' + team)
    all_players_general[team], all_players_links[team] = generate_player_info(rosters[team])
    
all_players_df = pd.DataFrame()
for team in all_players_general.keys():
    team_df = all_players_general[team]
    team_df['team'] = team
    all_players_df = all_players_df.append(team_df)

all_players_df = all_players_df.reset_index(drop=True)#reset all indexes
all_players_df.to_json('data/general_info_players.json')


print('Now gathering career stats on all players (may take a while):')


career_stats_df = pd.DataFrame(columns = ['Name', 'Team' 'GP','GS','MIN','FGM', 'FGA','FG%','3PTM','3PTA','3P%','FTM','FTA','FT%','OR','DR','REB','AST','BLK','STL','PF','TO','PTS'])

career_stats_df = pd.DataFrame() # make this a function. Can add advanced, totals, carrers. 
stats = []
for index, row in all_players_df.iterrows():
    url = re.sub(r'(/player/)', r'\1stats/', all_players_links[row['team']][row['Name']])
    if len(pd.read_html(url)) > 2:
        career_stats = pd.read_html(url)[1].iloc[-2]
        stats.append({
            'Name': row['Name'],
            'Team': row['team'],
            'GP': float(career_stats['GP']),
            'GS': float(career_stats['GS']),
            'MIN': float(career_stats['MIN']),
            'FGM': float(career_stats['FG'].split('-')[0]),
            'FGA': float(career_stats['FG'].split('-')[1]),
            'FG%': float(career_stats['FG%']),
            '3PTM': float(career_stats['3PT'].split('-')[0]),
            '3PTA': float(career_stats['3PT'].split('-')[1]),
            '3P%': float(career_stats['3P%']),
            'FTM': float(career_stats['FT'].split('-')[0]),
            'FTA': float(career_stats['FT'].split('-')[1]),
            'FT%': float(career_stats['FT%']),
            'OR': float(career_stats['OR']),
            'DR': float(career_stats['DR']),
            'REB': float(career_stats['REB']),
            'AST': float(career_stats['AST']),
            'BLK': float(career_stats['BLK']),
            'STL': float(career_stats['STL']),
            'PF': float(career_stats['PF']),
            'TO': float(career_stats['TO']),
            'PTS': float(career_stats['PTS']),
            })
        
    else:
        stats.append({
            'Name': row['Name'],
            'Team': row['team'],
            'GP': np.nan,
            'GS': np.nan,
            'MIN': np.nan,
            'FGM': np.nan,
            'FGA': np.nan,
            'FG%': np.nan,
            '3PTM': np.nan,
            '3PTA': np.nan,
            '3P%': np.nan,
            'FTM': np.nan,
            'FTA': np.nan,
            'FT%': np.nan,
            'OR': np.nan,
            'DR': np.nan,
            'REB': np.nan,
            'AST': np.nan,
            'BLK': np.nan,
            'STL': np.nan,
            'PF': np.nan,
            'TO': np.nan,
            'PTS': np.nan,
            })

regularSeasonStats = pd.DataFrame(stats)




print('Creating json files:')

regularSeasonStats.to_json('data/allTeams/'+ datetime.today().strftime('%d-%m-%Y') + '.json')

for squad, n_df in regularSeasonStats.groupby('Team'):
    n_df.to_json('data/'+squad.split(r'-')[0]+squad.split(r'-')[1]+'/'+ datetime.today().strftime('%d-%m-%Y') + '.json')
    
    
end = time.time()
print('Time elapsed = ' + str(end - start) + ' seconds')
