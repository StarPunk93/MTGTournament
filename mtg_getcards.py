#!/usr/bin/env python3
import sqlalchemy
import requests
import json
import MySQLdb
from config import Config

import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine


season = 'ISD'
url = 'https://api.magicthegathering.io/v1/cards?set=' + season + '&page='
page = 1
nextpage = True

frames = []

r = requests.get(url + str(1))
data = r.json()['cards']
df1 = pd.json_normalize(data)
df1.set_index('id', inplace = True)
if len(df1) == 100:
    r = requests.get(url + str(2))
    data = r.json()['cards']
    df2 = pd.json_normalize(data)
    df2.set_index('id', inplace = True)
    if len(df2) == 100:
        r = requests.get(url + str(3))
        data = r.json()['cards']
        df3 = pd.json_normalize(data)
        df3.set_index('id', inplace = True)
        if len(df3) == 100:
            r = requests.get(url + str(4))
            data = r.json()['cards']
            df4 = pd.json_normalize(data)
            df4.set_index('id', inplace = True)
            if len(df4) == 100:
                r = requests.get(url + str(5))
                data = r.json()['cards']
                df5 = pd.json_normalize(data)
                df5.set_index('id', inplace = True)
                frames = [df1, df2, df3, df4, df5]
            else:
                frames = [df1, df2, df3, df4]
        else:
            frames = [df1, df2, df3]
    else:
        frames = [df1, df2]
else:
    frames = [df1]

result = pd.concat(frames, verify_integrity = True)
result = result.astype(str)

server = Config.DATABASE_CONFIG['server']
user = Config.DATABASE_CONFIG['user']
password = Config.DATABASE_CONFIG['password']
db = Config.DATABASE_CONFIG['name']

engine=create_engine(f'mysql+pymysql://{user}:{password}@{server}:3306/{db}'

            )

#result.to_sql(con=con, name='cards', if_exists='replace')
# engine = create_engine('sqlite:///cards.db', echo=True)
with engine.begin() as connection:
     result.to_sql('cards', con=connection, if_exists='append', method=None)

print(result)
