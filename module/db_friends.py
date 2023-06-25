#!/usr/bin/python
import uuid
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
import logging
import module
from datetime import datetime
from dotenv import load_dotenv
import os


def generate_conn_str():
    load_dotenv()
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_db = os.getenv("POSTGRES_DB")
    connection_string = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_db}"
    return connection_string

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
    logging.info("Database ready to use.")

def convert_to_datetime(date_str):
    date = datetime.strptime(date_str, "%Y, %B")
    return date.strftime("%Y-%m-%d 00:00:00")