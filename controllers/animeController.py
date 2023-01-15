import pickle

import pandas as pd
from flask import jsonify, request
from spellchecker import SpellChecker

spell = SpellChecker(language='en')
bm25_title = pickle.load(open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/src/bm25_synopsis.pkl', 'rb'))
bm25_synopsis = pickle.load(open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/src/bm25_synopsis.pkl', 'rb'))
parsed_data = pickle.load(open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/resources/parsed_data.pkl', 'rb'))

class AnimeController:
    @staticmethod
    def query_title():
        query = request.args['title']
        spell_corr = [spell.correction(w) for w in query.split()]
        score = bm25_title.transform(query)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=10)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'content': df_bm.to_dict('records')}), 200

    @staticmethod
    def query_description():
        query = request.json['description']
        spell_corr = [spell.correction(w) for w in query.split()]
        score = bm25_synopsis.transform(query)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=10)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'content': df_bm.to_dict('records')}), 200