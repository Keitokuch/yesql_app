from database import neo4jdb
import random

#  ret = neo4jdb.get_likes_by_uid(11)
# ret = neo4jdb.users_also_viewed(1, 1)
#
# ret = neo4jdb.find_similar_user_articles(11)

# print(ret)

ulist = []
alist = []
for i in range(100):
    print('sdff')
    print(i)
    alist.append(random.randint(1, 40))
    ulist.append(random.randint(1, 1000))
    neo4jdb.add_read_articles(ulist[i], alist[i])
    if (i < 30):
        neo4jdb.add_like_articles(ulist[i], alist[i])


#
#  neo4jdb.add_read_articles(2, 1)
#  neo4jdb.add_read_articles(2, 5)
#  neo4jdb.add_read_articles(3, 1)
#  neo4jdb.add_read_articles(3, 7)
#  neo4jdb.add_read_articles(3, 11)
#  neo4jdb.add_read_articles(4, 1)
#  neo4jdb.add_read_articles(4, 13)
