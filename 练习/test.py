import cx_Oracle
import os

username = 'sys'
syspwd = 'Oracle'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
realfilepath="/u01/app/oracle/oradata/zctest"

def whatif(opertion):
    def decorator(func):
        def wrapper(self,*args, **kwargs):
            ifPDBexists_init=common()
            ifPDBexists = ifPDBexists_init.Pdbexists(*args)
            if opertion == 'create':
                if ifPDBexists:
                    print("The Create Pluggable database already exists")
                else:
                    func(self,*args,**kwargs)
                    print("done.")
            elif opertion == 'drop':
                if ifPDBexists:
                    print("The Create Pluggable database exists")
                    func(self, *args, **kwargs)
                else:
                    print("done.")
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
            db_records = db_cursor.fetchall()
            db_conn.commit()
            return db_records[0][0]

class PDB:
    def __init__(self):
        self.PDB_NAME=None
        print("begin call PDB class.")

    # @whatif
    def CreatePDB(self, pdb_name):
        print("begin call PDB.CreatePDB function.")
        self.PDB_NAME = pdb_name
        try:
            with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                db_cursor = db_conn.cursor()
                create_sql="""CREATE PLUGGABLE DATABASE {pdb} ADMIN USER admin IDENTIFIED BY {passwd} ROLES=(CONNECT,DBA)
                DEFAULT  TABLESPACE {pdb} DATAFILE '{datafilepath}/{pdb}/{pdb}.dbf'
                SIZE  100M AUTOEXTEND  ON  PATH_PREFIX = '{datafilepath}/{pdb}/'
                FILE_NAME_CONVERT = ('{datafilepath}/pdbseed', '{datafilepath}/{pdb}')""".format(pdb=self.PDB_NAME,passwd='"ChangeMe"',datafilepath=realfilepath)
                print(create_sql)
                print("the pluggable database {pdb} create success.".format(self.PDB_NAME))
                open_sql="alter pluggable database {pdb} open".format(pdb=self.PDB_NAME)
                print("open the pluggable database {pdb}.".format(pdb=self.PDB_NAME))
                db_cursor.execute(create_sql)
                db_cursor.execute(open_sql)
        except Exception as e:
            return e

    def DropPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
                db_cursor = db_conn.cursor()
                close_sql="alter pluggable database {pdb} close".format(pdb=self.PDB_NAME)
                drop_sql="drop pluggable database {pdb} including datafiles".format(pdb=self.PDB_NAME)
                db_cursor.execute(close_sql)
                db_cursor.execute(drop_sql)
                return self.PDB_NAME+"已删除"
        except Exception as e:
            return e

if __name__ == '__main__':
    tt="test"
    t1 = PDB()
    t2 = t1.CreatePDB(tt)
    print(t2)