from recommend import NNRecommender
from recommend import Recommender

#  nn = NNRecommender(5)

#  outputs = nn.find_similar(5)
outputs = Recommender.find_similar(5)

print(outputs)
