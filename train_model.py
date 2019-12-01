import scipy.sparse
import numpy as np
from database import mysql as db
from utils.timer import Timer
from model import Tfidf
import json
import pickle


if __name__ == "__main__":
    timer = Timer()

    article_lemma = db.get_article_lemma()

    timer('select')

    text = [json.loads(item['lemma_list']) for item in article_lemma]
    ids = [int(item['article_id']) for item in article_lemma]

    timer('text')

    tfidf = Tfidf()
    vectors = tfidf.fit_transform(text)

    timer('vectorize')
    print(type(vectors), vectors.shape)

    scipy.sparse.save_npz('local/lemma_vectors.npz', vectors)
    np.save('local/aid_list.npy', ids)
    with open('local/tfidf.bin', 'wb') as f:
        pickle.dump(tfidf, f)

    timer('dump')
    ids = np.load('local/aid_list.npy')
    print(ids)
