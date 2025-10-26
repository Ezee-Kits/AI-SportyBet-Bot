from importlib.resources import path
from func import drop_duplicate,save_daily_csv,match_day_date
from bs4 import BeautifulSoup
import requests
import pandas as pd

def footballsupertips_func():
    full_path = save_daily_csv()
    path = f'{full_path}/footballsupertips.csv'

    _1x2url = 'https://www.footballsuper.tips/todays-free-football-super-tips/'
    ovrund_url = 'https://www.footballsuper.tips/todays-over-under-football-super-tips/'
    btsots_url = 'https://www.footballsuper.tips/todays-both-teams-to-score-football-super-tips/'
    all_url = [_1x2url,ovrund_url,btsots_url]
    

    _1x2data = {
            'DATE':[],
            'TIME':[],

            'HOME TEAM': [],
            'AWAY TEAM': [],

            'HOME PER':[],
            'DRAW PER':[],
            'AWAY PER':[]}

    ovrund_data = {

            'HOME TEAM': [],
            'AWAY TEAM': [],

            'UNDER 2.5':[],
            'OVER 2.5':[]
            }
    btsund_data = {
            'HOME TEAM': [],
            'AWAY TEAM': [],

            'BTS':[],
            'OTS':[],
            'NAME':[]
            }
    for x in all_url:
        res = requests.get(x)
        soup = BeautifulSoup(res.content, 'html.parser')

        if x == _1x2url:
            date = [y.text.split()[0] for y in soup.find_all('div', class_='datedisp')]
            time = [y.text.split()[1] for y in soup.find_all('div', class_='datedisp')]
            hm_team = [y.text for y in soup.find_all('div', class_='homedisp')]
            aw_team = [y.text for y in soup.find_all('div', class_='awaydisp')]

            # per = [y.text.split()[0] for y in soup.find_all('div', class_='percdiv')]
            hm_per = [y.text.split()[0].replace('%','') for y in soup.find_all('div', class_='percdiv')]
            draw_per =[y.text.split()[1].replace('%','') for y in soup.find_all('div', class_='percdiv')]
            aw_per = [y.text.split()[2].replace('%','') for y in soup.find_all('div', class_='percdiv')]
            # print(hm_per,draw_per,aw_per)
            _1x2data['DATE']= date
            _1x2data['TIME']= time
            _1x2data['HOME TEAM']= hm_team
            _1x2data['AWAY TEAM']= aw_team

            _1x2data['HOME PER']= hm_per
            _1x2data['DRAW PER']= draw_per
            _1x2data['AWAY PER']= aw_per

        elif x == ovrund_url:
            hm_team = [y.text for y in soup.find_all('div', class_='homedisp')]
            aw_team = [y.text for y in soup.find_all('div', class_='awaydisp')]

            over_2_5 = [y.text.split()[0].replace('%','') for y in soup.find_all('div', class_='percdiv')]
            under_2_5 = [y.text.split()[1].replace('%','') for y in soup.find_all('div', class_='percdiv')]

            ovrund_data['HOME TEAM']= hm_team
            ovrund_data['AWAY TEAM']= aw_team

            ovrund_data['UNDER 2.5']= under_2_5
            ovrund_data['OVER 2.5']= over_2_5

        else:
            hm_team = [y.text for y in soup.find_all('div', class_='homedisp')]
            aw_team = [y.text for y in soup.find_all('div', class_='awaydisp')]

            bts = [y.text.split()[0].replace('%','') for y in soup.find_all('div', class_='percdiv')]
            ots = [y.text.split()[1].replace('%','') for y in soup.find_all('div', class_='percdiv')]

            btsund_data['HOME TEAM']= hm_team
            btsund_data['AWAY TEAM']= aw_team
            btsund_data['BTS']= bts
            btsund_data['OTS']= ots
            btsund_data['NAME']= 'FST'
    df1 = pd.DataFrame(_1x2data)
    df2 = pd.DataFrame(ovrund_data)
    df3 = pd.DataFrame(btsund_data)
    # print(df1.to_string())
    # print(df2.to_string())  
    # print(df3.to_string())
    all_df = pd.merge(df1, df2, on=['HOME TEAM', 'AWAY TEAM'], how='inner')
    all_df = pd.merge(all_df, df3, on=['HOME TEAM', 'AWAY TEAM'], how='inner')
    print(all_df)
    all_df.to_csv(path, index=False)
    print('============================= FIRST FILE SAVED ==========================')
    drop_duplicate(path=path)

footballsupertips_func()