from .mysql_connection import MySQLConnection


def get_jname_by_id(jid: int):
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT journal_name
                    FROM jid_name
                    WHERE journal_id=%(jid)s
                    ;
                    """
            cursor.execute(query, {'jid': jid})
            return cursor.fetchone()


def get_jid_name():
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT *
                    FROM jid_name
                    LIMIT 10
                    ;
            """
            cursor.execute(query)
            return cursor.fetchall()


def search_journal_by_name(keyword: str):
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT *
                    FROM jid_name
                    WHERE journal_name LIKE %s
                    LIMIT 15
                    ;
                    """
            cursor.execute(query, "%" + keyword + "%")
            return cursor.fetchall()


def update_jname_by_id(jid: int, name: str):
    with MySQLConnection() as conn:
            with conn.cursor() as cursor:
                query = """
                UPDATE jid_name
                SET journal_name=%(jname)s
                WHERE journal_id=%(jid)s
                ;
                """
                cursor.execute(query, {'jname': name, 'jid': jid})
                return 0



def delete_journal_by_id(jid: int):
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    DELETE FROM jid_name
                    WHERE journal_id = %(jid)s
                    ;
            """
            cursor.execute(query, {'jid': jid})


def insert_journal_name(jname: str):
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO jid_name (journal_name)
                    VALUE (%(jname)s)
                    ;
                    """
            cursor.execute(query, {'jname': jname})
