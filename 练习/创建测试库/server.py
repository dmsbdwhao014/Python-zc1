import cx_Oracle, os

username = 'sys'
syspwd = 'gzNsn789'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
enabled_ddl_parallel="alter session force parallel ddl parallel 8"
disabled_ddl_parallel="alter session disable parallel ddl"

class common:
    def __init__(self):
        self.PDB_NAME = None
        self.USERNAME = None

    def Pdbexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("select count(1) from dba_pdbs where pdb_name= :pdb", pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

    def Userexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username=:user and PDB_NAME=:pdb",
                pdb=self.PDB_NAME, user=self.USERNAME)
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

    def Profileexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME=:pdb",
                pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

    def Tbsexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select TABLESPACE_NAME from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like '%:user%' and PDB_NAME=':pdb'",
                pdb=self.PDB_NAME, user=self.USERNAME)
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

    def ListUSER(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("alter session set nls_date_format='yyyy-mm-dd hh24:mi:ss'")
            db_cursor.execute(
                "select PDB_NAME,username,created from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper(':pdb') order by created desc fetch first 5 rows only",
                pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

    def ListPDB(self):
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("show pdbs")
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records

class tablespace:

    def __init__(self):
        self.PDB_NAME=None
        self.USERNAME=None

    def CreateTBS(self,pdb_name,user_name):
        self.PDB_NAME=pdb_name
        self.USERNAME=user_name
        ifPDBexists = common.Pdbexists(self.PDB_NAME)
        if ifPDBexists:
                try:
                    with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                        db_cursor = db_conn.cursor()
                        tbs="tbs_{user}".format(user=self.USERNAME)
                        sql = "create tablespace {tablespace_name} datafile '/data/oracle/datafile/zctest/{pdb}/{tablespace_name}.dbf' SIZE 100M AUTOEXTEND ON NEXT 1G MAXSIZE 30G".format(tablespace_name=tbs,pdb=self.PDB_NAME)
                        db_cursor.execute(enabled_ddl_parallel)
                        db_cursor.execute(sql)
                        db_cursor.execute(disabled_ddl_parallel)
                        db_cursor.colse()
                        db_conn.colse()
                        ifTBSexists = common.Tbsexists(self.PDB_NAME)
                        if ifTBSexists:
                            return tbs+"创建成功"
                        else:
                            return tbs+"创建失败"
                except Exception as e:
                    return e
        else:
            return self.PDB_NAME + "不存在"

    def DropTBS(self,pdb_name,user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        ifPDBexists = common.Pdbexists(self.PDB_NAME)




class PDB:
    def __init__(self):
        self.PDB_NAME = None

    def CreatePDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        ifPDBexists = common.Pdbexists(self.PDB_NAME)
        if ifPDBexists:
            return self.PDB_NAME + "已存在"
        else:
            try:
                with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                    db_cursor = db_conn.cursor()
                    db_cursor.execute(enabled_ddl_parallel)
                    db_cursor.execute(
                        """CREATE PLUGGABLE DATABASE $PDB_NAME ADMIN USER admin IDENTIFIED BY :passwd ROLES=(CONNECT,DBA)
                    DEFAULT  TABLESPACE $PDB_NAME DATAFILE '/data/oracle/datafile/zctest/:pdb/:pdb.dbf'
                    SIZE  100M AUTOEXTEND  ON  PATH_PREFIX = '/data/oracle/datafile/zctest/:pdb/'
                    FILE_NAME_CONVERT = ('/data/oracle/datafile/zctest/pdbseed', '/data/oracle/datafile/zctest/:pdb')""",
                        passwd="ChangeMe", pdb=self.PDB_NAME)
                    db_cursor.execute(disabled_ddl_parallel)
                    db_cursor.execute("alter pluggable database :pdb open", pdb=self.PDB_NAME)
                    db_cursor.colse()
                    db_conn.colse()
            except Exception as e:
                return e

    def DropPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        ifPDBexists = common.Pdbexists(self.PDB_NAME)
        if ifPDBexists:
            try:
                with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                    db_cursor = db_conn.cursor()
                    db_cursor.execute("alter pluggable database :pdb close", pdb=self.PDB_NAME)
                    db_cursor.execute("drop pluggable database :pdb including datafiles", pdb=self.PDB_NAME)
                    db_cursor.colse()
                    db_conn.colse()
            except Exception as e:
                return e
        else:
            return self.PDB_NAME + "不存在"


class USER:
    def __init__(self):
        self.PDB_NAME = None
        self.USERNAME = None

    def ShowUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        ifPDBexists = common.Pdbexists(self.PDB_NAME)
        if ifPDBexists:
            ifUserexists = common.Userexists(self.PDB_NAME, self.USERNAME)
            if ifUserexists:
                try:
                    with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                        db_cursor = db_conn.cursor()
                        db_cursor.execute(
                            "select '数据库名:'||PDB_NAME||', 用户名:'||USERNAME||', 密码:ChangeMe, 默认表空间:'||DEFAULT_TABLESPACE  from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper(':pdb') and  username like upper('%:user%') ",
                            pdb=self.PDB_NAME, user=self.USERNAME)
                        db_records = db_cursor.fetchall()
                        db_cursor.colse()
                        db_conn.colse()
                        return db_records
                except Exception as e:
                    return e
            else:
                return self.USERNAME + "不存在"
        else:
            return self.PDB_NAME + "不存在"

    def CreateUser(self,pdb_name,user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        ifexists = common.Pdbexists(self.PDB_NAME)
        if ifexists:
            ifUserexists = common.Userexists(self.PDB_NAME, self.USERNAME)
            if ifUserexists:
                try:
                    with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                        db_cursor = db_conn.cursor()
                        db_cursor.execute("alter session set container=;pdb",pdb=self.PDB_NAME)
