# source: https://www.kaggle.com/dannielr/marvel- superheroes#marvel_dc_charactAOers.csv
import pandas as pd
import zipfile
import logging
from typing import Tuple


def extract_data(testOrProd: str) -> Tuple[pd.DataFrame, ...]:
    logging.info('Extracting started..')

    # get zip file
    if testOrProd == 'test':
        zf = zipfile.ZipFile('data/test_data.zip') 
    else:
        zf = zipfile.ZipFile('data/marvel-superheroes.zip') 

    # extract from zip file to dataframes
    try:
        characters = pd.read_csv(zf.open('characters.csv'))
        charactersToComics = pd.read_csv(zf.open('charactersToComics.csv'))
        characters_stats = pd.read_csv(zf.open('charcters_stats.csv'))
        comics = pd.read_csv(zf.open('comics.csv'))
        marvel_characters_info = pd.read_csv(zf.open('marvel_characters_info.csv'))
        superheroes_power_matrix = pd.read_csv(zf.open('superheroes_power_matrix.csv'))
        # marvel_dc_characters.csv is a corrupted file, same purpose as marvel_dc_characters_ms, therefore ignored
        marvel_dc_characters_ms = pd.read_excel(zf.open('marvel_dc_characters.xlsx'))
        logging.info('Extract completed!')
        return (characters, charactersToComics, characters_stats, comics, marvel_characters_info, superheroes_power_matrix, marvel_dc_characters_ms)
    except Exception as e:
        logging.info('Extract failed:')
        logging.error(e)
