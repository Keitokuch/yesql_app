from .mysql_connection import MySQLConnection


db_config = {
    'host': 'fa19-cs411-050.cs.illinois.edu',
    'user': 'root',
    'password': '123456',
    'db': 'pj'
}


def get_jname_by_id(jid: int):
    with MySQLConnection(db_config) as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT journal_name
                    FROM jid_name
                    WHERE journal_id=%(jid)s
                    ;
                    """
            cursor.execute(query, {'jid': jid})
            return cursor.fetchall()
