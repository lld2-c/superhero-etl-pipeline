from .transform import transform_data
import pandas as pd
from models import * # import all schemas
from sqlalchemy.orm import sessionmaker
from config.configurations import connection_string
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import json

from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

def load_data(transformed_data):
    o_characters, o_charactersToComics, o_charactersToPowers, o_character_stats, o_comics, o_powers, o_character_wiki = transformed_data
    characters_o = o_characters.apply(lambda x: x.astype('string')).head().to_json(orient = 'records')
    obj = json.loads(characters_o)
    # [-] pipe it to SQL database (19/jun)
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    for entry in obj:
        character = Character(**entry)
        character_name = entry.get('character_name')

        # Check if character_id already exists in the database
        existing_character = session.query(Character).filter_by(character_name=character_name).first()

        if existing_character:
            print(f"Character '{character_name}' already exists")
        else:
            # Add more fields and relationships if needed
            session.add(character)

    session.commit()
    session.close()


