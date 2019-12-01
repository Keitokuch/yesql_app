import scipy.sparse
import numpy as np
#  from sklearn.feature_extraction.text import CountVectorizer
#  from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import NearestNeighbors
#  from sklearn.linear_model import LogisticRegression
import pickle
from utils.timer import Timer
from model import Tfidf
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
