from func import requests_init,saving_files,drop_duplicate,match_day_date,main_date,save_daily_csv,sorting_values
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time



def prematips_func():
    full_path = save_daily_csv()
    path = f'{full_path}/prematips.csv'
    _1x2url = f'https://primatips.com/tips/{main_date()}'
    ovrund_url = f'https://primatips.com/tips/{main_date()}/over-under-25'
    btsots_url = f'https://primatips.com/tips/{main_date()}/both-teams-to-score'
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
    for main_url in all_url:
        res = requests.get(main_url)
        soup = BeautifulSoup(res.content, 'html.parser')

        if main_url == _1x2url:
            match_time = [y.text for y in soup.find_all('span', class_='tm')]
            hm_team = [y.text.split('-')[0] for y in soup.find_all('span', class_='nms')]
            aw_team = [y.text.split('-')[-1] for y in soup.find_all('span', class_='nms')]
        #     print(match_time,hm_team,aw_team)

            per = [y.text for y in soup.find_all('span', class_='t')]
            hm_per = [per[y] for y in range(0,len(per),3)]
            draw_per = [per[y] for y in range(1,len(per),3)]
            aw_per = [per[y] for y in range(2,len(per),3)]
        #     print(hm_per, draw_per, aw_per)
           
            match_date =time.localtime() 
            _1x2data['DATE']= f'{match_date[0]}-{match_date[1]}-{match_date[2]}'
            _1x2data['TIME']= match_time
            _1x2data['HOME TEAM']= hm_team
            _1x2data['AWAY TEAM']= aw_team

            _1x2data['HOME PER']= hm_per
            _1x2data['DRAW PER']= draw_per
            _1x2data['AWAY PER']= aw_per

        elif main_url == ovrund_url:
            hm_team = [y.text.split('-')[0] for y in soup.find_all('span', class_='nms')]
            aw_team = [y.text.split('-')[-1] for y in soup.find_all('span', class_='nms')]

            per = [y.text for y in soup.find_all('span', class_='t2')]
            over_2_5 = [per[y] for y in range(0,len(per),2)]
            under_2_5 = [per[y] for y in range(1,len(per),2)]
        #     print(hm_team,aw_team,under_2_5,over_2_5)

            ovrund_data['HOME TEAM']= hm_team
            ovrund_data['AWAY TEAM']= aw_team

            ovrund_data['UNDER 2.5']= under_2_5
            ovrund_data['OVER 2.5']= over_2_5

        else:
            hm_team = [y.text.split('-')[0] for y in soup.find_all('span', class_='nms')]
            aw_team = [y.text.split('-')[-1] for y in soup.find_all('span', class_='nms')]

            per = [y.text for y in soup.find_all('span', class_='t2')]
            bts = [per[y] for y in range(0,len(per),2)]
            ots = [per[y] for y in range(1,len(per),2)]
        #     print(hm_team,aw_team,bts,ots)
            btsund_data['HOME TEAM']= hm_team
            btsund_data['AWAY TEAM']= aw_team
            btsund_data['BTS']= bts
            btsund_data['OTS']= ots
            btsund_data['NAME']= 'PREMA'
            

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

prematips_func()
