import csv
import sqlite3
from numpy import insert
import pandas as pd

data = pd.read_csv('codefoobackend_cfgames.csv')   
df = pd.DataFrame(data)

DATABASE = './database.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
#file = open('codefoobackend_cfgames.csv')
#contents = csv.reader(file)

create_table = "CREATE TABLE IF NOT EXISTS data (id TEXT, media_type TEXT, name TEXT, short_name TEXT, long_description TEXT, short_description TEXT, created_at TEXT, updated_at TEXT, review_url TEXT, review_score TEXT, slug TEXT, genres TEXT, created_by TEXT, published_by TEXT, franchises TEXT, regions TEXT)"
cursor.execute(create_table)
print(df)

for row in df.itertuples():
    insert_sql = f"INSERT INTO data(id,media_type,name,short_name,long_description,short_description,created_at,updated_at,review_url,review_score,slug,genres,created_by,published_by,franchises,regions) VALUES ('{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}', '{row[7]}', '{row[8]}', '{row[9]}', '{row[10]}', '{row[11]}', '{row[12]}', '{row[13]}', '{row[14]}', '{row[15]}', '{row[16]}')"
    cursor.execute(insert_sql)
    break

connection.commit()





# insert_records = "INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
# cursor.executemany(insert_records, contents)
# select_all = "SELECT * FROM id"
# rows = cursor.execute(select_all).fetchall()
# for r in rows:
#     print(r)

# connection.commit()
# connection.close()