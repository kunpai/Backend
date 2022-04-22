import imp
import pandas as pd
import sqlite3
import json
from flask import Flask
from flask import g

data = pd.read_csv (r'codefoobackend_cfgames.csv')   
df = pd.DataFrame(data)

app = Flask(__name__)
DATABASE = './database.db'

def create_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS data (id TEXT media_type TEXT name TEXT short_name TEXT long_description TEXT short_description TEXT created_at TEXT updated_at TEXT review_url TEXT review_score TEXT slug TEXT genres TEXT created_by TEXT published_by TEXT franchises TEXT regions TEXT)')
        db.commit()
    db.row_factory = sqlite3.Row
    return db



