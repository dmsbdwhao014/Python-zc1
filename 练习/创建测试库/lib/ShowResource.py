import os, sys, cx_Oracle

sys.path.insert(1, os.path.dirname((os.path.dirname(__file__))))
from conf import settings
from lib import ConnectDB
from lib import GetIP

class Show:
    def ShowUser(self, pdb_name, user_name):
        self.PDB_NAME = pdb_name
        self.USERNAME = user_name
        select_sql = """select PDB_NAME,USERNAME,DEFAULT_TABLESPACE from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper('{PDB_NAME}') and ( '{USER_NAME}' is null or username like upper('%{USER_NAME}%')) order by created""".format(
            PDB_NAME=self.PDB_NAME, USER_NAME=self.USERNAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                db_records=db_cursor.fetchall()
                print('用户信息'.center(40,'#'))
                for pdb,user,tbs in db_records:
                    print("数据库名: ",pdb_name,",用户名:",user,",默认密码:ChangeMe,默认表空间:",tbs)
                print(''.center(44, '#'))
        except cx_Oracle.DatabaseError as e:
            return e

    def ShowPDB(self):
        select_sql = "select  NAME, OPEN_MODE from V$PDBS order by CON_ID"
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                db_records = db_cursor.fetchall()
                print('数据库列表'.center(40, '#'))
                for name, mode in db_records:
                    print("数据库名:", name, " 打开模式:", mode)
                print(''.center(45, '#'))
        except cx_Oracle.DatabaseError as e:
            return e

    def ShowCONN(self,pdb_name,username):
        self.PDB_NAME=pdb_name
        self.USERNAME=username
        print('连接串信息'.center(40, '#'))
        print('jdbc:oracle:thin:{user}/ChangeMe@{IP}:1521/{pdb}'.format(user=self.USERNAME, IP=GetIP.get_host_ip(),
                                                                        pdb=self.PDB_NAME))
        print('sqlplus {user}/ChangeMe@{IP}:1521/{pdb}'.format(user=self.USERNAME, IP=GetIP.get_host_ip(),
                                                                        pdb=self.PDB_NAME))
        print(''.center(45, '#'))

    def ListUser(self,pdb_name):
        self.PDB_NAME=pdb_name
        select_sql="select USERNAME,created,profile from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper('{PDB_NAME}') order by created desc fetch first 10 rows only".format(PDB_NAME=self.PDB_NAME)
        try:
            with  ConnectDB.get_connect() as db_cursor:
                db_cursor.execute(select_sql)
                db_records = db_cursor.fetchall()
                print('用户列表'.center(40, '#'))
                for user,ctd,profile in db_records:
                    print('用户:',user,",创建时间:,",ctd,",概要文件:",profile)
                print(''.center(44, '#'))
        except cx_Oracle.DatabaseError as e:
            return e