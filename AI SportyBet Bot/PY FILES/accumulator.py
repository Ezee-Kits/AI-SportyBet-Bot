from func import requests_init,saving_files,drop_duplicate,sorting_values,save_daily_csv,match_day_date,save_daily_csv2,main_date
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import time
import os

def accumulator_func():
    save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
    save_path = f'{save_dir}/ACCU_Data.csv'

    local_time = time.localtime()
    full_path = save_daily_csv()
    path = path = f'{full_path}/accumulator.csv'

    td_url = 'https://www.accagenerator.com/football-predictions/'
    # tmr_url = 'https://www.accagenerator.com/football-predictions/tomorrow/'


    res = requests.get(td_url)
    soup = BeautifulSoup(res.content,"html.parser")

    links = [name.get('href') for name in soup.findAll('a')]
    # print(links)
    all_links =[]
    for link in links:
        if link.startswith('https://www.accagenerator.com/football-tips-and-predictions-for') and link not in all_links:
            all_links.append(link)
    # print(all_links)
    print('LENGHT OF ALL LINKS = ',len(all_links))



    ex_link = ['1x2-predictions/','over-under-predictions','both-teams-score-predictions/']

    for i,x in enumerate(all_links[:]):
        pp_data = {'INFO':[]}
        pp_target = f'{x}'
        pp_data['INFO'].append(pp_target)
        try:
            pp_data_df = pd.read_csv(save_path)['INFO'].to_list()
        except:
            pp_data_df = pd.DataFrame({'INFO':['accumulator']})['INFO'].to_list()

        if pp_target not in pp_data_df:
            saving_files(data=pp_data,path=save_path)
            print(x)
            data = {
                    'DATE':[],
                    'TIME':[],
                    
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
            
            for xlink in ex_link:

                res = requests.get(x+xlink)
                soup = BeautifulSoup(res.content,"html.parser")
                tree = html.fromstring(res.content)

                index_pos = i
                print(f'>>>>>>>>>>>>>>>>>>>>  NUMBER = {index_pos+1} HAS STARTED TO RUN, WITH TOTAL RUNS OF {len(all_links)}  & REMANING OF {len(all_links) - (index_pos+1)} <<<<<<<<<<<<<<<<<<<< \n')
                
                tip_info = soup.select('#accagen-banner > div > div > div.accagen-banner-text.accagen-headline > h1')[0].text
                print(tip_info)
                try:
                    for all_pred in range(0,20):
                        each_row = soup.select('#accagen-banner > div > div > div:nth-child(3) > ul > li:nth-child('+str((2*all_pred) + 1)+')')[0]
                        pred_date = each_row.find('div',class_="datecombos").text.split()
                        pred_time = pred_date[3]
                        pred_date = f'{local_time[0]}.' + pred_date[1]
                        time_match = time.strptime(pred_date,'%Y.%d.%m')[:3] == local_time[:3]
                        
                        if time_match:
                            league = each_row.find('span',class_="tips-card__league").text.split('\n')[-1]
                            teams = each_row.find('h3',class_="tips-card__name-first").text.split('vs')
                            
                            tip = each_row.find('div',class_="tipdetail").text
                            tip_per = int(each_row.find('span',class_="count-text").get('data-stop'))
                            print(pred_date, league,teams,tip, tip_per)

                            if '1x2' in tip_info:
                                data['DATE'].append(pred_date)
                                data['TIME'].append(pred_time)
                                data['HOME TEAM'].append(teams[0])
                                data['AWAY TEAM'].append(teams[1])
                                if str(tip) == '1':
                                    hw = tip_per
                                    draw = int((100-tip_per)/2)
                                    aw = int((100-tip_per)/2)
                                if str(tip) == '2':
                                    aw = tip_per
                                    draw = int((100-tip_per)/2)
                                    hw = int((100-tip_per)/2)                       
                                if str(tip) == 'X':
                                    draw = tip_per
                                    hw = int((100-tip_per)/2)
                                    aw = int((100-tip_per)/2)

                                data['HOME PER'].append(hw)
                                data['DRAW PER'].append(draw)
                                data['AWAY PER'].append(aw)
                                data['NAME'].append('ACC')


                            if 'BTTS' in tip_info:
                                if tip == 'Yes':
                                    bts = tip_per
                                    ots = int(100-tip_per)
                                if tip == 'No':
                                    ots = tip_per
                                    bts = int(100-tip_per)
                                data['BTS'].append(bts)
                                data['OTS'].append(ots)

                            if 'Over Under' in tip_info:
                                if tip == 'Over 2.5':
                                    over = tip_per
                                    under = 100-tip_per
                                if tip == 'Under 2.5':
                                    under = tip_per
                                    over = 100-tip_per
                                data['UNDER 2.5'].append(under)
                                data['OVER 2.5'].append(over)
                except:
                    print('\n \t ERROR OCCURED WHEN SCRAPING \n ')
            saving_files(data=data,path=path)
        
    drop_duplicate(path=path)


accumulator_func()