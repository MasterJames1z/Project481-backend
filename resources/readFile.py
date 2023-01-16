import pickle
import string

import pandas as pd
from nltk import PorterStemmer, word_tokenize


def get_data(path):
    # Read data
    df = pd.read_json(path, orient='records')
    df.drop(columns=['approved', 'titles', 'title_english', 'title_japanese', 'title_synonyms'], inplace=True)
    df['images'] = df['images'].apply(lambda x: x['jpg']['image_url'])
    df['trailer'] = df['trailer'].apply(lambda x: x['url'])
    df['producers'] = df['producers'].apply(lambda x: [i['name'] for i in x])
    df['licensors'] = df['licensors'].apply(lambda x: [i['name'] for i in x])
    df['studios'] = df['studios'].apply(lambda x: [i['name'] for i in x])
    df['genres'] = df['genres'].apply(lambda x: [i['name'] for i in x])
    df['themes'] = df['themes'].apply(lambda x: [i['name'] for i in x])
    df['demographics'] = df['demographics'].apply(lambda x: [i['name'] for i in x])

    # cleaning title
    cleaned_title = df['title']
    cleaned_title = cleaned_title.apply(lambda x: x.lower())
    cleaned_title = cleaned_title.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['title'] = cleaned_title

    # cleaning synopsis
    cleaned_synopsis = df['synopsis']
    cleaned_synopsis = cleaned_synopsis.apply(lambda x: x.lower() if x is not None else '')
    cleaned_synopsis = cleaned_synopsis.apply(
        lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['synopsis'] = cleaned_synopsis

    # cleaning background
    cleaned_background = df['background']
    cleaned_background = cleaned_background.apply(lambda x: x.lower() if x is not None else '')
    cleaned_background = cleaned_background.apply(
        lambda x: x.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    df['background'] = cleaned_background

    cleaned_score = df['score']
    cleaned_score = cleaned_score.apply(lambda x: x.lower() if x is str else 0)
    df['score'] = cleaned_score

    cleaned_scored_by = df['scored_by']
    cleaned_scored_by = cleaned_scored_by.apply(lambda x: x.lower() if x is str else 0)
    df['scored_by'] = cleaned_scored_by

    pickle.dump(df, open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/resources/parsed_data.pkl', 'wb'))
    return df

def pre_process(s):
    ps = PorterStemmer()
    s = word_tokenize(s)
    s = [ps.stem(w) for w in s]
    s = ' '.join(s)
    s = s.translate(str.maketrans('', '', string.punctuation + u'\xa0'))
    return s


df = get_data("C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/anime.json")