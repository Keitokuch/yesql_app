import scipy.sparse
import numpy as np
import database.mysql as db
#  from sklearn.feature_extraction.text import CountVectorizer
#  from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import NearestNeighbors
#  from sklearn.linear_model import LogisticRegression
import pickle
from model import Tfidf
import json
from utils.timer import Timer
import logging
from utils.config import *

Logger = logging.getLogger('app.'+__name__)


class NNRecommender():
    def __init__(self, nn=10):
        timer = Timer()
        with open(LOCAL_DIR / 'tfidf.bin', 'rb') as f:
            self.tfidf = pickle.load(f)
        vectors = scipy.sparse.load_npz(LOCAL_DIR / 'lemma_vectors.npz')
        self.ids = [int(i) for i in np.load(LOCAL_DIR / 'aid_list.npy')]
        self.knn = NearestNeighbors(n_neighbors=nn, metric='cosine')
        self.knn.fit(vectors)
        Logger.info(f'Recommender loaded in {next(timer)} seconds')

    def find_similar(self, aid):
        s = db.get_lemma_by_aid(aid)
        lemma_list = json.loads(s) if s else []
        query_vector = self.tfidf.transform(lemma_list)
        dists, indices = self.knn.kneighbors(query_vector)
        result_ids = [self.ids[idx] for idx in indices]
        return result_ids

    def lemma_search(self, query_str):
        query_vector = self.tfidf.transform(query_str)
        dists, indices = self.knn.kneighbors(query_vector)
        indices = indices[0]
        result_ids = [self.ids[idx] for idx in indices]
        return result_ids


if __name__ == "__main__":
    import service.article_service as articles
    timer = Timer()

    with open('local/tfidf.bin', 'rb') as f:
        tfidf = pickle.load(f)

    vectors = scipy.sparse.load_npz('local/lemma_vectors.npz')
    ids = [int(i) for i in np.load('local/aid_list.npy')]

    timer('load')
    print(type(vectors), vectors.shape)


    knn = NearestNeighbors(n_neighbors=10, metric='cosine')
    knn.fit(vectors)

    timer('knn')
    #  query_phrase = "experiment evidence to see what is on research data statistics"
    #  query = lemmatize(query_phrase)
    #  print(query)
    #  query_vector = tfidf.transform([query])

    dists, indices = knn.kneighbors(vectors[30])
    #  dists, indices = knn.kneighbors(query_vector)
    for i in range(5):
        index = indices[0][i]
        dist = dists[0][i]
        aid = ids[index]
        print('#{} distance: {}, no:{}, text:\n{} \n'.format(i, dist, index,
                                                            articles.get_by_id(aid).abstract))
        #  print('#{} distance: {}, no:{}, text:\n{} \n'.format(i, dist,
                                                    #  index, tfidf._tfidf.inverse_transform(vectors[indices[0][i]])))
