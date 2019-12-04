from .mysql_connection import MySQLConnection
from .mysql_connection import mysql_execute
from pymysql.err import *
import logging
import json
from typing import List


Logger = logging.getLogger("app."+__name__)


def get_uid_and_passwd_by_name(name: str):
    query = """
    SELECT user_id, passwd
    FROM user
    WHERE username = %(name)s
    ;
    """
    ret, result, err = mysql_execute(query, {'name': name})
    return result[0] if result else None, err


def get_user_by_uid(uid: int):
    query = """
    SELECT user_id, username
    FROM user
    WHERE user_id = %(uid)s;
    """
    ret, result, err = mysql_execute(query, {'uid': uid})
    return result[0] if ret else None


def insert_user(name: str, passwd: str):
    query = """
    INSERT INTO user(username, passwd)
    VALUE (%(name)s, %(passwd)s)
    ;
    """
    ret, _, err = mysql_execute(query, {'name': name, 'passwd': passwd})
    return ret, err


def get_aid_title():
    query = """
    SELECT article_id, title
    FROM articles
    LIMIT 50
    ;
    """
    ret, result, err = mysql_execute(query)
    return result


def article_title_search(search_key: str):
    query = """
    SELECT article_id, title
    FROM articles
    WHERE MATCH(title)
        AGAINST (%(search_key)s IN NATURAL LANGUAGE MODE)
    LIMIT 20;
    """
    ret, result, err = mysql_execute(query, {'search_key': search_key})
    return result


def article_full_search(search_key: str):
    query = """
    SELECT article_id, title
    FROM articles
    WHERE MATCH(title, authors, abstract)
        AGAINST (%(search_key)s IN NATURAL LANGUAGE MODE)
    LIMIT 20;
    """
    ret, result, err = mysql_execute(query, {'search_key': search_key})
    return result


def get_lemma_by_aid(aid: int):
    query = """
    SELECT article_id, lemma_list
    FROM article_lemma
    WHERE article_id = %(aid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'aid': aid})
    return result[0]['lemma_list'] if result else None


def get_title_by_aid(aid: int):
    query = """
    SELECT article_id, title
    FROM articles
    WHERE article_id = %(aid)s
    ;
    """
    _, result, _ = mysql_execute(query, {'aid': aid})
    return result


def get_title_by_aids(aids: List[int]):
    query = f"""
    SELECT article_id, title
    FROM articles
    WHERE article_id IN ({','.join(['%s'] * len(aids))})
    ;
    """
    ret, result, err = mysql_execute(query, tuple(aids))
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
