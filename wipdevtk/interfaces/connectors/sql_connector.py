from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import InterfaceError

from wipdevtk.dev.log import log
from wipdevtk.dev.mode import DEBUG, MODE
from wipdevtk.exceptions import handle_exception
from wipdevtk.meta import NamedSingleton


class SQLConnector(metaclass=NamedSingleton):
    def __init__(
        self,
        driver: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        connection_url: Optional[str] = None,
        drivername: Optional[str] = None,
        **kwargs,
    ):
        """ """

        if not connection_url:
            connection_url = URL.create(
                drivername=drivername,
                username=username,
                password=password,
                host=host,
                port=port,
                database=database,
            )
            log(f"[INFO] sql connection URL: {connection_url}", "DEBUG")

        self.connection_url = connection_url
        self.engine_params = kwargs

        self.connect(connection_url=connection_url, **kwargs)
        self.connect_events()

    def connect(self, connection_url: str, **kwargs):
        self.engine = create_engine(
            connection_url, pool_pre_ping=True, echo=(MODE == DEBUG), **kwargs
        )
        self.connection = self.engine.raw_connection()
        self.cursor = self.connection.cursor()

    def connect_events(self): ...

    def reconnect(self):
        self.connect(self.connection_url, **self.engine_params)

    def _execute(self, query, values=None):
        if values is not None:
            self.cursor.execute(query, *values)
        else:
            self.cursor.execute(query)
        try:
            ret = self.cursor.fetchall()
            if not ret:
                ret = None
        except Exception:
            ret = None
        return ret

    def execute_and_commit(self, query, values=None):
        ret = self._execute(query, values)

        self.cursor.commit()

        return ret

    def execute_no_commit(self, query, values=None):
        try:
            ret = self._execute(query, values)
            self.committed = False
            return ret

        except Exception:
            self.cursor.rollback()
            raise Exception(
                f"Error while executing SQL Query: {query}\nDatabase Rollback !"
            )

    def commit_queries(self):
        try:
            self.cursor.commit()
            self.committed = True

        except Exception:
            self.cursor.rollback()
            raise Exception("Error while while committing Queries\nDatabase Rollback !")

    def is_alive(self):
        try:
            self.connection.cursor()
            return True
        except Exception:
            return False

    def get_info(self, info):
        return self.connection.getinfo(info)

    def __del__(self):
        try:
            if self.committed is None:
                pass
            elif not self.committed:
                self.cursor.rollback()
                log(
                    "DataBase Rollback Performed !\n"
                    "You executed some sql queries but did not committed them !\n"
                    "Try using dbconnector.commit_queries()",
                    "ERROR",
                )
        except Exception:
            pass


def check_db_connector(**kwargs):
    try:
        SQLConnector()
    except InterfaceError as exception:
        handle_exception(exception=exception, **kwargs)
