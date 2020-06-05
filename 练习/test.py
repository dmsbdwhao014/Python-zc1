import cx_Oracle
import os

username = 'sys'
syspwd = 'gzNsn789'
dsn = cx_Oracle.makedsn("192.168.10.10", 1521, service_name="zctest")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
with  cx_Oracle.connect(username, syspwd, dsn, mode=cx_Oracle.SYSDBA, encoding="UTF-8") as db_conn:
    db_cursor = db_conn.cursor()
    db_cursor.execute("select count(1) from dba_users")
    db_records = db_cursor.fetchall()
    db_conn.commit()
    print(db_records)
