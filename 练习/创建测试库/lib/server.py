import cx_Oracle, os,functools

username = 'sys'
syspwd = 'Oracle'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
enabled_ddl_parallel = "alter session force parallel ddl parallel 8"
disabled_ddl_parallel = "alter session disable parallel ddl"
realfilepath="/u01/app/oracle/oradata/zctest"


def Pdbexists(self, pdb_name):
    self.PDB_NAME = pdb_name
    with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
        db_cursor = db_conn.cursor()
        db_cursor.execute("select count(1) from dba_pdbs where pdb_name= :pdb", pdb=self.PDB_NAME)
        db_records = db_cursor.fetchall()[0][0]
        if db_records:
            return True
        else:
            return False


class whatif:
    def decorator(self,func,format1,format2):
        def wrapper(*args, **kwargs):
            ifPDBexists_init = common()
            ifPDBexists = ifPDBexists_init.Pdbexists(*args[0])
            ifProfexists = ifPDBexists_init.Profileexists(*args[0])
            ifUSERexists = ifPDBexists_init.Userexists(*args)
            ifTBSexists= ifPDBexists_init.Tbsexists(*args)
            if format1 == 'create':
                print("开始{} {}操作".format(format1,format2))
                if ifPDBexists:
                    print("The Create Pluggable database already exists")
                else:
                    func(self, *args, **kwargs)
            elif format1 == 'drop':
                print("开始{} {}操作".format(format1,format2))
        return wrapper

    def first(self,format1,format2):
        def foo(func):
            return self.decorator(func, format1,format2)
        return foo


class common:
    def __init__(self):
        self.PDB_NAME = None
        self.USERNAME = None

    def Pdbexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("select count(1) from dba_pdbs where pdb_name= :pdb", pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False

    def Userexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username=:user and PDB_NAME=:pdb",
                pdb=self.PDB_NAME, user=self.USERNAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False

    def Profileexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME=:pdb",
                pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False

    def Tbsexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(
                "select TABLESPACE_NAME from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like '%:user%' and PDB_NAME=':pdb'",
                pdb=self.PDB_NAME, user=self.USERNAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False

    def ListUSER(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("alter session set nls_date_format='yyyy-mm-dd hh24:mi:ss'")
            db_cursor.execute(
                "select PDB_NAME,username,created from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper(':pdb') order by created desc fetch first 5 rows only",
                pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()
            return db_records

    def ListPDB(self):
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("select CON_ID,NAME,OPEN_MODE,RESTRICTED,OPEN_TIME from v$pdbs")
            db_records = db_cursor.fetchall()
            return db_records

class tablespace:
    def __init__(self):
        self.PDB_NAME = None
        self.USERNAME = None


    def CreateTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                db_cursor = db_conn.cursor()
                tbs = "tbs_{user}".format(user=self.USERNAME)
                sql = "create tablespace {tablespace_name} datafile '/data/oracle/datafile/zctest/{pdb}/{tablespace_name}.dbf' SIZE 100M AUTOEXTEND ON NEXT 1G MAXSIZE 30G".format(
                    tablespace_name=tbs, pdb=self.PDB_NAME)
                db_cursor.execute(enabled_ddl_parallel)
                db_cursor.execute(sql)
                db_cursor.execute(disabled_ddl_parallel)
                ifTBSexists = common.Tbsexists(self.PDB_NAME)
                if ifTBSexists:
                    return tbs + "创建成功"
                else:
                    return tbs + "创建失败"
        except Exception as e:
            return e

    def DropTBS(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        # ifPDBexists = common.Pdbexists(self.PDB_NAME)


class PDB:
    def __init__(self):
        self.PDB_NAME = None

    def CreatePDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                db_cursor = db_conn.cursor()
                create_sql = """CREATE PLUGGABLE DATABASE {pdb} ADMIN USER admin IDENTIFIED BY {passwd} ROLES=(CONNECT,DBA)
                DEFAULT  TABLESPACE {pdb} DATAFILE '{datafilepath}/{pdb}/{pdb}.dbf'
                SIZE  100M AUTOEXTEND  ON  PATH_PREFIX = '{datafilepath}/{pdb}/'
                FILE_NAME_CONVERT = ('{datafilepath}/pdbseed', '{datafilepath}/{pdb}')""".format(pdb=self.PDB_NAME,
                                                                                                 passwd='"ChangeMe"',
                                                                                                 datafilepath=realfilepath)
                open_sql = "alter pluggable database {pdb} open".format(pdb=self.PDB_NAME)
                db_cursor.execute(create_sql)
                print("the pluggable database {pdb} create success.".format(self.PDB_NAME))
                db_cursor.execute(open_sql)
                print("open the pluggable database {pdb}.".format(pdb=self.PDB_NAME))
                return True
        except Exception as e:
            return False

    def DropPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                db_cursor = db_conn.cursor()
                close_sql = "alter pluggable database {pdb} close".format(pdb=self.PDB_NAME)
                drop_sql = "drop pluggable database {pdb} including datafiles".format(pdb=self.PDB_NAME)
                db_cursor.execute(close_sql)
                db_cursor.execute(drop_sql)
                return True
        except Exception as e:
            return False

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

    def CreateUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        ifexists = common.Pdbexists(self.PDB_NAME)
        if ifexists:
            ifUserexists = common.Userexists(self.PDB_NAME, self.USERNAME)
            if ifUserexists:
                try:
                    with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                        tbs = "tbs_{user}".format(user=self.USERNAME)
                        pwd = "ChangeMe"
                        db_cursor = db_conn.cursor()
                        db_cursor.execute("alter session set container=;pdb", pdb=self.PDB_NAME)
                        db_cursor.execute(
                            "create user :pdb default tablespace :tablespace identified by :passwd  PROFILE default1",
                            pdb=self.PDB_NAME, tablespace=tbs, passwd=pwd)
                        db_cursor.execute("grant dba to :pdb", pdb=self.PDB_NAME)
                except Exception as e:
                    return e

if __name__ == '__main__':
    tt = "test"
    t1 = PDB()
    t2 = t1.CreatePDB(tt)
    print(t2)
