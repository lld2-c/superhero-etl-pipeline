import pandas as pd
from .extract import extract_data
import module # custom modules
import logging
import numpy as np
from datetime import datetime


def clean_dates(marvel_dc_characters_ms):
    df = marvel_dc_characters_ms
    df['flag'] = [isinstance(x, datetime) for x in df.FirstAppearance]

    flagged = df[df['flag'] == False]
    for index, row in flagged.iterrows():
        date_str = row['FirstAppearance']
        try:
            converted_date = module.convert_to_datetime(date_str)
            flagged.at[index, 'FirstAppearance'] = converted_date
        except Exception as e:
            flagged.at[index, 'FirstAppearance'] = np.nan

    unflagged = df[df['flag'] == True]
    concatenated_df = pd.concat([flagged, unflagged])
    concatenated_df['FirstAppearance'] = concatenated_df['FirstAppearance'].astype(str)
    concatenated_df.drop('flag', axis=1, inplace=True)
    return concatenated_df

def pre_process(extracted_data):
    logging.info('Start transforming..')
    try:
        characters, charactersToComics, characters_stats, comics, marvel_characters_info, superheroes_power_matrix, marvel_dc_characters_ms = extracted_data
        marvel_dc_characters_ms = clean_dates(marvel_dc_characters_ms)
        t_characters = pd.concat([characters['name'], 
                                        superheroes_power_matrix['Name'],
                                        marvel_characters_info['Name'], 
                                        marvel_dc_characters_ms['Name']])\
                                        .drop_duplicates().sort_values().reset_index(drop=True)
        o_characters = pd.DataFrame(t_characters, columns=['character_name'])
        o_characters.insert(0, 'character_id', range(0, len(o_characters)))
        o_characters['character_id'] = o_characters['character_id'].astype(str)
        # transform characters_to_powers M:N relationship
        t_charactersToPowers = pd.melt(superheroes_power_matrix, id_vars='Name', var_name='power', value_name='yn').query('yn == True').reset_index(drop=True).drop('yn', axis=1)
        o_powers = pd.DataFrame({'power_name': superheroes_power_matrix.columns}).drop(0).reset_index(drop=True)
        o_powers.insert(0, 'power_id', range(0, len(o_powers)))
        o_powers['power_id'] = o_powers['power_id'].astype(str)
        o_charactersToPowers = t_charactersToPowers.\
        merge(o_characters, left_on='Name', right_on='character_name', how='left').\
            merge(o_powers, left_on='power', right_on='power_name', how='left').\
            loc[:, ['character_id', 'power_id']]
        # transform characters characters_wiki 1:N relationship
        # merge tables related to character_wiki
        # something went wrong when the author pivot the Universe, let's clean it
        t_character_info_ms = marvel_dc_characters_ms.drop(['Universe', 'ID'], axis = 1).drop_duplicates() 
        # get the ones with unique Universe
        universe_clean = marvel_dc_characters_ms.groupby('Name')['Universe'].count().reset_index(name='Count').query('Count == 1').drop('Count', axis = 1).merge(marvel_dc_characters_ms, how='left').loc[:, ['Name', 'Universe']]
        print(round(1-len(t_character_info_ms)/len(marvel_dc_characters_ms), 2)*100, "% duplicates removed.")
        characters_wiki = pd.concat([marvel_characters_info, t_character_info_ms], ignore_index=True).merge(universe_clean, how='left')
        print(len(characters_wiki[characters_wiki.duplicated(subset='Name', keep=False)]), " duplicated names  in the same Universe or different universe, e.g., Spider-Man, Captain Marvel, etc. Small impact, ignore.")
        # add foreign key 
        o_character_wiki = characters_wiki.merge(o_characters, left_on='Name', right_on='character_name', how = 'left').drop('character_name', axis=1).drop('Name', axis=1).drop('Alignment', axis=1).rename(columns={'FirstAppearance': 'first_appearance'}).drop(['ID'], axis=1)
        o_character_wiki.insert(0, 'character_wiki_id', range(0, len(o_character_wiki)))
        o_character_stats = characters_stats.merge(o_characters, left_on='Name', right_on='character_name', how = 'left').drop('character_name', axis=1).drop('Name', axis=1)
        o_character_stats.insert(0, 'character_stat_id', range(0, len(o_character_stats)))
        # reset character index for charactersToComics
        o_comics = comics.drop_duplicates()
        o_comics['comicID'] = o_comics['comicID'].astype(str)
        o_charactersToComics = charactersToComics.drop_duplicates().merge(characters).merge(o_characters, left_on='name', right_on='character_name').loc[:, ['character_id', 'comicID']]
        o_charactersToComics['comicID'] = o_charactersToComics['comicID'].astype(str)
        return (o_characters,o_charactersToPowers,o_powers,o_character_stats,o_character_wiki, o_charactersToComics,o_comics)
    except Exception as e:
        logging.info('Preprocessing failed:')
        logging.error(e)

# to do: - [ ] character_wiki.first_appearance should be in datetime format, enforce alembic schema first


def transform_data(extracted_data):
    preprocessed_data = pre_process(extracted_data)
    o_characters,o_charactersToPowers,o_powers,o_character_stats,o_character_wiki, o_charactersToComics,o_comics = preprocessed_data
    character_power = o_characters.merge(o_charactersToPowers, how='left').merge(o_powers, how='left').apply(lambda x: x.astype('string')).to_json(orient = 'records')
    convert_dict = {'comic_id': str,
                'title':str,
                'issue_number':float,
                'description':object,
                'character_id':str}
    dict = {'comicID': 'comic_id',
            'issueNumber': 'issue_number'}
    character_comic = o_comics.merge(o_charactersToComics,how='left').rename(columns=dict).astype(convert_dict).to_json(orient = 'records')
    convert_dict = {'character_stat_id': str,
                    'alignment': str,
                    'intelligence': int,
                    'strength': int,
                    'speed': int,
                    'durability': int,
                    'power': int,
                    'combat': int,
                    'total': int,
                    'character_id': str}
    o_character_stats.columns = o_character_stats.columns.str.lower()
    character_stats = o_character_stats.astype(convert_dict).to_json(orient = 'records')
    convert_dict = {'character_wiki_id': str,
                    'gender': object,
                    'eyecolor': object,
                    'race': object,
                    'haircolor': object,
                    'publisher': object,
                    'skincolor': object,
                    'height': float,
                    'weight': float,
                    'identity': object,
                    'status': object,
                    'appearances': pd.Int64Dtype(),
                    'first_appearance': object,
                    'year': pd.Int64Dtype(),
                    'universe': object,
                    'character_id': object}
    o_character_wiki.columns = o_character_wiki.columns.str.lower()
    character_wikis = o_character_wiki.astype(convert_dict).to_json(orient = 'records')
    character_wikis = character_wikis.replace('"first_appearance":"nan"', '"first_appearance":null')
    logging.info('Transform completed!')
    return (character_power, character_stats, character_comic, character_wikis)