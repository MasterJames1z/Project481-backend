import pickle

import numpy as np
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer


class BM25(object):
    def __init__(self, b=0.75, k1=1.6):
        self.vectorizer = TfidfVectorizer(norm=None, smooth_idf=False, ngram_range=(1, 3))
        self.b = b
        self.k1 = k1

    def fit(self, X):
        """ Fit IDF to documents X """
        self.vectorizer.fit(X)
        y = super(TfidfVectorizer, self.vectorizer).transform(X)
        self.X = y
        self.avdl = y.sum(1).mean()

    def transform(self, q):
        """ Calculate BM25 between query q and documents X """
        b, k1, avdl = self.b, self.k1, self.avdl

        len_X = self.X.sum(1).A1

        q, = super(TfidfVectorizer, self.vectorizer).transform([q])

        assert sparse.isspmatrix_csr(q)
        # convert to csc for better column slicing
        X = self.X.tocsc()[:, q.indices]
        denom = X + (k1 * (1 - b + b * len_X / avdl))[:, None]
        # idf(t) = log [ n / df(t) ] + 1 in sklearn, so it need to be coneverted
        # to idf(t) = log [ n / df(t) ] with minus 1
        idf = self.vectorizer._tfidf.idf_[None, q.indices] - 1.
        numer = X.multiply(np.broadcast_to(idf, X.shape)) * (k1 + 1)
        return (numer / denom).sum(1).A1


if __name__ == '__main__':
    parsed_data = pickle.load(open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/resources/parsed_data.pkl', 'rb'))

    bm25_title = BM25()
    bm25_title.fit(parsed_data['title'])
    pickle.dump(bm25_title, open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/src/bm25_title.pkl', 'wb'))

    bm25_synopsis = BM25()
    bm25_synopsis.fit(parsed_data['synopsis'])
    pickle.dump(bm25_synopsis, open('C:/Users/NITRO5/OneDrive/เดสก์ท็อป/IRproject/Project481-backend/Project481-backend/src/bm25_synopsis.pkl', 'wb'))