import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
from lib import ConnectDB

class Drop:
    def DropPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        close_sql = """alter pluggable database {pdb} close""".format(pdb=self.PDB_NAME)
        drop_sql = """drop pluggable database {pdb} including datafiles""".format(pdb=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(close_sql)
                db_cursor.execute(drop_sql)
        except cx_Oracle.DatabaseError as e:
            return e

    def DropUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        switch_sql="alter session set container={pdb}".format(pdb=self.PDB_NAME)
        drop_sql="drop user {user} cascade".format(user=self.USERNAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(switch_sql)
                db_cursor.execute(drop_sql)
        except cx_Oracle.DatabaseError as e:
            return e

if __name__ == '__main__':
    pdb='test1'
    user='admin6'
    drop=Drop()
    drop.DropUser(pdb,user)


