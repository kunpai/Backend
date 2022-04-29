from crypt import methods
import sqlite3
from unicodedata import name
import requests
from flask import Flask, g, request, jsonify, Response
import pandas as pd
import json

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

@app.route("/api/details", methods= ['GET', 'POST'])
def getDetails():
    name = request.get_json()['slug']
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute("SELECT * FROM data WHERE slug LIKE ?", [(name.lower().replace(' ','-'))])
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row[1],
                'name' : row[2],
                'short_description' : row[5],
                'long_description' : row[4],
                'genres' : row[11],
                'ratings' : row[9],
                'review_url' : row[8],
                'slug' : row[10]
            }
            results.append(row)
            break
        return Response(json.dumps(results),  mimetype='application/json')

    else:
        return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')

## ----------------------------------------- ##

# Takes in a genre and a media type
# Returns everything that fulfils those two parameters

@app.route("/api/recommend", methods= ['GET', 'POST'])
def getRecommend():
    media_type = request.get_json()['media_type']
    genre = request.get_json()['genres']
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute("SELECT * FROM data WHERE media_type LIKE ?", (media_type.title(),))
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row[1],
                'name' : row[2],
                'short_description' : row[5],
                'long_description' : row[4],
                'genres' : row[11],
                'ratings' : row[9],
                'review_url' : row[8],
                'slug' : row[10]
            }
            if genre in row['genres']:
                results.append(row)
        return Response(json.dumps(results),  mimetype='application/json')
    if len(results) == 0:
            return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')

## ----------------------------------------- ##

# Takes in a publisher and a media type
# Returns everything that fulfils those two parameters

@app.route("/api/publisher", methods= ['GET', 'POST'])
def getPublished():
    media_type = request.get_json()['media_type']
    published_by = request.get_json()['published_by']
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute("SELECT * FROM data WHERE media_type LIKE ?", (media_type.title(),))
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row[1],
                'name' : row[2],
                'short_description' : row[5],
                'long_description' : row[4],
                'genres' : row[11],
                'ratings' : row[9],
                'review_url' : row[8],
                'slug' : row[10],
                'published_by' : row[13]
            }
            if published_by in row['published_by']:
                results.append(row)
        if len(results) == 0:
            return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')
        return Response(json.dumps(results),  mimetype='application/json')

    else:
        return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')

## ----------------------------------------- ##

# Takes a franchise
# Returns everything part of the Franchise

@app.route("/api/franchise", methods = ['GET', 'POST'])
def getFranchise():
    franchise = request.get_json()['franchise']
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute("SELECT * FROM data")
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row[1],
                'name' : row[2],
                'short_description' : row[5],
                'long_description' : row[4],
                'genres' : row[11],
                'ratings' : row[9],
                'review_url' : row[8],
                'slug' : row[10],
                'published_by' : row[13],
                'franchise': row[14]
            }
            if franchise in row['franchise']:
                results.append(row)
        if len(results) == 0:
            return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')
        return Response(json.dumps(results),  mimetype='application/json')

    else:
        return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')

## ----------------------------------------- ##

# Takes a media type and a franchise
# Searches and returns results

@app.route("/api/mediafranchise", methods = ['GET', 'POST'])
def getMediaFranchise():
    franchise = request.get_json()['franchise']
    media_type = request.get_json()['media_type']
    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()
    cur.execute("SELECT * FROM data WHERE media_type LIKE ?", (media_type.title(),))
    rows = cur.fetchall()
    results = []
    if len(rows)>0:
        for row in rows:
            row = {
                'media_type' : row[1],
                'name' : row[2],
                'short_description' : row[5],
                'long_description' : row[4],
                'genres' : row[11],
                'ratings' : row[9],
                'review_url' : row[8],
                'slug' : row[10],
                'published_by' : row[13],
                'franchise': row[14]
            }
            if franchise in row['franchise']:
                results.append(row)
        if len(results) == 0:
            return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')
        return Response(json.dumps(results),  mimetype='application/json')

    else:
        return Response(json.dumps({'error': 'No media found'}),  mimetype='application/json')

## ----------------------------------------- ##

# Running the application

if __name__ == "__main__":
    app.run(debug=True)
