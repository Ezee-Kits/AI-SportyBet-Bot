from func import main_date,save_daily_csv2,saving_files,place_bet,sort_by_name_and_time,click_center
from datetime import datetime
from pyppeteer import launch
from Main_Calc import cal
import os,time
import asyncio
import pandas as pd
import warnings
warnings.simplefilter(action='ignore',category=pd.errors.PerformanceWarning)


browser_delay_time=5000

csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')

save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
save_path = f'{save_dir}/Data.csv'



percent = 57 # DATA SORTING PERCENT
A_edge = 10 #ACCEPTED EDGE
# FA3W_percent = 53 #FORBET ACCEPTED 3WAY PERCENT
# FA2W_percent = 63 #FORBET ACCEPTED 2WAY PERCENT
Err_Timeout = 4000 # WEBPAGE TIMEOUT 




# # Read the CSV files
acc_df_f = pd.read_csv(f'{csv_files_path}/accumulator.csv')
bcl_df_f = pd.read_csv(f'{csv_files_path}/betclan.csv')
fst_df_f = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
frb_df_f = pd.read_csv(f'{csv_files_path}/forebet.csv')
pre_df_f = pd.read_csv(f'{csv_files_path}/prematips.csv')
sta_df_f = pd.read_csv(f'{csv_files_path}/statarea.csv')

 

async def main():
    global acc_df, bcl_df, fst_df, frb_df, pre_df, sta_df
    browser = await launch({
        'executablePath': '/data/data/com.termux/files/usr/lib/chromium/chrome',
        'args': [
            '--no-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-software-rasterizer',
            '--disable-setuid-sandbox',
            '--enable-features=UseOzonePlatform',
            '--ozone-platform=x11'
        ],
        'headless': False,
        'userDataDir': '/data/data/com.termux/files/home/BrowserData'
    })

    
    page = await browser.newPage()
    url = 'https://www.sportybet.com/ng/sport/football/today'
    await page.goto(url=url,timeout = 0,waitUntil='networkidle2')
    input("PRESS ENTER AFTER LOGGING IN AND SETTING UP THE PAGE TO AUTOMATE...")



    for next_page in range(2,12):
        for fir_match in range(2,100): # MAIN LAYER (2 MINIMUM VALUE)
            print(f'\n [[CURRENTLY ON PAGINATION PAGE]] : {next_page-1}\n')
            try:
                await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]', timeout=Err_Timeout)
                # Scroll element into view
                await page.evaluate(f'''
                    el = document.evaluate('//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]',
                    document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                ''')
            except:
                try:
                    await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match+1}]/div/div[3]/div[1]', timeout=Err_Timeout)
                    # Scroll element into view
                    await page.evaluate(f'''
                        el = document.evaluate('//*[@id="importMatch"]/div[{fir_match+1}]/div/div[3]/div[1]',
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    ''')
                except:
                    try:
                        print(f'\n CURRENTLY ON PAGINATION SECTION : {next_page} \n')
                        await page.waitForXPath(f'//span[@class="pageNum" and text()="{next_page}"]', timeout=Err_Timeout)
                        # Scroll element into view
                        await page.evaluate(f'''
                            el = document.evaluate('//span[@class="pageNum" and text()="{next_page}"]',
                            document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        ''')

                        await asyncio.sleep(2)
                        await click_center(page, f'//span[@class="pageNum" and text()="{next_page}"]') 
                        await asyncio.sleep(12)
                        print(f'\n CLICKED ON NEXXT PAGE : {next_page}\n')
                        break
                    except:
                        break


            sec_match_error_list = []
            for sec_match in range(2,50): # SUB LAYER (2 MINIMUM VALUE)
                pp_data = {'INFO':[]}
                print(f'\n CURRENTLY ON SPORTY NUMBER >>>> {fir_match} ON {sec_match}\n')
    
                # Wait for the first element to appear
                try:
                    element = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]', timeout=Err_Timeout)
                    await element.getProperty('textContent')
                except:
                    break

                await asyncio.sleep(1)
                try:
                    # Scroll element into view
                    await page.evaluate(f'''
                        el = document.evaluate('//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]',
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    ''')
                except:
                    print('error on 1 scroll')
                    break
                #await asyncio.sleep(1)

                # Scroll again to make sure the next section is visible
                try:
                    await page.evaluate(f'''
                        el = document.evaluate('//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]',
                        document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    ''')
                except:
                    print('error on 2 scroll')
                    break

                # Extract text values
                print('currently on data extraction')
                try:
                    date_elem = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[1]/div[1]',timeout = Err_Timeout)
                    spt_date = (await (await date_elem.getProperty('textContent')).jsonValue()).split()[0]
                    spt_date = datetime.strptime(f"2025/{spt_date}", "%Y/%d/%m").strftime("%Y-%m-%d")

                    time_elem = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[1]/div[1]', timeout=Err_Timeout)
                    spt_time = (await (await time_elem.getProperty('textContent')).jsonValue()).strip()

                    home_elem = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]', timeout=Err_Timeout)
                    spt_home_team = (await (await home_elem.getProperty('textContent')).jsonValue()).strip()

                    away_elem = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[2]', timeout=Err_Timeout)
                    spt_away_team = (await (await away_elem.getProperty('textContent')).jsonValue()).strip()

                except:
                    print('error on data extraction section')
                    break
        
                print(spt_date, spt_time, spt_home_team, spt_away_team)

                pp_target = f'{spt_date}-{spt_time}-{spt_home_team}-{spt_away_team}'
                pp_data['INFO'].append(pp_target)
    
                
                try:
                    pp_data_df = pd.read_csv(save_path)['INFO'].to_list()
                except:
                    pp_data_df = pd.DataFrame({'INFO':['starting']})['INFO'].to_list()

                if pp_target not in pp_data_df:
                    saving_files(data=pp_data,path=save_path)

                    acc_df = sort_by_name_and_time(acc_df_f, spt_home_team, spt_away_team, spt_time, percent)
                    bcl_df = sort_by_name_and_time(bcl_df_f, spt_home_team, spt_away_team, spt_time, percent)
                    fst_df = sort_by_name_and_time(fst_df_f, spt_home_team, spt_away_team, spt_time, percent)
                    frb_df = sort_by_name_and_time(frb_df_f, spt_home_team, spt_away_team, spt_time, percent)
                    pre_df = sort_by_name_and_time(pre_df_f, spt_home_team, spt_away_team, spt_time, percent)
                    sta_df = sort_by_name_and_time(sta_df_f, spt_home_team, spt_away_team, spt_time, percent)

                    all_df = [acc_df,bcl_df,fst_df,pre_df,sta_df]
                    new_df = pd.concat(all_df, ignore_index=True)

                    if len(new_df) >=1:
                        frb_time = new_df['TIME'][0]
                        frb_home_team = new_df['HOME TEAM'][0]
                        frb_away_team = new_df['AWAY TEAM'][0]
                        frb_home_per = round(new_df['HOME PER'].mean(), 2)
                        frb_draw_per = round(new_df['DRAW PER'].mean(), 2)
                        frb_away_per = round(new_df['AWAY PER'].mean(), 2)
                        frb_ovr25_per = round(new_df['OVER 2.5'].mean(), 2)
                        frb_und25_per = round(new_df['UNDER 2.5'].mean(), 2)
                        frb_bts_per = round(new_df['BTS'].mean(), 2)
                        frb_ots_per = round(new_df['OTS'].mean(), 2)

                        if len(new_df) ==1:
                            FA3W_percent = 60 #FORBET ACCEPTED 3WAY PERCENT
                            FA2W_percent = 70 #FORBET ACCEPTED 2WAY PERCENT

                        if len(new_df) ==2:
                            FA3W_percent = 57 #FORBET ACCEPTED 3WAY PERCENT
                            FA2W_percent = 67 #FORBET ACCEPTED 2WAY PERCENT

                        if len(new_df) >=3:
                            FA3W_percent = 53 #FORBET ACCEPTED 3WAY PERCENT
                            FA2W_percent = 63 #FORBET ACCEPTED 2WAY PERCENT


                        print('\n ==================== MATCHED DATA ====================== \n')
                        print(new_df)



                        # ======================================  1 X 2 OPTIONS  ===============================================
                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')
                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')

                        if frb_home_per >= FA3W_percent:
                            try:
                                spt_hodd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[1]')
                                spt_hodd_text = (await (await spt_hodd.getProperty('textContent')).jsonValue()).strip()
                                home_edge = cal(float(spt_hodd_text), frb_home_per)
                                if home_edge >= A_edge:
                                    await asyncio.sleep(1.5)
                                    await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[1]')
                                    await place_bet(page, home_edge)
                                    print(f'\n PLACED BET ON >>>>> (HOME EDGE : {home_edge} %  @ {spt_hodd_text} WITH ACCU : {frb_home_per}% ) \n')
                                print(f'HOME EDGE : {home_edge} %  @ {spt_hodd_text} WITH ACCU : {frb_home_per}% \n')
                            except Exception as e:
                                print(f"Error fetching home odd: {e}")
                        
                        if frb_draw_per >= FA3W_percent:
                            try:
                                spt_dodd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[2]')
                                spt_dodd_text = (await (await spt_dodd.getProperty('textContent')).jsonValue()).strip()
                                draw_edge = cal(float(spt_dodd_text), frb_draw_per)
                                if draw_edge >= A_edge:
                                    await asyncio.sleep(1.5)
                                    await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[2]')
                                    await place_bet(page, draw_edge)
                                    print(f'\n PLACED BET ON >>>>> (DRAW EDGE : {draw_edge} %  @ {spt_dodd_text} WITH ACCU : {frb_draw_per}% ) \n')
                                print(f'DRAW EDGE : {draw_edge} %  @ {spt_dodd_text} WITH ACCU : {frb_draw_per}% \n')
                            except Exception as e:
                                print(f"Error fetching draw odd: {e}")


                        if frb_away_per >= FA3W_percent:
                            try:
                                spt_aodd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[3]')
                                spt_aodd_text = (await (await spt_aodd.getProperty('textContent')).jsonValue()).strip()
                                away_edge = cal(float(spt_aodd_text), frb_away_per)
                                if away_edge >= A_edge:
                                    await asyncio.sleep(1.5)
                                    await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[3]')
                                    await place_bet(page, away_edge)
                                    print(f'\n PLACED BET ON >>>>> (AWAY EDGE : {away_edge} %  @ {spt_aodd_text} WITH ACCU : {frb_away_per}% ) \n')
                                print(f'AWAY EDGE : {away_edge} %  @ {spt_aodd_text} WITH ACCU : {frb_away_per}% \n')
                            except Exception as e:
                                print(f"Error fetching away odd: {e}")





                        # ======================================== Over/Under 2.5 OPTIONS ================================================
                        xpath = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[1]'
                        try:
                            elements = await page.xpath(xpath)
                            if elements:
                                await elements[0].click()
                                await asyncio.sleep(1)  # Give time for dropdown animation
                            else:
                                pass
                            await page.waitForSelector('.af-select-list-open', {'visible': True, 'timeout': 6000})
                            await page.evaluate('''() => {
                                const options = document.querySelectorAll('.af-select-list-open .af-select-item');
                                for (let opt of options) {
                                    if (opt.textContent.trim() === '2.5') {
                                        opt.click();
                                        break;
                                    }
                                }
                            }''')
                        except:
                            print('\n MAYBE OVR/UND 2.5 SELECTION DOESNT EXIST \n')

                        try:
                            main_ovr_odd = await page.waitForXPath(xpath, timeout=Err_Timeout)
                            main_ovr_odd_text = (await (await main_ovr_odd.getProperty('textContent')).jsonValue()).strip()
                        except:
                            main_ovr_odd_text = '5.5'
                            
                        if '2.5' in main_ovr_odd_text:
                            print('OVER / UNDER 2.5 DETECTED, CHECKING FOR EDGE ODDS NOW....')
                            await asyncio.sleep(1)
                            if frb_ovr25_per >= FA2W_percent:
                                try:
                                    spt_ovr_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[2]')
                                    spt_ovr_odd_text = (await (await spt_ovr_odd.getProperty('textContent')).jsonValue()).strip()
                                    over_edge = cal(float(spt_ovr_odd_text), frb_ovr25_per)
                                    if over_edge >= A_edge:
                                        await asyncio.sleep(1.5)
                                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[2]')
                                        await place_bet(page, over_edge)
                                        print(f'\n PLACED BET ON >>>>> (OVER 2.5 EDGE : {over_edge} %  @ {spt_ovr_odd_text} WITH ACCU : {frb_ovr25_per}% ) \n')
                                    print(f'OVER 2.5 EDGE : {over_edge} %  @ {spt_ovr_odd_text} WITH ACCU : {frb_ovr25_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching over odd: {e}")

                            if frb_und25_per >= FA2W_percent:
                                try:
                                    spt_und_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[3]')
                                    spt_und_odd_text = (await (await spt_und_odd.getProperty('textContent')).jsonValue()).strip()
                                    under_edge = cal(float(spt_und_odd_text), frb_und25_per)
                                    if under_edge >= A_edge:
                                        await asyncio.sleep(1.5)
                                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[3]')
                                        await place_bet(page, under_edge)
                                        print(f'\n PLACED BET ON >>>>> (UNDER 2.5 EDGE : {under_edge} %  @ {spt_und_odd_text} WITH ACCU : {frb_und25_per}% ) \n')
                                    print(f'UNDER 2.5 EDGE : {under_edge} %  @ {spt_und_odd_text} WITH ACCU : {frb_und25_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching under odd: {e}")




                        # # =====================================     BTS / OTS OPTIONS   ============================================
                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[3]')
                        await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[3]')

                        if frb_bts_per >= FA2W_percent:
                            try:
                                spt_bts_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[1]')
                                spt_bts_odd_text = (await (await spt_bts_odd.getProperty('textContent')).jsonValue()).strip()
                                bts_edge = cal(float(spt_bts_odd_text), frb_bts_per)
                                if bts_edge >= A_edge:
                                    await asyncio.sleep(1.5)
                                    await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[1]')
                                    await place_bet(page, bts_edge) 
                                    print(f'\n PLACED BET ON >>>>> (BOTH TEAMS TO SCORE EDGE : {bts_edge} %  @ {spt_bts_odd_text} WITH ACCU : {frb_bts_per}% ) \n')
                                print(f'BOTH TEAMS TO SCORE EDGE : {bts_edge} %  @ {spt_bts_odd_text} WITH ACCU : {frb_bts_per}% \n')
                            except Exception as e:
                                print(f"Error fetching BTS odd: {e}")

                        if frb_ots_per >= FA2W_percent:
                            try:
                                spt_ots_odd = await page.waitForXPath(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[2]')
                                spt_ots_odd_text = (await (await spt_ots_odd.getProperty('textContent')).jsonValue()).strip()
                                ots_edge = cal(float(spt_ots_odd_text), frb_ots_per)
                                if ots_edge >= A_edge:    
                                    await asyncio.sleep(1.5)
                                    await click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[2]')
                                    await place_bet(page, ots_edge)
                                    print(f'\n PLACED BET ON >>>>> (OTS SCORE EDGE : {ots_edge} %  @ {spt_ots_odd_text} WITH ACCU : {frb_ots_per}% ) \n')
                                print(f'OTS SCORE EDGE : {ots_edge} %  @ {spt_ots_odd_text} WITH ACCU : {frb_ots_per}% \n')
                            except Exception as e:
                                print(f"Error fetching OTS odd: {e}")
                                    

    await browser.close()

asyncio.run(main())
