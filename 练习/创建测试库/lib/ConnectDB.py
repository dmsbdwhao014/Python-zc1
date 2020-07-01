import os
import cx_Oracle
import sys

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings


class connect:
    def get_connect(self):
        try:
            self.connect = cx_Oracle.connect(settings.username, settings.syspwd, settings.dsn, mode=cx_Oracle.SYSDBA)
        except  cx_Oracle.DatabaseError as e:
            return e

    def get_cur(self):
        return self.connect.cursor()


def get_connect():
    db = connect()
    db.get_connect()
    return db.get_cur()
