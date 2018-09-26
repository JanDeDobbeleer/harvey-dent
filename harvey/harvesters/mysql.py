from pymysql import Connect
from pymysql.cursors import Cursor
from typing import Dict, Any, Type
from typing_extensions import Protocol
from .base.multipointsbase import MultiPointsBase


class DatabaseConnection(Protocol):

    def close(self) -> None:
        ...  # Use a literal '...' here

    def cursor(self, cursor: Type[Cursor] = None) -> Any:
        ...


class MySql(MultiPointsBase):

    def __init__(self, settings: Dict, config: Dict) -> None:
        super().__init__(settings=settings, config=config)

    def get_description(self) -> str:
        return 'Running MYSQL data fetching'

    def _get_connection(self) -> DatabaseConnection:
        return Connect(host=self.config['mysql_host'],
                       user=self.config['mysql_user'],
                       passwd=self.config['mysql_password'],
                       db=self.config['mysql_database'])

    def get_data(self, key_value: str) -> Dict:
        db = self._get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM YOUR_TABLE_NAME")
        for row in cur.fetchall():
            print(row[0])
        db.close() # noqa
        app_details = dict()
        app_details["test"] = ""
        return app_details
