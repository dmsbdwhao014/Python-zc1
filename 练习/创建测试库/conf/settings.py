import os
import cx_Oracle

username = 'sys'
syspwd = 'oracle'
db_name='ORCL'
dsn = cx_Oracle.makedsn("192.168.148.10", 1521, service_name="orcl")
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
enabled_ddl_parallel = "alter session force parallel ddl parallel 8"
disabled_ddl_parallel = "alter session disable parallel ddl"
realfilepath = "/u01/app/oracle/oradata"

