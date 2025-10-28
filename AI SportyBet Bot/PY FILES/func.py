
from difflib import SequenceMatcher as ss
from datetime import datetime, timedelta
from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import asyncio
import time
import os


match_day_date = 0

def main_date(day = match_day_date):
    last_date = date.today() + timedelta(day)
    return last_date


def save_daily_csv():
    outcome_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES')
    todays_dir = str(main_date(match_day_date))+' Files'
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    
    
def save_daily_csv2(main_dir,second_dir_path_name):
    outcome_dir = main_dir
    todays_dir = second_dir_path_name
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    

def requests_init(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")
    tree = html.fromstring(res.content)
    return soup,tree


def tree_init(optional):
    tree = html.fromstring(optional)


def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')



def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)


def sorting_values(path,value,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path, index=False)


def sorting_values_path_to_save(path,value,path_to_save,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path_to_save, index=False)





async def place_bet(page, edge_amt, browser_delay_time=5000):
    # 2️⃣ Locate and clear input
    input_element = await page.waitForSelector('#j_stake_0 input', timeout=browser_delay_time)
    await page.evaluate('(el) => el.scrollIntoView({ behavior: "smooth", block: "center" })', input_element)
    await input_element.click()
    await asyncio.sleep(1)
    await input_element.click()
    await asyncio.sleep(1)
    await page.keyboard.down('Control')
    await page.keyboard.press('A')
    await page.keyboard.up('Control')
    await page.keyboard.press('Backspace')
    await asyncio.sleep(1)

    # 3️⃣ Type the new stake
    await input_element.type(str(edge_amt))
    await asyncio.sleep(2)

    # 4️⃣ Click "Place Bet"
    place_bet_element = await page.waitForXPath('//button[.//span[@data-cms-key="place_bet" and @data-cms-page="component_betslip" and normalize-space(text())="Place Bet"]]')
    await page.evaluate('(el) => el.scrollIntoView({ behavior: "smooth", block: "center" })', place_bet_element)
    await asyncio.sleep(1)
    await place_bet_element.click()
    await asyncio.sleep(1.5)
    await place_bet_element.click()
    await asyncio.sleep(1.5)

    # 5️⃣ Click "Confirm"
    confirm_button = await page.waitForXPath('//button[.//span[@data-cms-key="confirm" and @data-cms-page="common_functions"]]')
    await confirm_button.click()
    await asyncio.sleep(2)

    # 6️⃣ Click "OK"
    ok_button = await page.waitForXPath('//button[@data-action="close" and @data-ret="close" and .//span[@data-cms-key="ok" and @data-cms-page="common_functions"]]')
    await ok_button.click()
    await asyncio.sleep(1)

    # 1️⃣ Handle any dialogs early
    page.on("dialog", lambda dialog: asyncio.ensure_future(dialog.dismiss()))



async def click_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 8000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        time.sleep(1.5)
        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{xpath}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        time.sleep(1.5)
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{xpath}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{xpath}': {e}")
        return False

 





def sort_by_name_and_time(df, spt_home_team, spt_away_team, spt_time, percent):
    try:
        # Step 1: Calculate similarity for home team
        df['HOME_SIMILARITY'] = df['HOME TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_home_team).lower()).ratio() * 100
        )

        # Step 2: Calculate similarity for away team
        df['AWAY_SIMILARITY'] = df['AWAY TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_away_team).lower()).ratio() * 100
        )

        # Step 3: Keep rows where both similarities >= threshold
        filtered_df = df[
            (df['HOME_SIMILARITY'] >= percent) &
            (df['AWAY_SIMILARITY'] >= percent)
        ].copy()

        if filtered_df.empty:
            return filtered_df  # nothing matches, return empty

        # Step 4: Sort by combined similarity
        filtered_df['TOTAL_SIMILARITY'] = (
            filtered_df['HOME_SIMILARITY'] + filtered_df['AWAY_SIMILARITY']
        ) / 2
        filtered_df = filtered_df.sort_values(by='TOTAL_SIMILARITY', ascending=False).reset_index(drop=True)

        # Step 5: Filter by time difference
        spt_time_dt = datetime.strptime(spt_time, "%H:%M")
        def time_within_range(row_time_str):
            try:
                row_time_dt = datetime.strptime(str(row_time_str), "%H:%M")
                diff = abs((row_time_dt - spt_time_dt).total_seconds()) / 3600  # convert to hours
                return diff <= 1  # within ±1 hour
            except:
                return False

        filtered_df = filtered_df[filtered_df['TIME'].apply(time_within_range)].reset_index(drop=True)

        # Step 6: Drop helper columns
        filtered_df = filtered_df.drop(columns=['HOME_SIMILARITY', 'AWAY_SIMILARITY', 'TOTAL_SIMILARITY'])

        return filtered_df

    except Exception as e:
        print(f"Error sorting by team similarity and time: {e}")
        return df


        
def sort_by_name(df, spt_home_team, spt_away_team, percent):
    try:
        # Calculate similarity for home team
        df['HOME_SIMILARITY'] = df['HOME TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_home_team).lower()).ratio() * 100
        )

        # Calculate similarity for away team
        df['AWAY_SIMILARITY'] = df['AWAY TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_away_team).lower()).ratio() * 100
        )

        # Keep only rows where BOTH home & away similarity >= threshold
        filtered_df = df[
            (df['HOME_SIMILARITY'] >= percent) &
            (df['AWAY_SIMILARITY'] >= percent)
        ].copy()

        # Sort by total similarity (combined)
        filtered_df['TOTAL_SIMILARITY'] = (
            filtered_df['HOME_SIMILARITY'] + filtered_df['AWAY_SIMILARITY']
        ) / 2

        filtered_df = filtered_df.sort_values(by='TOTAL_SIMILARITY', ascending=False).reset_index(drop=True)

        # Drop helper columns
        filtered_df = filtered_df.drop(columns=['HOME_SIMILARITY', 'AWAY_SIMILARITY', 'TOTAL_SIMILARITY'])

        return filtered_df

    except Exception as e:
        print(f"Error sorting by team similarity: {e}")
        return df




def sort_by_time(df, current_time):
    try:
        # Convert the string time to datetime object
        time_obj = datetime.strptime(current_time, "%H:%M")

        # Define the time range (1 hour before and 1 hour after)
        start_time = time_obj - timedelta(hours=1)
        end_time = time_obj + timedelta(hours=1)

        # Convert 'TIME' column to datetime objects for comparison
        df['TIME_DT'] = pd.to_datetime(df['TIME'], format="%H:%M", errors='coerce')

        # Keep only rows within the ±1-hour window
        filtered_df = df[(df['TIME_DT'] >= start_time) & (df['TIME_DT'] <= end_time)]

        # Sort and reset index
        filtered_df = filtered_df.sort_values(by='TIME_DT').reset_index(drop=True)

        # Drop helper column
        filtered_df = filtered_df.drop(columns=['TIME_DT'])

        return filtered_df
    except Exception as e:
        print(f"Error sorting by time: {e}")
        return df
    



