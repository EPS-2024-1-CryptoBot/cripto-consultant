import os # pragma: no cover
import psycopg2
from sqlalchemy import insert # pragma: no cover

from log import get_logger


class PostgresConnector: # pragma: no cover
    def __init__(self):
        self.__db_user = os.environ.get("PG_USER")
        self.__db_pass = os.environ.get("PG_PASS")
        self.__db_host = os.environ.get("PG_HOST")
        self.__db_name = os.environ.get("PG_DB")
        self.__db_ssl = os.environ.get("PG_SSL") or False
        self.__logger = get_logger(self.__class__.__name__)
        self.establish_connection()

    @property
    def __conn_string(self):
        ssl_mode = "?ssl=require" if bool(self.__db_ssl) else ""
        return f"postgres://{self.__db_user}:{self.__db_pass}@{self.__db_host}/{self.__db_name}{ssl_mode}"
    
    def execute_stmt(self, stmt):
        self.session.execute(stmt)
        self.session.commit()

    def insert_on_conflict(self, Table, pks: list, data: dict) -> int:
        insert_stmt = insert(Table).values(data)
        insert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=pks,
            set_=dict(insert_stmt.excluded)
        )
        try:
            self.execute_stmt(insert_stmt)
            return 1
        except:
            return -1
        
    def insert(self, Table, data: dict) -> int:
        insert_stmt = insert(Table).values(data)
        try:
            self.execute_stmt(insert_stmt)
            return 1
        except Exception as e:
            print(e)
            return -1

    def establish_connection(self):
        self.__logger.info(f"ESTABLISHING CONNECTION TO POSTGRES DATABASE")
        self.connection = psycopg2.connect(self.__conn_string)

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.__logger.info(f"POSTGRES CONNECTED SUCCESSFULLY")

    def select_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return 1, "success"
        except Exception as e:
            print(e)
            return -1, e

    def close_connection(self):
        self.connection.close()