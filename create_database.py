import sqlite3
import pandas as pd

# create database connection
connection = sqlite3.connect('venv/data/slang.db')

# assigning csv file to a variable & making sure to encode emoji
# abusive_data = pd.read_csv('venv/data/abusive.csv', encoding='latin-1')

try:
    connection.execute("""CREATE TABLE slangwords (alay VARCHAR(255), baku VARCHAR(255)); """)
    print("table created!")
except: 
    print("table already exists!")

# import data to dataframe
kamus_alay_df = pd.read_csv('venv/data/new_kamusalay.csv', names=['alay', 'baku'], encoding='latin-1', header=None)

# import dataframe to database
kamus_alay_df.to_sql(name='slangwords', con=connection, if_exists='replace', index=False)

connection.commit()
connection.close()

