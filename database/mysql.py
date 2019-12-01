from .mysql_connection import MySQLConnection
from .mysql_connection import mysql_execute
from pymysql.err import *
import logging
import json


Logger = logging.getLogger("app."+__name__)


def get_lemma_by_aid(aid: int):
    query = """
    SELECT lemma_list
    FROM article_lemma
    WHERE article_id = %(aid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'aid': aid})
    return result[0]['lemma_list'] if result else None


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
    query = """
    SELECT *
    FROM jid_name
    WHERE journal_name LIKE %s
    LIMIT 15
    ;
    """
    _, result, err = mysql_execute(query, "%" + keyword + "%")
    return result


def update_jname_by_id(jid: int, name: str):
    query = """
    UPDATE jid_name
    SET journal_name=%(jname)s
    WHERE journal_id=%(jid)s
    ;
    """
    ret, _, err = mysql_execute(query, {'jname': name, 'jid': jid})
    return err


def delete_journal_by_id(jid: int):
    query = """
    DELETE FROM jid_name
    WHERE journal_id = %(jid)s
    ;
    """
    _, _, err = mysql_execute(query, {'jid': jid})
    return err


def insert_journal_name(jname: str):
    query = """
    INSERT INTO jid_name (journal_name)
    VALUE (%(jname)s)
    ;
    """
    _, _, err = mysql_execute(query, {'jname': jname})
    return err
