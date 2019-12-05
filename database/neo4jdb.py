from neo4j import GraphDatabase


driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "8888"))


def add_read_articles(uid, aid):
    with driver.session() as session:
        session.run("MERGE (u:User {id: $uid})", uid=uid)
        session.run("MERGE (a:Article {id: $read_article_id})", read_article_id=aid)
        result = session.run(
            "MATCH (u:User {id: $uid}), (a:Article {id: $read_article_id}) MERGE (u)-[:Read]->(a)",
            uid=uid, read_article_id=aid
        )
        result = list(result)
        print("rows: {}".format(len(result)))


def add_like_articles(uid, aid):
    with driver.session() as session:
        session.run("MERGE (a:Article {id: $like_article_id})", like_article_id=aid)
        result = session.run(
            "MATCH (u:User {id: $uid}), (a:Article {id: $like_article_id}) MERGE (u)-[:Like]->(a)",
            uid=uid, like_article_id=aid
        )
        result = list(result)
        print("rows: {}".format(len(result)))


def find_similar_user_articles(uid):
    with driver.session() as session:
        # store read relation uid
        uid_res = session.run(
            "MATCH (u1:User {id: $uid})-[r:Read]-(a:Article)-[:Like]-(u2:User) "
            "RETURN u2.id, COUNT(r) "
            "ORDER BY COUNT(r) DESC",
            uid=uid
        )

        uid_list = []
        for record in uid_res:
            uid_list.append(record["u2.id"])

        # store like relation uid
        uid_res = session.run(
            "MATCH (u1:User {id: $uid})-[r:Like]-(a:Article)-[:Like]-(u2:User) "
            "RETURN u2.id, COUNT(r) "
            "ORDER BY COUNT(r) DESC",
            uid=uid
        )
        for record in uid_res:
            uid_list.append(record["u2.id"])

        print(uid_list, "sdsd")


        article_res = session.run(
            "MATCH (u:User)-[:Like]-(a:Article) "
            "WHERE u.id IN $uid_list "
            "RETURN a.id "
            "LIMIT 8",
            parameters={'uid_list': uid_list}
        )
        res = []
        for record in article_res:
            res.append(record["a.id"])
        print(res)
        return res


def clear_all_records():

    with driver.session() as session:
        session.run("MATCH (n)-[r]-() DELETE r")
        session.run("match (c) delete c")


# clear_all_records()
# add_read_articles(1, 3)
# add_read_articles(3, 3)
# add_like_articles(3, 3)
# add_like_articles(1, 4)
# add_read_articles(1, 5)
# add_read_articles(1, 6)
# add_read_articles(2, 4)
# add_like_articles(2, 3)
#
# add_read_articles(2, 8)
# add_like_articles(1, 8)
# find_similar_user_articles(2)

