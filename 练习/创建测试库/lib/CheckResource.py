import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
from lib import ConnectDB


class Check:
    def CheckPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute("select count(1) from dba_pdbs where pdb_name= upper(:pdb)", pdb=pdb_name)
                if db_cursor.fetchall()[0][0]:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        select_sql="select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username=upper('{user}') and PDB_NAME=upper('{pdb}')".format(user=self.USERNAME,pdb=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                if db_cursor.fetchall()[0][0]:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckProfile(self, pdb_name):
        self.PDB_NAME = pdb_name
        select_sql="select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME=upper('{pdb}')".format(pdb=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                if db_cursor.fetchall()[0][0]:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

    def CheckTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        select_sql="select count(1) from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like upper('%{username}%') and PDB_NAME=upper('{pdb}')".format(username=self.USERNAME,pdb=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                if db_cursor.fetchall()[0][0]:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return False

if __name__ == '__main__':
    pdb='test1'
    user='admin3'
    check=Check()
    print(check.CheckUser(pdb,user))