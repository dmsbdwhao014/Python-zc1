import cx_Oracle, os, functools

username = 'sys'
syspwd = 'Oracle'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
enabled_ddl_parallel = "alter session force parallel ddl parallel 8"
disabled_ddl_parallel = "alter session disable parallel ddl"
realfilepath = "/u01/app/oracle/oradata/zctest"
db_connect = cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA)


class Check:
    def CheckPDB(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  db_connect.cursor() as db_cursor:
                db_cursor.execute("select count(1) from dba_pdbs where pdb_name= upper(:pdb)", pdb=pdb_name)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return e

    def Userexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        try:
            with  db_connect.cursor() as db_cursor:
                db_cursor.execute(
                    "select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username=:user and PDB_NAME=:pdb",
                    pdb=self.PDB_NAME, user=self.USERNAME)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return e

    def Profileexists(self, pdb_name):
        self.PDB_NAME = pdb_name
        try:
            with  db_connect.cursor() as db_cursor:
                db_cursor.execute(
                    "select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME=:pdb",
                    pdb=self.PDB_NAME)
                db_records = db_cursor.fetchall()[0][0]
                if db_records:
                    return True
                else:
                    return False
        except cx_Oracle.DatabaseError as e:
            return e

    def Tbsexists(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        with   db_connect.cursor() as db_cursor:
            db_cursor.execute(
                "select TABLESPACE_NAME from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like '%:user%' and PDB_NAME=':pdb'",
                pdb=self.PDB_NAME, user=self.USERNAME)
            db_records = db_cursor.fetchall()[0][0]
            if db_records:
                return True
            else:
                return False



if __name__ == '__main__':
    pdb = "test1"
    users = "admin1"
    t1 = Check()
    t2 = t1.CheckPDB(pdb)
    print(t2)
