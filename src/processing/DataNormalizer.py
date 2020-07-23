import string
import numpy as np
import pandas as pd
import pathlib as pl
from ast import literal_eval
import matplotlib.pyplot as plt

def normalize_dtypes_nyt(df):
    """
    Normalizes data types of NYT articles DataFrame
    """

    cols = ['headline', 'keywords', 'byline', 'multimedia']

    for c in cols:
        df.loc[:,c] = df.loc[:,c].apply(literal_eval)

    df.loc[:, 'pub_date'] = pd.to_datetime(df.loc[:, 'pub_date'])

    return df

def explode_column_nyt(df,column:str='keywords'):
    """
    Explodes NYT Articles DataFrame based on column`
    """
    exploded_df = df.explode('keywords')
    mask = exploded_df.keywords.notna()
    exploded_df = exploded_df[mask]
    exploded_df = exploded_df.reset_index().drop('index', axis=1)
    tmp = pd.json_normalize(exploded_df[column], errors='ignore').add_prefix(f'{column}.')
    exploded_df = exploded_df.drop(column, axis=1).join(tmp)

    return exploded_df

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))