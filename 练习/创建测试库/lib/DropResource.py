import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
import ConnectDB


class DropResource:
    def DropPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.get_cur() as db_cursor:
                close_sql = """alter pluggable database {pdb} close""".format(pdb=self.PDB_NAME)
                drop_sql = """drop pluggable database {pdb} including datafiles""".format(pdb=self.PDB_NAME)
                db_cursor.execute(close_sql)
                db_cursor.execute(drop_sql)
        except cx_Oracle.DatabaseError as e:
            return e

    def DropUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  ConnectDB.get_cur() as db_cursor:
                db_cursor.execute("alter session set container=;pdb", pdb=self.PDB_NAME)
                db_cursor.execute("drop user {user} cascade", user=self.USERNAME)
        except cx_Oracle.DatabaseError as e:
            return e
