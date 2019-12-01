import service.article_service as articles

for i in range(50):
    new = articles.get_by_id(i)
    print(new.entries)
