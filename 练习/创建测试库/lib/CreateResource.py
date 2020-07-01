import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
import ConnectDB


class CreateResource:
    def CreatePDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.cursor() as db_cursor:
                create_sql = """CREATE PLUGGABLE DATABASE {pdb} ADMIN USER admin IDENTIFIED BY {passwd} ROLES=(CONNECT,DBA)
                DEFAULT  TABLESPACE {pdb} DATAFILE '{datafilepath}/{pdb}/{pdb}.dbf'
                SIZE  100M AUTOEXTEND  ON  PATH_PREFIX = '{datafilepath}/{pdb}/'
                FILE_NAME_CONVERT = ('{datafilepath}/pdbseed', '{datafilepath}/{pdb}')""".format(pdb=self.PDB_NAME,
                                                                                                 passwd='"ChangeMe"',
                                                                                                 datafilepath=settings.realfilepath)
                db_cursor.execute(create_sql)
                open_sql = "alter pluggable database {pdb} open".format(pdb=self.PDB_NAME)
                db_cursor.execute(open_sql)
        except cx_Oracle.DatabaseError as e:
            return e

    def CreateProfile(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  ConnectDB.get_cur() as db_cursor:
                db_cursor.execute("alter session set container=;pdb", pdb=self.PDB_NAME)
                db_cursor.execute(
                    "create PROFILE default1 LIMIT FAILED_LOGIN_ATTEMPTS unlimited PASSWORD_LIFE_TIME unlimited PASSWORD_REUSE_TIME unlimited PASSWORD_REUSE_MAX unlimited PASSWORD_VERIFY_FUNCTION default PASSWORD_GRACE_TIME unlimited")
        except cx_Oracle.DatabaseError as e:
            return e

    def CreateTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  ConnectDB.get_cur() as db_cursor:
                tbs = "tbs_{user}".format(user=self.USERNAME)
                db_cursor.execute("alter session set container=;pdb", pdb=self.PDB_NAME)
                sql = "create tablespace {tablespace_name} datafile '/data/oracle/datafile/zctest/{pdb}/{tablespace_name}.dbf' SIZE 100M AUTOEXTEND ON NEXT 1G MAXSIZE 30G".format(
                    tablespace_name=tbs, pdb=self.PDB_NAME)
                db_cursor.execute(settings.enabled_ddl_parallel)
                db_cursor.execute(sql)
        except cx_Oracle.DatabaseError as e:
            return False

    def CreateUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  ConnectDB.get_cur() as db_cursor:
                tbs = "tbs_{user}".format(user=self.USERNAME)
                pwd = "ChangeMe"
                db_cursor.execute("alter session set container=;pdb", pdb=self.PDB_NAME)
                db_cursor.execute(
                    "create user :username default tablespace :tablespace identified by :passwd  PROFILE default",
                    username=self.USERNAME, tablespace=tbs, passwd=pwd)
                db_cursor.execute("grant dba to :username", username=self.USERNAME)
        except cx_Oracle.DatabaseError as e:
            return e
