
from func import requests_init,saving_files,drop_duplicate,sorting_values,save_daily_csv,match_day_date,save_daily_csv2,main_date
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os




def betclan_func():
    full_path = save_daily_csv()
    path = f'{full_path}/betclan.csv'
    save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
    save_path = f'{save_dir}/BCLAN_Data.csv'

    if match_day_date ==1:
        url = 'https://www.betclan.com/tomorrows-football-predictions/'
    else:
        url = 'https://www.betclan.com/todays-football-predictions/'



    soup,_ = requests_init(url)
    #   GETTING LINK SECTION
    links = [name.get('href') for name in soup.findAll('a')]
    # print(links)

    all_link = []
    for link in links:
        try:
            if link.startswith('https://www.betclan.com/predictionsdetails/') and link not in all_link:
                all_link.append(link)
        except:
            pass
    # USING LINKS TO GET ELEMENT IN THAT TEAMS
    print('LENGHT OF ALL LINKS = ',len(all_link))
    # all_link = all_link[170:]


    for i,x in enumerate(all_link[:]):
        pp_data = {'INFO':[]}
        pp_target = f'{x}'
        pp_data['INFO'].append(pp_target)
        try:
            pp_data_df = pd.read_csv(save_path)['INFO'].to_list()
        except:
            pp_data_df = pd.DataFrame({'INFO':['accumulator']})['INFO'].to_list()

        if pp_target not in pp_data_df:
            saving_files(data=pp_data,path=save_path)

            print('\n url = ',x)


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

            index_pos = i
            print(f'>>>>>>>>>>>>>>>>>>>>  NUMBER = {index_pos} HAS STARTED TO RUN, WITH TOTAL RUNS OF {len(all_link)}  & REMANING OF {len(all_link) - (index_pos+1)} <<<<<<<<<<<<<<<<<<<< \n')
            
            try:
                res = requests.get(x)
                soup = BeautifulSoup(res.content,"html.parser")

                preds = [x.text.strip().replace('%','').split() for x in soup.find_all('div',class_ = 'cell vote__stats js-vote-stats-container')]
                # _,tree = requests_init(url=x)
                date_time = soup.find('span',class_ = 'dategamedetailsis').text.strip().split()
                teams = soup.find('div',class_ = 'teamstop').text.strip().split('\n')
                home_team = teams[0]
                away_team = teams[-1]
                
                hw = int(preds[0][1])
                draw = int(preds[0][3])
                aw = int(preds[0][5])

                under = int(preds[1][1])
                over = int(preds[1][3])

                bts = int(preds[2][1])
                ots = int(preds[2][3])

                print(date_time,home_team,away_team,hw,draw,aw,under,over,bts,ots)

                data['DATE'].append(date_time[1])
                data['TIME'].append(date_time[2])

                data['HOME TEAM'].append(home_team)
                data['AWAY TEAM'].append(away_team)

                data['HOME PER'].append(hw)
                data['DRAW PER'].append(draw)
                data['AWAY PER'].append(aw)
                
                data['UNDER 2.5'].append(under)
                data['OVER 2.5'].append(over)

                data['BTS'].append(bts)
                data['OTS'].append(ots)
                data['NAME'].append('BCL')

                saving_files(path=path,data=data)

            except:
                print('\n \n SORRY AN ERROR OCCURED \n')
                pass

    drop_duplicate(path=path)

betclan_func()