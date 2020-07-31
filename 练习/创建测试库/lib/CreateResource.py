import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
from lib import ConnectDB

class Create:
    def CreatePDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        create_sql = """CREATE PLUGGABLE DATABASE {pdb} ADMIN USER admin IDENTIFIED BY {passwd} ROLES=(CONNECT,DBA)
                        DEFAULT  TABLESPACE {pdb} DATAFILE '{datafilepath}/{dbname}/{pdb}/{pdb}.dbf'
                        SIZE  100M AUTOEXTEND  ON  PATH_PREFIX = '{datafilepath}/{pdb}/'
                        FILE_NAME_CONVERT = ('{datafilepath}/{dbname}/pdbseed', '{datafilepath}/{dbname}/{pdb}')""".format(
            pdb=self.PDB_NAME,
            passwd='"ChangeMe"',
            datafilepath=settings.realfilepath,dbname=settings.db_name
            )
        open_sql = "alter pluggable database {pdb} open".format(pdb=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(create_sql)
                db_cursor.execute(open_sql)
                return True
        except cx_Oracle.DatabaseError as e:
            return e

    def CreateProfile(self, pdb_name):
        self.PDB_NAME = pdb_name
        switch_sql="alter session set container={pdb}".format(pdb=self.PDB_NAME)
        create_sql="create PROFILE default1 LIMIT FAILED_LOGIN_ATTEMPTS unlimited PASSWORD_LIFE_TIME unlimited PASSWORD_REUSE_TIME unlimited PASSWORD_REUSE_MAX unlimited PASSWORD_VERIFY_FUNCTION default PASSWORD_GRACE_TIME unlimited"
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(switch_sql)
                db_cursor.execute(create_sql)
                return True
        except cx_Oracle.DatabaseError as e:
            return e

    def CreateTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        tbs = "tbs_{user}".format(user=self.USERNAME)
        switch_sql="alter session set container={pdb}".format(pdb=self.PDB_NAME)
        create_sql = "create tablespace {tablespace_name} datafile '{datafilepath}/{dbname}/{pdb}/{tablespace_name}.dbf' SIZE 100M AUTOEXTEND ON NEXT 1G MAXSIZE 30G".format(
            tablespace_name=tbs, pdb=self.PDB_NAME,datafilepath=settings.realfilepath,dbname=settings.db_name)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(switch_sql)
                db_cursor.execute(settings.enabled_ddl_parallel)
                db_cursor.execute(create_sql)
                return tbs
        except cx_Oracle.DatabaseError as e:
            return e

    def CreateUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        self.tbs = "tbs_{user}".format(user=self.USERNAME)
        self.pwd = "ChangeMe"
        switch_sql="alter session set container={pdb}".format(pdb=self.PDB_NAME)
        create_sql="create user {username} default tablespace {tablespace} identified by {passwd}  PROFILE default".format(username=self.USERNAME,tablespace=self.tbs,passwd=self.pwd)
        grant_sql="grant dba to {username}".format(username=self.USERNAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(switch_sql)
                db_cursor.execute(settings.enabled_ddl_parallel)
                db_cursor.execute(create_sql)
                db_cursor.execute(grant_sql)
                return True
        except cx_Oracle.DatabaseError as e:
            return e
