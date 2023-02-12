# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 08:44:17 2023

@author: Guilherme Theis
"""

import re
import urllib
import json

# This method finds the urls for each of the rosters in the NBA using regexes.
def build_team_urls():
    # Open the espn teams webpage and extract the names of each roster available.
    f = urllib.request.urlopen('https://www.espn.com/nba/teams')
    teams_source = f.read().decode('utf-8')
    teams = dict(re.findall("www\.espn\.com/nba/team/_/name/(\w+)/(.+?)\",", teams_source))
    # Using the names of the rosters, create the urls of each roster
    roster_urls = []
    for key in teams.keys():
        # each roster webpage follows this general pattern.
        roster_urls.append('https://www.espn.com/nba/team/roster/_/name/' + key + '/' + teams[key])
        teams[key] = str(teams[key])
    return dict(zip(teams.values(), roster_urls))

rosters = build_team_urls()

with open('../data/teamsUrls.json', 'w') as fp:
    json.dump(rosters,fp)