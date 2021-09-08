"""
Created on Wed Sep 8 16:32:32 2021
@author: amali
"""


from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import time
import random
import json


# ===================================================================================================================== 
"""
Extracting the 200 Top Chess Players in the five classical modes : | bullet | blitz | rapid | classical | ultraBullet |
"""
# =====================================================================================================================

url = "https://lichess.org/player/top/200/"
mode_play = ['bullet','blitz','rapid','classical','ultraBullet']

results = {}

for play in mode_play :
    
    result = []
    
    page = urllib.request.urlopen(url+play)
    soup = BeautifulSoup(page, 'html.parser')
    
    # Checking the online and offline players
    online_players = soup.find_all('a',class_='online user-link ulpt')
    offline_players = soup.find_all('a',class_='offline user-link ulpt')
    
    for index in range(0,max(len(offline_players),len(online_players))) :
        
        if (0 <= index < len(offline_players)):
            
            result.append(offline_players[index].contents[-1])
            
        if (0 <= index < len(online_players)):
            
            result.append(online_players[index].contents[-1])
            
    results[play] = result

df = pd.DataFrame(results)
df.to_csv('./top200.csv',index=False)

# ================================================================
"""Clean Data & Extract unique Players in all 5 classical modes"""
# ================================================================

players = []

for result in results :
    
        tmp_players = results[result]
        
        for player in tmp_players :
            
            # the characters \xa0 stands for the title of the players like GM, FM,...
            tmp_player = player.replace('\xa0', '', 1) 
            
            if tmp_player not in players :
                
                players.append(tmp_player)

# ===========================================================================================
"""Webscrapping the players info : rating, wins, draws and losses in the 5 classical modes"""
# ===========================================================================================

url = 'https://lichess.org/@/'
results = {}

mode_play = ['bullet','blitz','rapid','classical','ultraBullet']


timer = 0
at_sleep_time = 200

for play in mode_play :
    
    results[play] = {}
    print("new mode",play)
    
    for player in players :
        
        # To avoid the overloading of the server, and eventually the crash, we will pause the execution sometimes

        if (timer==200) :

                sleep_time = random.randint(1, 30)
                print('Go to sleep')
                time.sleep(sleep_time)
                print('Wake up')
                timer = 0
        
        # Some players never played in some modes, so there is no records
        try :

            url_player = url+player+'/perf/'+play
            page = urllib.request.urlopen(url_player)
            soup = BeautifulSoup(page, 'html.parser')
            timer += 1

            results[play][player] = {}


            rating_tag = soup.find_all('section',class_='glicko')
            rating = rating_tag[0].h2.strong.contents[0]

            results[play][player]['rating'] = rating

            stats = soup.find_all('tr',class_='full')

            for element in stats :

                result = element.get_text(" ",strip=True)
                result = result.split(' ')

                if ('Victories'in result) or ('Draws'in result) or ('Defeats'in result) :

                    results[play][player][result[0]] = result[1]

        except :

            print(player + " Not found")
                
    with open('data_'+play+'.json', 'w') as fp:
        json.dump(results, fp,  indent=4)