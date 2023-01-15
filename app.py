import pickle

from resources.bm25 import BM25
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
from spellchecker import SpellChecker
from sqlalchemy_utils.functions import database_exists, create_database

from controllers.animeController import AnimeController
from controllers.authController import AuthController
from models.database import db

spell = SpellChecker(language='en')
parsed_data = pickle.load(open('resources/parsed_data.pkl', 'rb'))
bm25_title = pickle.load(open('src/bm25_title.pkl', 'rb'))
bm25_synopsis = pickle.load(open('src/bm25_synopsis.pkl', 'rb'))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    print('Creating a database')
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def AuthLogin():
    return AuthController.auth()

@app.route('/animeTitle', methods=['POST'])
def AnimeTitle():
    return AnimeController.query_title()

@app.route('/animeDescription', methods=['POST'])
def AnimeDescription():
    return AnimeController.query_description()

if __name__ == '__main__':
    app.run(debug=True)