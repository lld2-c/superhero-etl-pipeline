import pandas as pd
from .extract import extract_data
import module # custom modules


def transform_data(extracted_data):
    characters, charactersToComics, characters_stats, comics, marvel_characters_info, superheroes_power_matrix, marvel_dc_characters_ms = extracted_data
    t_characters = pd.concat([characters['name'], 
                                    superheroes_power_matrix['Name'],
                                    marvel_characters_info['Name'], 
                                    marvel_dc_characters_ms['Name']])\
                                    .drop_duplicates().sort_values().reset_index(drop=True)
    o_characters = pd.DataFrame(t_characters, columns=['character_name'])
    o_characters['character_id'] = o_characters.apply(module.gen_id, axis=1)
    # transform characters_to_powers M:N relationship
    t_charactersToPowers = pd.melt(superheroes_power_matrix, id_vars='Name', var_name='power', value_name='yn').query('yn == True').reset_index(drop=True).drop('yn', axis=1)
    o_powers = pd.DataFrame({'power_name': superheroes_power_matrix.columns}).drop(0).reset_index(drop=True)
    o_powers['power_id'] = o_powers.apply(module.gen_id, axis=1)
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
    o_character_wiki = characters_wiki.merge(o_characters, left_on='Name', right_on='character_name', how = 'left')
    o_character_stats = characters_stats.merge(o_characters, left_on='Name', right_on='character_name', how = 'left')
    # reset character index for charactersToComics
    o_comics = comics.drop_duplicates()
    o_charactersToComics = charactersToComics.drop_duplicates().merge(characters).merge(o_characters, left_on='name', right_on='character_name').loc[:, ['character_id', 'comicID']]
    return o_characters, o_charactersToComics, o_charactersToPowers, o_character_stats, o_comics, o_powers, o_character_wiki
