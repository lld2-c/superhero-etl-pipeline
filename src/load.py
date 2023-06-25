import pandas as pd
from models import * # import all schemas
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import json
from typing import Tuple
from sqlalchemy.ext.compiler import compiles
import logging
import module


def loadCharactersNPowers(character_power: str):
    # connect database
    connection_string = module.generate_conn_str()
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # pass json data to database (characters, powers, character_power_association)
    json_obj = json.loads(character_power)
    for entry in json_obj:
        # characters table
        character_name = entry.get('character_name')
        existing_character = session.query(Character).filter_by(character_name=character_name).first()
        if existing_character:
            pass
        else:
            character = Character(character_id=entry['character_id'], character_name=entry['character_name'])
            session.add(character)
            session.commit()
        # powers table
        power_name = entry.get('power_name')
        if power_name is not None: 
            existing_power = session.query(Power).filter_by(power_name=power_name).first()
            if existing_power:
                pass
            else:
                power = Power(power_id=entry.get('power_id'), power_name=entry.get('power_name'))
                session.add(power)
                session.commit()
        # character_power_association table
        character_id = entry.get('character_id')
        power_id = entry.get('power_id')
        if power_id is not None: 
            existing_association = session.execute(f"SELECT * FROM character_power_association WHERE character_id = '{character_id}' AND power_id = '{power_id}';").first()
            if existing_association:
                pass
            else:
                session.execute(f"INSERT INTO character_power_association (character_id, power_id) VALUES ('{character_id}', '{power_id}');")
                session.commit()
    session.close()

def loadCharactersNComics(character_comic: str):
    # connect database
    connection_string = module.generate_conn_str()
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # pass json data to database (comics, character_comic_association)
    json_obj = json.loads(character_comic)
    for entry in json_obj:
        # comics table
        comic_id = entry.get('comic_id')

        existing_comic = session.query(Comic).filter_by(comic_id=comic_id).first()
        if existing_comic:
            pass
        else:
            comic = Comic(comic_id=entry['comic_id'],title=entry['title'],issue_number = entry['issue_number'],description=entry['description'])
            session.add(comic)
            session.commit()
        # character_comic_association table
        character_id = entry.get('character_id')
        comic_id = entry.get('comic_id')
        if character_id != 'nan': 
            existing_association = session.execute(f"SELECT * FROM character_comic_association WHERE character_id = '{character_id}' AND comic_id = '{comic_id}';").first()
            if existing_association:
                pass
            else:
                session.execute(f"INSERT INTO character_comic_association (character_id, comic_id) VALUES ('{character_id}', '{comic_id}');")
                session.commit()
    session.close()

def loadCharacterStats(character_stats: str):
    # connect database
    connection_string = module.generate_conn_str()
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # pass json data to database (comics, character_comic_association)
    json_obj = json.loads(character_stats)
    for entry in json_obj:
        # comics table
        character_id = entry.get('character_id')
        character_stat_id = entry.get('character_stat_id')
        if character_id != 'nan': 
            existing_stat = session.query(CharacterStat).filter_by(character_stat_id=character_stat_id).first()
            if existing_stat:
                pass
            else:
                stat = CharacterStat(**entry)
                session.add(stat)
                session.commit()
    session.close()

def loadCharacterWiki(character_wiki: str):
    # connect database
    connection_string = module.generate_conn_str()
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # pass json data to database (character_wiki)
    json_obj = json.loads(character_wiki)
    for entry in json_obj:
        # comics table
        character_id = entry.get('character_id')
        character_wiki_id = entry.get('character_wiki_id')
        if character_id != 'nan': 
            existing_stat = session.query(CharacterWiki).filter_by(character_wiki_id=character_wiki_id).first()
            if existing_stat:
                pass
            else:
                stat = CharacterWiki(**entry)
                session.add(stat)
                session.commit()
    session.close()

def load_data(transformed_data: Tuple[str, ...]):
    logging.info('Start loading..')
    try:
        character_power, character_stats, character_comic, character_wiki = transformed_data
        loadCharactersNPowers(character_power)
        logging.info('Load characters, powers and character_power_association completed!')
        loadCharactersNComics(character_comic)
        logging.info('Load comics and character_comic_association completed!')
        loadCharacterStats(character_stats)
        logging.info('Load character_stats completed!')
        loadCharacterWiki(character_wiki)
        logging.info('Load characters_wiki completed!')
        return True

    except Exception as e:
        logging.info('Load failed:')
        logging.error(e)
        
    

