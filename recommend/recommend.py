import scipy.sparse
#  from sklearn.feature_extraction.text import CountVectorizer
#  from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import NearestNeighbors
#  from sklearn.linear_model import LogisticRegression
import pickle
from utils.timer import Timer
from models.tfidf import Tfidf


timer = Timer()

with open('models/tfidf.bin', 'rb') as f:
    tfidf = pickle.load(f)

vectors = scipy.sparse.load_npz('models/lemma_vectors.npz')

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
    print('#{} distance: {}, no:{}, text:\n{} \n'.format(i, dists[0][i],
                                                  indices[0][i], tfidf._tfidf.inverse_transform(vectors[indices[0][i]])))
    #  print('#{} distance: {}, text:\n{} \n'.format(i, dists[0][i], text[indices[0][i]]))
