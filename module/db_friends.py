#!/usr/bin/python
import uuid
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
import logging
import module

# generate uuid
def gen_id(row):
    return str(uuid.uuid4())

def create_db_ifnot_exist(connection_string):
    engine = create_engine(connection_string)
    if database_exists(engine.url):
        print("db already exists")
    else:
        create_database(engine.url)
        print("New db just created!")
    module.basic_logging_configure()
    logging.info("Database ready to use. Use alembic to migrate schema next")
