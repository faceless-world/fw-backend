"""
Module with class to create databases
"""

from psycopg2 import sql
from configs.postgresql.credentials import config as pg_creds
from modules.postgresql.requester import PostgresRequester


class PostgresCreator(PostgresRequester):
    """
    Class to create databases
    """
    def __init__(self):
        super().__init__()
        self._update_cursor(pg_creds['main_db_name'])
        self.cursor.execute("SELECT datname FROM pg_database;")
        current_dbs = [d[0] for d in self.cursor.fetchall()]
        if pg_creds['db_name'] not in current_dbs:
            self.cursor.execute(sql.SQL(
                """CREATE DATABASE {db_name};""").format(
                    db_name=sql.Identifier(pg_creds['db_name'])
                ))
