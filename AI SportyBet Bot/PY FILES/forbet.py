import time
import asyncio
import pandas as pd
from pyppeteer import launch
from bs4 import BeautifulSoup
from func import requests_init,saving_files,drop_duplicate,match_day_date,main_date,save_daily_csv,sorting_values





async def main(): 
    full_path = save_daily_csv()
    path = f'{full_path}/forebet.csv'
    # Use your Chrome installation path here
    browser = await launch(
        executablePath=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        headless=False  # Set False if you want to see the browser
    )
    page = await browser.newPage()

    _1x2url = f'https://www.forebet.com/en/football-predictions/predictions-1x2/{main_date()}'
    ovrund_url = f'https://www.forebet.com/en/football-predictions/under-over-25-goals/{main_date()}'
    btsots_url = f'https://www.forebet.com/en/football-predictions/both-to-score/{main_date()}'
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
        await page.goto(main_url,timeout = 0,waitUntil='networkidle2')

        for i in range(7):  # scroll 10 times
            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(1)

        for x in range(3):  # click MORE button 3 times
            try:
                await page.waitForSelector('#mrows', {'visible': True})
                await page.click('#mrows')
                print(f'Clicked MORE button {x+1} times \n')
            except Exception as e:
                print(f'Breaking Due To Error clicking MORE button: {e}')
                break
            time.sleep(2)  # wait for 2 seconds after each click

        await asyncio.sleep(7)
        print('\n MORE CLICKED AND 7 SECONDS WAITED \n')

        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        all_content = soup.find('div', class_='schema')
        print('\n ALL CONTENT FETCHED \n')
        


        if main_url == _1x2url:
            print('\n CURRENTLY ON 1X2 OPTION \n')
            match_date = [(y.text.split())[0] for y in all_content.find_all('span', class_='date_bah')]
            match_time = [(y.text.split())[-1] for y in all_content.find_all('span', class_='date_bah')]
            hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
            aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
            # print(match_date, match_time, hm_team, aw_team) 

            hm_per = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
            draw_per = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
            aw_per = [y.find_all('span')[2].text for y in all_content.find_all('div', class_='fprc')]
            # print(hm_per, draw_per, aw_per)
            print(len(match_date), len(match_time), len(hm_team), len(aw_team), len(hm_per), len(draw_per), len(aw_per))
            _1x2data['DATE']= match_date
            _1x2data['TIME']= match_time
            _1x2data['HOME TEAM']= hm_team
            _1x2data['AWAY TEAM']= aw_team
            _1x2data['HOME PER']= hm_per
            _1x2data['DRAW PER']= draw_per
            _1x2data['AWAY PER']= aw_per


        elif main_url == ovrund_url:
            print('\n CURRENTLY ON OVER/UNDER OPTION \n')
            hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
            aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
            under_2_5 = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
            over_2_5 = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
            # print(hm_team,aw_team,under_2_5,over_2_5)
            print(len(hm_team), len(aw_team), len(under_2_5), len(over_2_5))
            ovrund_data['HOME TEAM']= hm_team
            ovrund_data['AWAY TEAM']= aw_team
            ovrund_data['UNDER 2.5']= under_2_5
            ovrund_data['OVER 2.5']= over_2_5

        else:
            print('\n CURRENTLY ON OTS/BTS OPTION \n')
            hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
            aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
            ots = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
            bts = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
            # print(hm_team,aw_team,bts,ots)
            print(len(hm_team), len(aw_team), len(bts), len(ots))
            btsund_data['HOME TEAM']= hm_team
            btsund_data['AWAY TEAM']= aw_team
            btsund_data['BTS']= bts
            btsund_data['OTS']= ots
            btsund_data['NAME']= 'Forebet'

    df1 = pd.DataFrame(_1x2data)
    df2 = pd.DataFrame(ovrund_data)
    df3 = pd.DataFrame(btsund_data)
    # print(df1.to_string())
    # print(df2.to_string())  
    # print(df3.to_string())
    print(len(df1), len(df2), len(df3))
    all_df = pd.merge(df1, df2, on=['HOME TEAM', 'AWAY TEAM'], how='inner')
    all_df = pd.merge(all_df, df3, on=['HOME TEAM', 'AWAY TEAM'], how='inner').reset_index(drop=True)
    print(all_df)

    all_df.to_csv(path, index=False)
    print('============================= FIRST FILE SAVED ==========================')
    drop_duplicate(path=path)
    await browser.close()

asyncio.run(main())

