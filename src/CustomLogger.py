"""
Scripts for parameterizing logging instance.
"""

import json
import logging
import pandas as pd
import logging.config
from pythonjsonlogger import jsonlogger
from src.paths import LOCAL_CONFIG_PATH, LOCAL_LOGGING_PATH
from logging import (NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL)


def getLogger(name:str, logging_level:int=INFO):
    """
    Returns a logger object with timestamp
    information and terminal output
    """

    # force logger name
    name = 'default'
    logging.config.fileConfig(LOCAL_CONFIG_PATH / 'logging.ini', disable_existing_loggers=True)
    logging.FileHandler(LOCAL_LOGGING_PATH)
    logger = logging.getLogger(name)
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    # bounds screen_handler to return logger 

    return logger


def set_logging_ini_file():
    """
    Updated logging ini file based on local paths.
    """

    ini_template = LOCAL_CONFIG_PATH / 'logging_template.ini'
    ini_output = LOCAL_CONFIG_PATH / 'logging.ini'

    with open(ini_template) as f:
        ini_str = f.read().format(output_logging_path=str(LOCAL_LOGGING_PATH))

    with open(ini_output, mode='w', encoding='utf8') as f:
        f.write(ini_str)                          


def load_log2dataframe(logging_path=LOCAL_LOGGING_PATH):
    """
    Returns logs as DataFrame for exploration.
    """

    with open(logging_path, mode='r', encoding='utf8') as fp:
        jsons = [json.loads(j) for j in fp.read().splitlines()]
        
    df = pd.DataFrame.from_records(jsons)

    if 'asctime' in df.columns:
        df['asctime'] = pd.to_datetime(df['asctime'])

    return df

set_logging_ini_file()