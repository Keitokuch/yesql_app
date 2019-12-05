from database import neo4jdb

#  ret = neo4jdb.get_likes_by_uid(11)
ret = neo4jdb.users_also_viewed(1, 1)

ret = neo4jdb.find_similar_user_articles(11)

print(ret)

#  neo4jdb.add_read_articles(1, 1)
#  neo4jdb.add_read_articles(2, 1)
#  neo4jdb.add_read_articles(2, 5)
#  neo4jdb.add_read_articles(3, 1)
#  neo4jdb.add_read_articles(3, 7)
#  neo4jdb.add_read_articles(3, 11)
#  neo4jdb.add_read_articles(4, 1)
#  neo4jdb.add_read_articles(4, 13)
