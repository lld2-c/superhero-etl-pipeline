import pandas as pd
import zipfile
import shutil

def generateTestData():
    zf = zipfile.ZipFile('data/marvel-superheroes.zip') 
    characters = pd.read_csv(zf.open('characters.csv')).sample(n=50, random_state=666)
    charactersToComics = pd.read_csv(zf.open('charactersToComics.csv'))
    charactersToComics = charactersToComics[charactersToComics.characterID.isin(characters.characterID)]
    characters_stats = pd.read_csv(zf.open('charcters_stats.csv'))
    characters_stats = characters_stats[characters_stats.Name.isin(characters.name)]
    comics = pd.read_csv(zf.open('comics.csv')).sample(n=2000, random_state=666)
    marvel_characters_info = pd.read_csv(zf.open('marvel_characters_info.csv')).sample(n=100, random_state=666)
    superheroes_power_matrix = pd.read_csv(zf.open('superheroes_power_matrix.csv')).sample(n=100, random_state=666)
    # marvel_dc_characters.csv is a corrupted file, same purpose as marvel_dc_characters_ms, therefore ignored
    marvel_dc_characters_ms = pd.read_excel(zf.open('marvel_dc_characters.xlsx')).sample(n=100, random_state=666)

    characters.to_csv('data/test_data/characters.csv', index=False)
    charactersToComics.to_csv('data/test_data/charactersToComics.csv', index=False)
    characters_stats.to_csv('data/test_data/charcters_stats.csv', index=False)
    comics.to_csv('data/test_data/comics.csv', index=False)
    marvel_characters_info.to_csv('data/test_data/marvel_characters_info.csv', index=False)
    superheroes_power_matrix.to_csv('data/test_data/superheroes_power_matrix.csv', index=False)
    marvel_dc_characters_ms.to_excel('data/test_data/marvel_dc_characters.xlsx', index=False)

    shutil.make_archive('data/test_data', 'zip', 'data/test_data')