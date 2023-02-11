# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 15:43:41 2023

@author: Guilherme Theis
"""

## Import space
import pandas as pd
import numpy as np
import re
from datetime import datetime
from pytz import timezone
#from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

#load_dotenv()

# LUT

#listOfTeams = {'https://www.espn.com/nba/team/roster/_/name/bos/boston-celtics'}

#for urls in listOfTeams:
 #   table_roster_init = pd.read_html(urls)[0]  
    
r = requests.get('https://www.espn.com/nba/player/_/id/2566769/malcolm-brogdon')
source = r.content
soup = BeautifulSoup(r.content, 'lxml') 

altlinks = []
imgalt_list = {"Malcolm Brogdon"}

for x in soup.find_all('img', alt= True): #we find all img alt names
    #print(x)
    if x['alt'] in imgalt_list and x['data-mptype'] == "image": #if alt name matchs with your numbers
        print(x)
        #altlinks.append(x.get('src')) #adding into list
#print(altlinks)
