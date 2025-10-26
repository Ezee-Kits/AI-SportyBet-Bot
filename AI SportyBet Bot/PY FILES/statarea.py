
from func import saving_files,save_daily_csv,sorting_values,match_day_date,drop_duplicate
from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests


def getting_tmr_match(data,match_date):
    url = 'https://www.statarea.com/predictions/date/' + str(match_date) + '/competition'

    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    def_match_date = str(match_date)
    for one_match_info in soup.find_all('div',class_ = 'match'):

        def_match_time = one_match_info.find('div',class_ = 'date').text.strip()
        def_host_team = one_match_info.find('div',class_ = 'hostteam').find('div',class_ = 'name').text.strip()
        def_guess_team = one_match_info.find('div',class_ = 'guestteam').find('div',class_ = 'name').text.strip()
        def_pred_list = []
        for all_pred_value in  one_match_info.find('div',class_ = 'inforow').find('div',class_ = 'coefrow').find_all('div',class_ = 'coefbox'):
            try:
                def_pred_list.append(all_pred_value.find('div',class_ = 'value').text.strip())
            except:
                pass
        data['DATE'].append(def_match_date)
        data['TIME'].append(def_match_time)
        data['HOME TEAM'].append(def_host_team)
        data['AWAY TEAM'].append(def_guess_team)

        data['HOME PER'].append(def_pred_list[0])
        data['DRAW PER'].append(def_pred_list[1])
        data['AWAY PER'].append(def_pred_list[2])

        data['BTS'].append(def_pred_list[9])
        data['OTS'].append(def_pred_list[10])

        data['OVER 2.5'].append(def_pred_list[7])
        data['UNDER 2.5'].append(100 - int(def_pred_list[7]))
        data['NAME'].append('STA')
     


def statarea_func():
    full_path = save_daily_csv()
    path = f'{full_path}/statarea.csv'

    data = {
        'DATE': [],
        'TIME': [],
        
        'HOME TEAM': [],
        'AWAY TEAM': [],

        'HOME PER':[],
        'DRAW PER':[],
        'AWAY PER':[],

        'UNDER 2.5':[],
        'OVER 2.5':[],

        'BTS':[],
        'OTS':[],

        'NAME':[]
    }

    if match_day_date ==1:
        match_date = date.today() + timedelta(1)
    else:
        match_date = date.today() + timedelta(0)
        
    getting_tmr_match(data=data,match_date=match_date)
    print('\n STATAREA DATA SUCCESSFULLY GOTTEN \n')
    saving_files(data=data,path=path)
    drop_duplicate(path=path)
statarea_func()