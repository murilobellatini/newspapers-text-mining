import os
import pandas as pd
import pathlib as pl
from tqdm import tqdm
from src.CustomLogger import getLogger
from src.paths import LOCAL_RAW_DATA_PATH, LOCAL_INTERIM_DATA_PATH
from src.processing.DataNormalizer import normalize_dtypes_nyt, explode_column_nyt

logger = getLogger(__name__)

def consolidate_csvs(prefix:str, data_path:pl.Path=LOCAL_RAW_DATA_PATH):
    """
    Loads all csv files beggining with `prefix` located inside `data_path`
    """
    csv_paths = [LOCAL_RAW_DATA_PATH / f for f in os.listdir(LOCAL_RAW_DATA_PATH) if f.startswith(prefix)]
    
    logger.info(f"Loading raw data into single DataFrame")

    df = pd.DataFrame()
    for i in tqdm(csv_paths):
        tmp_df = pd.read_csv(i, index_col=0)
        df = df.append(tmp_df)

    df = df.drop_duplicates('_id')

    return df

def consolidate_articles(prefix:str, input_data_path:pl.Path=LOCAL_RAW_DATA_PATH, output_data_path:pl.Path=LOCAL_INTERIM_DATA_PATH):
    """
    Consolidates articles into two DataFrame (full and exploded) with normalized data types.
     - Full DataFrame has each for for one article
     - Exploded DataFrame has as many rows for article as there are subfields inside keywords column (following concept of tidy data for future data exploration)
    Result is exported in cst to output_data_path
    """
    df = consolidate_csvs(prefix, data_path=LOCAL_RAW_DATA_PATH)
    df = normalize_dtypes_nyt(df)
    exploded_df = explode_column_nyt(df)

    df.to_csv(output_data_path / 'nyt-articles-consolidated.csv')
    logger.info(f"`df` sucessfully exported to {output_data_path / 'nyt-articles-consolidated.csv'}")
    exploded_df.to_csv(output_data_path / 'nyt-articles-consolidated-exploded.csv')
    logger.info(f"`exploded_df` sucessfully exported to {output_data_path / 'nyt-articles-consolidated-exploded.csv'}")

    return df, exploded_df

def load_normalized_nyt_df(df_path:pl.Path):
    df = pd.read_csv(df_path, index_col=0)
    df = normalize_dtypes_nyt(df)
    return df
