import pymysql
from dbconfig import db_config

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

