"""
Module with class to make requests to postgresql database
"""

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from configs.postgresql.credentials import config as pg_creds
import psycopg2


class PostgresRequester:
    """
    Class to make requests to postgresql database
    """
    def __init__(self):
        self._update_cursor(pg_creds['db_name'])


    def __del__(self):
        if getattr(self, 'connect', None) is not None:
            self.connect.close()
    
    
    def _update_cursor(self, db_name: str) -> None:
        """
        Update cursor of current connection
        :param db_name: Database name
        :type db_name: str
        """
        self.connect = psycopg2.connect(host=pg_creds['host'], port=pg_creds['port'],
                                        dbname=db_name,
                                        user=pg_creds['user'], password=pg_creds['password'])
        self.connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connect.cursor()
