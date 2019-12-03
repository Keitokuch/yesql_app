import service.article_service as articles
#  from recommend import Recommender

res = articles.lemma_search('machine learning in gaming')

#  res = Recommender.lemma_search('machine learning in gaming')
#  res = articles.title_search('machine learning in gaming')
#  res = articles.full_search('machine learning in gaming')

ids = [item['article_id'] for item in res]
print(ids)
