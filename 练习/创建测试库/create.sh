#!/bin/bash
#-------------------------------
#       create_pocdb.sh
#       NAME
#               create_pocdb.sh
#       DESCRIPTION
#               申请创建测试环境
#
#               MODIFIED        (YYYY/MM/DD)
#               zhoucheng       2019/9/23
#
#------------------------------
CreatePDBTBSLOG="/home/oracle/createpocdb/createpdbtablespace.log"
CreatePDBUSERLOG="/home/oracle/createpocdb/createpdbuser.log"
RUNLOG="/home/oracle/createpocdb/runlog.log"
DBALOGIN="sqlplus -S sys/oracle as sysdba"
source ~/.bash_profile

menu()
{
clear
echo "-****************************************************************************************-
1.创建
2.删除
q.退出
-****************************************************************************************-
"
}

Submenu1()
{
echo "-****************************************************************************************-
1.创建PDB
2.创建用户
3.返回上一级
q.退出
-****************************************************************************************-
"
}

Submenu2()
{
echo "-****************************************************************************************-
1.删除PDB
2.删除用户
3.返回上一级
q.退出
-****************************************************************************************-
"
}


CreatePDBTBS()
{
PDB_NAME=$1
USER_NAME=$2
echo  `date +"%F_%T"`  >> $CreatePDBTBSLOG
$DBALOGIN <<ROF >> $CreatePDBTBSLOG
alter session set container=$PDB_NAME;
set serveroutput on line 400 pages 1024
declare
V_PDB VARCHAR2(300) := lower('$PDB_NAME');
V_TABSPACE_NAME VARCHAR2(300) := lower('$USER_NAME');
v_seq_sql varchar2(2000);
begin
v_seq_sql :=' create tablespace tbs_'||V_TABSPACE_NAME||' DATAFILE ''/data/oracle/datafile/noktest/'||V_PDB||'/tbs_'||V_TABSPACE_NAME||'.dbf'' SIZE 100M AUTOEXTEND ON NEXT 1G MAXSIZE 30G';
 EXECUTE IMMEDIATE  v_seq_sql;
end;
/
exit;
ROF
}

CreatePDBUSER()
{
PDB_NAME=$1
USER_NAME=$2
TBSNAME=$3
echo  `date +"%F_%T"`  >> $CreatePDBUSERLOG
$DBALOGIN <<ROF >> $CreatePDBUSERLOG
alter session set container=$PDB_NAME;
create user $USER_NAME default tablespace $TBSNAME identified by "ChangeMe"  PROFILE default1;
grant dba to $USER_NAME;
ROF
}

CreatePROF()
{
PDB_NAME=$1
$DBALOGIN <<EOF
alter session set container=$PDB_NAME;
create PROFILE default1 LIMIT
   FAILED_LOGIN_ATTEMPTS unlimited
   PASSWORD_LIFE_TIME unlimited
   PASSWORD_REUSE_TIME unlimited
   PASSWORD_REUSE_MAX unlimited
   PASSWORD_VERIFY_FUNCTION default
   PASSWORD_GRACE_TIME unlimited;
exit;
EOF
}

ShowPDBS(){
$DBALOGIN <<EOF
SET PAGES 1024 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING on
show pdbs;
exit;
EOF
}

ShowUSERS(){
PDB_NAME=$1
USER_NAME=$2
$DBALOGIN <<EOF
SET line 400 PAGES 1024 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING on
col account_status for a150
select '数据库名:'||PDB_NAME||', 用户名:'||USERNAME||', 密码:ChangeMe, 默认表空间:'||DEFAULT_TABLESPACE AS "account_status" from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper('$PDB_NAME')
and ( '$username' is null or username like upper('%$USER_NAME%')) order by created;
exit;
EOF
}

ListUSERS(){
PDB_NAME=$1
$DBALOGIN <<EOF
SET line 400 PAGES 1024
col username for a20
col PDB_NAME for a20
alter session set nls_date_format='yyyy-mm-dd hh24:mi:ss';
select PDB_NAME,username,created from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where PDB_NAME=upper('$PDB_NAME') order by created desc fetch first 5 rows only;
exit;
EOF
}

ShowConnLink(){
PDB_NAME=$1
USER_NAME=$2
IP=`hostname -i`
Service_name=`lsnrctl status|grep Service|awk -F'"' '{print $2}'|grep -i $PDB_NAME`
echo "##############连接串信息#########"
echo "jdbc:oracle:thin:$USER_NAME/ChangeMe@$IP:1521/$Service_name"
echo "sqlplus $USER_NAME/ChangeMe@$IP:1521/$Service_name"
echo "#################################"
}




IsPDBExists()
{
typeset -u PDB_NAME
PDB_NAME=$1
IfPDBExists=$($DBALOGIN <<EOF
SET PAGES 0 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING OFF
col a for 9
select count(1) a  from dba_pdbs where pdb_name='$PDB_NAME';
exit;
EOF
)
}

IsUSERExists()
{
typeset -u PDB_NAME
typeset -u USER_NAME
PDB_NAME=$1
USER_NAME=$2
IfUSERExists=$($DBALOGIN <<EOF
SET PAGES 0 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING OFF
select count(1) from cdb_users a join dba_pdbs b on a.CON_ID=b.CON_ID where username='$USER_NAME' and PDB_NAME='$PDB_NAME';
exit;
EOF
)
}

IsProfileExists()
{
typeset -u PDB_NAME
PDB_NAME=$1
IfPROFILEExists=$($DBALOGIN <<EOF
SET PAGES 0 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING OFF
select count(1) from cdb_profiles a join dba_pdbs b on a.CON_ID=b.CON_ID where PROFILE='DEFAULT1' and PDB_NAME='$PDB_NAME';
exit;
EOF
)
}

IsTBSExists()
{
typeset -u USER_NAME
typeset -u PDB_NAME
PDB_NAME=$1
USER_NAME=$2
IfTBSExists=$($DBALOGIN <<EOF
SET PAGES 0 FEEDBACK OFF VERIFY Off ECHO OFF timing off HEADING OFF
select TABLESPACE_NAME from cdb_tablespaces a join dba_pdbs b on a.CON_ID=b.CON_ID where TABLESPACE_NAME like '%'||'$USER_NAME'||'%' and PDB_NAME='$PDB_NAME';
exit;
EOF
)
}

CreateDB()
{
typeset -l PDB_NAME
PDB_NAME=$1
$DBALOGIN <<EOF
CREATE PLUGGABLE DATABASE $PDB_NAME ADMIN USER admin IDENTIFIED BY "ChangeMe" ROLES=(CONNECT,DBA)
STORAGE (MAXSIZE UNLIMITED MAX_SHARED_TEMP_SIZE UNLIMITED)
DEFAULT TABLESPACE $PDB_NAME
DATAFILE '/data/oracle/datafile/noktest/$PDB_NAME/$PDB_NAME.dbf' SIZE 100M AUTOEXTEND ON
PATH_PREFIX = '/data/oracle/datafile/noktest/$PDB_NAME/'
FILE_NAME_CONVERT = ('/data/oracle/datafile/noktest/pdbseed', '/data/oracle/datafile/noktest/$PDB_NAME');
alter pluggable database $PDB_NAME open;
exit;
EOF
}

DropDB()
{
PDB_NAME=$1
$DBALOGIN <<EOF
alter pluggable database $PDB_NAME close;
drop pluggable database $PDB_NAME including datafiles;
exit;
EOF
}

DropUSER()
{
PDB_NAME=$1
USER=$2
$DBALOGIN <<EOF
alter session set container=$PDB_NAME;
declare
  i integer;
begin
  i := 1;
  while i=1 loop
  select count(*) into i from dba_users where username='$USER';
  if i = 1 then
   EXECUTE IMMEDIATE  'drop user $USER cascade';
  else
    dbms_output.put_line('用户已删除');
  end if;
  end loop;
end;
/
exit;
EOF
}


Print()
{
MSG=$1
echo "######################################"
echo ""
echo $MSG
echo ""
}

while :
do
menu
read -p "请选择功能:" chooes
if [[ $chooes == "1" ]]; then
        while :
                do
                Submenu1
                read -p "请选择功能:"   subchooes1
                if [[ $subchooes1 == "1" ]]; then
                        ShowPDBS
                        read -p "请输入PDB的名字:"      pdbname
                        if [[ -n $pdbname ]]; then
                                IsPDBExists $pdbname
                                if [[ `echo $IfPDBExists` == "0" ]];then
                                        Print "正在创建 "$pdbname" 数据库"
                                        CreateDB $pdbname
                                        Print $pdbname" 数据库已创建并打开,管理员用户:admin,密码:ChangeMe"
                                else
                                        Print "PDB已存在"
                                fi
                        else
                                Print "请输入pdb名字"
                        fi
                 elif [[ $subchooes1 == "2" ]]; then
                        ShowPDBS
                        read -p "请输入PDB的名字:" pdbname
                        if [[ -n $pdbname ]]; then
                                IsPDBExists $pdbname
                                if [[ `echo $IfPDBExists` == "1" ]];then
                                        read -p "请输入需要创建的用户:" username
                                        if [[ -n $username ]];then
                                                Print "检查用户是否存在"
                                                IsUSERExists $pdbname $username
                                                if [[ `echo $IfUSERExists` == "0" ]];then
                                                        Print "用户不存在，继续创建"
                                                        Print "创建profile,设置账号永不过期"
                                                        IsProfileExists $pdbname
                                                        if [[ `echo $IfPROFILEExists` == "0" ]]; then
                                                                CreatePROF $pdbname
                                                        fi
                                                        Print "创建表空间,用户名前加TBS_"
                                                        CreatePDBTBS $pdbname $username
                                                        IsTBSExists $pdbname $username
                                                        if [[ -n `echo $IfTBSExists` ]];then
                                                                Print "$IfTBSExists 表空间已创建成功"
                                                                Print "开始创建用户"
                                                                CreatePDBUSER $pdbname $username $IfTBSExists
                                                                IsUSERExists $pdbname $username
                                                                if [[ `echo $IfUSERExists` == "1" ]];then
                                                                        ShowUSERS  $pdbname $username
                                                                        ShowConnLink $pdbname $username
                                                                        Print "用户创建成功,初始化密码ChangeMe请修改"
                                                                        echo "按任意键继续"
                                                                        read
                                                                else
                                                                        Print "用户未创建成功"
                                                                fi
                                                        else
                                                                Print "表空间未创建"
                                                        fi
                                                else
                                                        Print "用户已存在"
                                                        ShowUSERS  $pdbname $username
                                                        ShowConnLink $pdbname $username
                                                        Print "用户初始化密码ChangeMe请修改"
                                                        echo "按任意键继续"
                                                fi
                                        else
                                                Print "请输入需要创建的用户"
                                        fi
                                else
                                        Print "PDB未创建,请先创建PDB"
                                fi
                        else
                                Print "请输入PDB的名字:"
                        fi
                elif [[ $subchooes1 == "3" ]]; then
                        break
                elif [[ $subchooes1 == "q" ]] || [[ $subchooes1 == "Q" ]] ; then
                        exit;
                fi
        done
elif [[ $chooes == "2" ]]; then
  while :
        do
        Submenu2
        read -p "请选择功能:" subchooes2
        if [[ $subchooes2 == "1" ]]; then
        ShowPDBS
        read -p "请输入PDB的名字:" pdbname
        if [[ -n $pdbname ]]; then
                IsPDBExists $pdbname
                if [[ `echo $IfPDBExists` == "1" ]];then
                        read -p "请输入DELETE确认删除,删除后不可恢复:" delete_
                        if [[ $delete_ == "DELETE" ]];then
                                Print "开始删除  $pdbname"
                                DropDB $pdbname
                                IsPDBExists $pdbname
                                if [[ `echo $IfPDBExists` == "1" ]];then
                                        Print "删除不成功"
                                else
                                        echo "删除成功"
                                fi
                        else
                                Print "已退出删除"
                        fi
                else
                        Print "$pdbname 不存在"
                fi
        else
                Print "请输入PDB的名字:"
        fi
        elif [[ $subchooes2 == "2" ]]; then
                ShowPDBS
                read -p "请输入PDB的名字:" pdbname
                if [[ -n $pdbname ]]; then
                  IsPDBExists $pdbname
                    if [[ `echo $IfPDBExists` == "1" ]];then
                        ListUSERS $pdbname
                        read -p "请输入用户的名字:" user_
                        read -p "请输入DELETE确认删除,删除后不可恢复:" delete_
                          if [[ $delete_ == "DELETE" ]];then
                            Print "开始删除  $user_"
                            DropUSER $pdbname $user_
                            IsUSERExists $pdbname $user_
                                if [[ `echo $IsUSERExists` == "0" ]]; then
                                        Print "删除不成功"
                                else
                                        Print "删除成功"
                                fi
                          else
                                Print "已退出删除"
                          fi
                  else
                        Print "$pdbname 不存在"
                  fi
                else
                        Print "请输入PDB的名字:"
                fi
        elif [[ $subchooes2 == "3" ]]; then
                break
        elif [[ $subchooes2 == "q" ]] || [[ $subchooes2 == "Q" ]] ; then
                exit;
        fi
        done
elif [[ $chooes == "q" ]]; then
        exit;
fi
done
