import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
import ConnectDB


class Check:
    def CheckPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute("select count(1) from dba_pdbs where pdb_name= upper(:pdb)", pdb=pdb_name)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(
                    "select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username=:user and PDB_NAME=:pdb",
                    pdb=self.PDB_NAME, user=self.USERNAME)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckProfile(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(
                    "select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME=:pdb",
                    pdb=self.PDB_NAME)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(
                    "select count(1) from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like '%:user%' and PDB_NAME=':pdb'",
                    pdb=self.PDB_NAME, user=self.USERNAME)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False
