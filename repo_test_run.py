# Databricks notebook source
# MAGIC %sh
# MAGIC pip install -r requirements.txt

# COMMAND ----------

from sqlalchemy import create_engine
from config import conn_string
from config import out_conn_string
import module
import pandas as pd
from datetime import datetime

# set up input database conn
db_instance = module.pgconnect()
db_instance.connect(conn_string)

# get the base table
df = db_instance.query("""
SELECT 
bonnet_user_id AS user_id, 
business_uid,
created,
deleted_at
FROM fleet_fleet_drivers;""")
                       
df.head(5)

# initiate user_id, ym table
active_user = pd.DataFrame(columns=['user_id', 'ym'])

# Iterate through the rows of the input DataFrame
for index, row in df.iterrows():
    user_id = row['user_id']
    created_ym = pd.to_datetime(row['created']).strftime('%Y-%m')
    business_uid = row['business_uid']
    if pd.isna(row['deleted_at']):
        now_ym = datetime.now().strftime('%Y-%m')
        ym_range = pd.date_range(start=created_ym, end=now_ym, freq='MS').strftime('%Y-%m')
    else:
        deleted_ym = pd.to_datetime(row['deleted_at']).strftime('%Y-%m')
        ym_range = pd.date_range(start=created_ym, end=deleted_ym, freq='MS').strftime('%Y-%m')
    user_ym = pd.DataFrame({'user_id': user_id, 'ym': ym_range, 'business_uid': business_uid})
    active_user = pd.concat([active_user, user_ym])

# Print the resulting active_user DataFrame
active_user['ym'] = pd.to_datetime(active_user['ym'])
print(active_user)

# load this to the output database
engine = create_engine(out_conn_string)
active_user.to_sql('test_github_table11', engine, if_exists='replace', index=False)
