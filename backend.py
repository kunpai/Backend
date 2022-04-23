import sqlite3
from unicodedata import name
import requests
from flask import Flask, request, jsonify
import pandas as pd

## ----------------------------------------- ##
## Putting data into SQLite3 database
data = pd.read_csv('codefoobackend_cfgames.csv')   
df = pd.DataFrame(data)

DATABASE = './database.db'
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS data (id NUMBER, media_type TEXT, name TEXT, short_name TEXT, long_description TEXT, short_description TEXT, created_at TEXT, updated_at TEXT, review_url TEXT, review_score NUMBER, slug TEXT, genres TEXT, created_by TEXT, published_by TEXT, franchises TEXT, regions TEXT)"
cursor.execute(create_table)

for row in df.itertuples():
    cursor.execute("INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16]))

connection.commit()

## ----------------------------------------- ##
# Creating Flask app

app = Flask(__name__)

## ----------------------------------------- ##

# Creating API endpoint that returns a name, media type, genre, and descriptions
# Functions as a search

@app.route("/details", methods= ['GET', 'POST'])
def getDetails():
    name = request.get_json()['slug']
    cur = DATABASE.cursor()
    cur.execute("SELECT * FROM data WHERE name LIKE ? or short_name LIKE ?", (name.lower().replace(' ','-'), name.lower().replace(' ','-')))
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row['media_type'],
                'name' : row['name'],
                'short_description' : row['short_description'],
                'long_description': row['long_description'],
                'genres': row['genres']
            }
            results.append(row)
        return results
    else:
        return None


## ----------------------------------------- ##
# Running the application

if __name__ == "__main__":
    app.run(debug=True)
