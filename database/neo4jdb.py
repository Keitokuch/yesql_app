from neo4j import GraphDatabase


driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "8888"))


def add_read_articles(uid, aid):
    with driver.session() as session:
        session.run("MERGE (u:User {id: {uid}})", uid=uid)
        session.run("MERGE (a:Article {id: {read_article_id}})", read_article_id=aid)
        result = session.run(
            "MATCH (u:User {id: {uid}}), (a:Article {id: {read_article_id}}) MERGE (u)-[:Read]->(a)",
            uid=uid, read_article_id=aid
        )
        result = list(result)
        print("rows: {}".format(len(result)))


def add_like_articles(uid, aid):
    with driver.session() as session:
        session.run("MERGE (a:Article {id: {like_article_id}})", like_article_id=aid)
        result = session.run(
            "MATCH (u:User {id: {uid}}), (a:Article {id: {like_article_id}}) MERGE (u)-[:Like]->(a)",
            uid=uid, like_article_id=aid
        )
        result = list(result)
        print("rows: {}".format(len(result)))


def remove_like_articles(uid, aid):
    with driver.session() as session:
        session.run(
            "MATCH (u:User {id: {uid}})-[r:Like]-(a:Article {id: {aid}}) "
            "DELETE r",
            uid=uid, aid=aid
        )


def find_similar_user_articles(uid):
    with driver.session() as session:
        # store read relation uid
        uid_res = session.run(
            "MATCH (u1:User {id: {uid}})-[r:Read]-(a:Article)-[:Like]-(u2:User) "
            "RETURN u2.id, COUNT(r) "
            "ORDER BY COUNT(r) DESC",
            uid=uid
        )

        uid_dict = {}
        for record in uid_res:
            uid_dict[record["u2.id"]] = record["COUNT(r)"]

        # store like relation uid
        uid_res = session.run(
            "MATCH (u1:User {id: {uid}})-[r:Like]-(a:Article)-[:Like]-(u2:User) "
            "RETURN u2.id, COUNT(r) "
            "ORDER BY COUNT(r) DESC",
            uid=uid
        )
        for record in uid_res:
            uid_dict[record["u2.id"]] = record["COUNT(r)"]

        # arrange uid_list by most similar user first
        uid_list = find_most_similar_users(uid_dict)

        article_res = session.run(
            "MATCH (u:User)-[:Like]-(a:Article) "
            "WHERE u.id IN {uid_list} "
            "RETURN a.id, u.id ",
            parameters={'uid_list': uid_list}
        )

        # find most relevant articles and only return those under the limit value
        article_list = []
        for record in article_res:
            temp = (record["a.id"], record["u.id"])
            article_list.append(temp)
        res = find_most_relevant_articles(article_list, uid_list, 8)
        return res


def user_liked_article(uid, aid):
    with driver.session() as session:
        res = session.run(
            "MATCH (u:User {id: {uid}}), (a:Article {id: {aid}}) "
            "RETURN EXISTS((u)-[:Like]-(a)) ",
            uid=uid, aid=aid
        )
        return res.value()[0]


def find_most_similar_users(uid_dict):
    sorted_list = sorted(uid_dict.items(), key=lambda kv: -kv[1])
    res = []
    for item in sorted_list:
        res.append(item[0])
    return res


def find_most_relevant_articles(article_dict, uid_list, limit):
    res = []
    for idx, uid in enumerate(uid_list):
        for temp_tuple in article_dict:
            if temp_tuple[1] == uid and len(res) < limit:
                res.append(temp_tuple[0])
    return res



