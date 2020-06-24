import cx_Oracle
import os

username = 'sys'
syspwd = 'Oracle'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
realfilepath = "/u01/app/oracle/oradata/zctest"


def whatif(opertion):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            ifPDBexists_init = common()
            ifPDBexists = ifPDBexists_init.Pdbexists(*args)
            if opertion == 'create':
                if ifPDBexists:
                    print("The Create Pluggable database already exists")
                else:
                    func(self, *args, **kwargs)
                    print("create done.")
            elif opertion == 'drop':
                if ifPDBexists:
                    func(self, *args, **kwargs)
                    print("drop done.")
                else:
                    print("The Pluggable database not exists")
        return wrapper
    return decorator


class common:
    def __init__(self):
        self.PDB_NAME = None
        self.USERNAME = None

    def Pdbexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute("select count(1) from dba_pdbs where pdb_name= upper(:pdb)", pdb=self.PDB_NAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False


class PDB:
    def __init__(self):
        self.PDB_NAME = None

    @whatif(opertion='create')
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

    @whatif(opertion='drop')
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


if __name__ == '__main__':
    tt = "test1"
    t1 = common()
    t2 = t1.Pdbexists(tt)
    print(t2)

