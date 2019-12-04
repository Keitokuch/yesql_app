import pymysql
from pymysql.err import *
from .dbconfig import db_config
import sys
import logging


Logger = logging.getLogger("app."+__name__)

class MySQLConnection:
    def __init__(self, config: dict=db_config):
        self._connection = None
        self._config = config

    def __enter__(self) -> pymysql.Connection:
        self._connection = pymysql.connect(**self._config)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.commit()
        self._connection.close()


def mysql_execute(query, args=None):
    caller = sys._getframe(1).f_code.co_name
    Logger.debug(f'MySQL {caller} {args}')
    with MySQLConnection() as conn:
        with conn.cursor() as cursor:
            try:
                ret = cursor.execute(query, args)
                result = cursor.fetchall()
                return ret, result, None
            except MySQLError as err:
                Logger.error(f'MySQL Failed in {caller}: {err}')
                return -1, [], err
