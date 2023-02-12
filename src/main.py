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
from itertools import chain

## functions space
# This method finds the urls for each of the rosters in the NBA using regexes.

def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

def generate_player_info(rosters):
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
        
    return table_roster_dropped,name_link_dict

# scrape player information from rosters

with open('../data/teamsUrls.json') as infile:
    rosters = json.load(infile)

all_players_general = dict()
all_players_liks = dict()
for team in rosters.keys():
    print("Gathering player info for team: " + team)
    all_players_general[team], all_players_liks[team] = generate_player_info(rosters[team])