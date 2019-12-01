from recommend.recommend import NNRecommender

nn = NNRecommender(5)

outputs = nn.find_similar(5)

print(outputs)
