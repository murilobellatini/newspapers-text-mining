"""
Script for interacting with New York Times API and extracting articles
"""

import re
import json
import time
import requests
import datetime
import itertools
import pandas as pd
from tqdm import tqdm
from src.CustomLogger import getLogger
from src.paths import LOCAL_CREDENTIALS_PATH, LOCAL_RAW_DATA_PATH


# Loads logger for exception handling purposes
logger = getLogger(__name__)

def get_api_token(api_name:str):
    """
    Returns API Token for ``api_name`` stored in ``LOCAL_CREDENTIALS_PATH / 'api-credentials.json'``
    """
    with open(LOCAL_CREDENTIALS_PATH / 'api-credentials.json') as fp:
        API_TOKEN = json.load(fp)[api_name]

    return API_TOKEN

def get_str_desk(desk_list:list):
    """
    Converts list into string for NYT API Url composition
    """
    str_desks = str(desk_list).replace('\'', '\"')
    str_desks = re.sub('\[|\]|,','', str_desks)
    return str_desks

def pairwise(iterable:list):
    """
    Iterates over list returning tuple of current and next value
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

def convert_dt_to_string(dt:datetime.datetime,fmt:str='%Y%m%d'):
    """
    Converts datetime into string according format defined in `fmt`
    """
    return dt.strftime('%Y%m%d')

def get_search_url(desks:list, page:int, begin_date:str, end_date:str):
    """
    Composes NYT API Article Search URL
    """
    NYT_SEARCH_URL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    NYT_API_TOKEN = get_api_token('NYT')
    return f"{NYT_SEARCH_URL}?fq=news_desk:({get_str_desk(desks)})&page={page}&begin_date={begin_date}&end_date={end_date}&api-key={NYT_API_TOKEN}"    

def get_day_range_list(begin_date:datetime.datetime, end_date:datetime.datetime):
    """
    Returns list of datetime strings between `begin_date` and `end_date`
    """
    output_days_list = []
    i = 0
    while True:
        current_date = begin_date + datetime.timedelta(days=i)
        output_days_list.append(convert_dt_to_string(current_date))
        i += 1
        if current_date >= end_date:
            break
    return output_days_list

def extract_desk_articles(desks:list, begin_date:datetime.datetime, end_date:datetime.datetime, sleep_time:int=10, export_data:bool=True):
    """
    Exports articles to csv's (one per request) and returns list objects.
    - `desks`: list of themes to be scrapped
    - `begin_date`: begin date for scrapping
    - `end_date`: end date for scrapping
    - `sleep_time`: time slept between api request to avoid exceding timely quota
    """
    output_articles = []
    days_list = get_day_range_list(begin_date, end_date)
    for current_date, next_date in tqdm(pairwise(days_list), total=len(days_list)-1):
        page = 0
        scrapped_articles = 0
        while True:
            try:
                api_url = get_search_url(desks, page, current_date, next_date)
                response = requests.get(api_url)
                scrapped_articles += len(response.json()['response']['docs'])
                total_articles = response.json()['response']['meta']['hits']
                response_docs = response.json()['response']['docs']
                output_articles.extend(response_docs)
                if export_data:
                    export_data_to_csv(response_docs)
                page += 1
                if scrapped_articles >= total_articles:
                    break
                time.sleep(sleep_time)
            except Exception as e:
                logger.error(f'Error `{e}` at `{api_url}`')

    return output_articles

def export_data_to_csv(output_articles:list):
    """
    Exports list of articles `output_articles` as `csv`
    """
    output_path = LOCAL_RAW_DATA_PATH / f'nyt-articles-{time.time()}.csv'
    df = pd.DataFrame(output_articles)
    df.to_csv(output_path)