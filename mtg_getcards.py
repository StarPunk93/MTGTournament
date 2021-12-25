#!/usr/bin/env python3
import sqlalchemy
import requests
import json
import sqlite3

import pandas as pd
from sqlalchemy import create_engine


season = 'VOW'
url = 'https://api.magicthegathering.io/v1/cards?set=' + season + '&page='
page = 1
nextpage = True

frames = []

r = requests.get(url + str(1))
data = r.json()['cards']
df1 = pd.json_normalize(data)
df1.set_index('id', inplace = True)
r = requests.get(url + str(2))
data = r.json()['cards']
df2 = pd.json_normalize(data)
df2.set_index('id', inplace = True)
r = requests.get(url + str(3))
data = r.json()['cards']
df3 = pd.json_normalize(data)
df3.set_index('id', inplace = True)
r = requests.get(url + str(4))
data = r.json()['cards']
df4 = pd.json_normalize(data)
df4.set_index('id', inplace = True)
r = requests.get(url + str(5))
data = r.json()['cards']
df5 = pd.json_normalize(data)
df5.set_index('id', inplace = True)

frames = [df1, df2, df3, df4, df5]

result = pd.concat(frames, verify_integrity = True)
result = result.astype(str)

engine = create_engine('sqlite:///cards.db', echo=True)
with engine.begin() as connection:
    result.to_sql('cards', con=connection, if_exists='replace', method=None)

print(result)
