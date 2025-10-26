
from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
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





