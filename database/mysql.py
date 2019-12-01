from .mysql_connection import MySQLConnection
from .mysql_connection import mysql_execute
from pymysql.err import *
import logging


Logger = logging.getLogger("app."+__name__)

def get_title_by_aid(aid: int):
    query = """
    SELECT title
    FROM articles
    WHERE article_id = %(aid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'aid': aid})
    return result


def get_article_by_aid(aid: int):
    query = """
            SELECT *
            FROM articles
            WHERE article_id = %(aid)s
            ;
            """
    _, result, err = mysql_execute(query, {'aid': aid})
    return result[0] if result else None, err


def get_entries_by_aid(aid: int):
    query = """
    SELECT link, journal_id, journal_name
    FROM article_entries NATURAL JOIN jid_name
    WHERE article_id = %(aid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'aid': aid})
    return result


def get_article_lemma(jid=None):
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            if not jid:
                query = """
                SELECT *
                from article_lemma
                ;
                """
                cursor.execute(query)
                return cursor.fetchall()
            else:
                Logger.error('not implemented')


def get_field_by_jid(jid: int):
    query = """
    SELECT field
    FROM jid_field
    WHERE journal_id=%(jid)s
    ;
    """
    ret, result, err = mysql_execute(query, {'jid': jid})
    return [item['field'] for item in result]


def get_jname_by_id(jid: int):
    query = """
    SELECT journal_name
    FROM jid_name
    WHERE journal_id=%(jid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'jid': jid})
    return result[0] if result else None


def get_jid_name():
    query = """
    SELECT *
    FROM jid_name
    LIMIT 10
    ;
    """
    _, result, _ = mysql_execute(query)
    return result


def search_journal_by_name(keyword: str):
    Logger.info(f'DB select journal with keyword: {keyword}')
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
    Logger.info(f'DB update jname of id:{jid} to {name}')
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
    Logger.info(f'DB delete journal with id:{jid}')
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            try:
                query = """
                DELETE FROM jid_name
                WHERE journal_id = %(jid)s
                ;
                """
                cursor.execute(query, {'jid': jid})
            except MySQLError as err:
                Logger.error(f'DB delete journal failed: {err}')
                return err


def insert_journal_name(jname: str):
    Logger.info(f'DB insert journal with name:{jname}')
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO jid_name (journal_name)
                    VALUE (%(jname)s)
                    ;
                    """
            cursor.execute(query, {'jname': jname})
