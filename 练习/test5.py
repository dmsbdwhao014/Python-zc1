import datetime
import threading
import os
import sys
import tempfile
import argparse
import paramiko
import stat
import socket
import signal
import glob
import time
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException


class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


class UsageError(Exception):
    def __init__(self, msg):
        self.msg = msg

def CopyAndExecute(host, copyfile, destdir, args):
    root = args.root
    rootpassword = args.rootpassword
    if copyfile and os.path.exists(copyfile):
        destfile = os.path.join(destdir, os.path.basename(copyfile.strip()))
    user = args.userid
    password = args.password
    verbose = args.verbosity
    init = args.init
    clientfile = args.clientfile
    install = args.install
    updateLock = threading.Lock()

    class sshCmd(threading.Thread):
        def __init__(self,ip):
            threading.Thread.__init__(self)
            self.IP = ip
            self.child = None
            try:
                if user and password:
                    self.T = paramiko.Transport((self.IP, 22))
                    self.T.connect(username=user, password=password)
                    self.userSsh = paramiko.SSHClient()
                    self.userSsh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    self.userSsh._transport = self.T
                if root and rootpassword:
                    self.T1 = paramiko.Transport((self.IP, 22))
                    self.T1.connect(username=root, password=rootpassword)
                    self.rootSsh = paramiko.SSHClient()
                    self.rootSsh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    self.rootSsh._transport = self.T1
                if init and (copyfile and destfile):
                    self.Sftp = paramiko.SFTPClient.from_transport(self.T)
            except AuthenticationException as e:
                print("[{}]:错误:认证失败,请检查{}的账号密码".format(datetime.datetime.now(), self.IP))
                os._exit(1)
            except NoValidConnectionsError:
                print('[{}]:错误:连接{}出现了问题'.format(datetime.datetime.now(), self.IP))
                os._exit(1)
            except Exception as e:
                print('[{}]:错误:其他错误问题{}'.format(datetime.datetime.now(), e))
                os._exit(1)

        def ThreadExecute(self):
            AddGroup = r'if [ `cat /etc/group|grep oinstall|wc -l` -eq 0 ]; then groupadd oinstall;fi'
            AddUser = r'if [ `cat /etc/passwd|grep oracle|wc -l` -eq 0  ];then useradd -g oinstall oracle;echo "Nsnoracle@jm20170408" | passwd --stdin oracle;fi'
            Modify_Global_Profile = r'if [ `cat /etc/profile|grep ORACLE_HOME|wc -l` -eq 0  ];then echo -e "export ORACLE_HOME={destfile1}/oracle/product/12.2.0/client_1/ \nexport PATH=$ORACLE_HOME/bin:$PATH\nexport LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH" >> /etc/profile '.format(
                destfile1=destfile)
            Modify_User_Profile = r'if [ `cat ~/.bash_profile|grep ORACLE_HOME|wc -l` -eq 0  ];then echo -e "export ORACLE_HOME={destfile1}/oracle/product/12.2.0/client_1/ \nexport PATH=$ORACLE_HOME/bin:$PATH\nexport LD_LIBRARY_PATH=$ORACLE_HOME/lib:$LD_LIBRARY_PATH" >> ~/.bash_profile '.format(
                destfile1=destfile)
            Check_Hosts = r'if [ `cat /etc/hosts |grep $HOSTNAME|wc -l` -eq 0 ];then echo {ip}  `hostname` >> /etc/hosts ;fi'.format(
                ip = self.IP)
            Uncompress_Tar = r'if [ `ls {file}|wc -l` -eq 1 ];then tar -xf {file} -C {dest1};done'.format(file=destfile,dest1=destdir)

            if install:
                if init and root == 'root' and rootpassword:
                    self.execute_shell(AddGroup + ";" + AddUser + ";" + Modify_Global_Profile + ";" + Check_Hosts,root)
                else:
                    if root == 'root' and rootpassword:
                        self.execute_shell(Modify_Global_Profile + ";" + Check_Hosts,root)
                self.execute_shell(Modify_User_Profile,user)
                if clientfile:
                    self.CopyFile(copyfile,destfile)
                self.execute_shell(Uncompress_Tar, user)
            updateLock.acquire()
            updateLock.release()

        def execute_shell(self, cmd,mode):
            try:
                if verbose:
                    print("[{}]:...entering thread for {}:".format(datetime.datetime.now(), self.IP))
                    print("command:", cmd)
                if mode == 'root':
                    stdin, stdout, stderr = self.rootSsh.exec_command(cmd)
                    print(stdout.read().decode('utf-8'))
                    Err_List = stderr.readlines()
                    if len(Err_List) > 0:
                        print('[%s]:错误: %s' % ((datetime.datetime.now(), Err_List[0])))
                        os._exit(1)
                else:
                    stdin, stdout, stderr = self.userSsh.exec_command(cmd)
                    print(stdout.read().decode('utf-8'))
                    Err_List = stderr.readlines()
                    if len(Err_List) > 0:
                        print('[%s]:错误: %s' % ((datetime.datetime.now(), Err_List[0])))
                        os._exit(1)
                if verbose:
                    print('[%s]:运行完毕' % datetime.datetime.now())
            except Exception as e:
                print("[%s]:错误:%s运行失败,失败原因%s" % (datetime.datetime.now(), cmd, e))

        def CopyFile(self,copyfile,destfile):
            try:
                if verbose:
                    print("local_path:", copyfile, " remote_path:", destfile)
                self.Sftp.put(copyfile, destfile)
                self.T.close()
            except Exception as e:
                raise UsageError('[{}]:错误: {}'.format(datetime.datetime.now(), e))

    output = {}
    status = {}
    waitList = []
    file = init or copyfile
    try:
        if file:
            for ipaddr in host:
                ThreadWork = sshCmd(ipaddr)
                ThreadWork.start()
                waitList.append(ThreadWork)

            for thread in waitList:
                while thread.isAlive():
                    thread.join(1)

    except KeyboardInterrupt as e:
        print("Keyboard interrupt")
        for thread in waitList:
            if thread.isAlive() and thread.child:
                try:
                    print
                    "killing child pid %d..." % thread.child.pid
                    os.kill(thread.child.pid, signal.SIGTERM)
                    t = 2.0  # max wait time in secs
                    while thread.child.poll() < 0:
                        if t > 0.4:
                            t -= 0.20
                            time.sleep(0.20)
                        else:  # still there, force kill
                            os.kill(thread.child.pid, signal.SIGKILL)
                            time.sleep(0.4)
                            thread.child.poll()  # final try
                            break
                except OSError as e:
                    if e.errno != 3:
                        raise
        raise KeyboardInterrupt
    return status, output

ssh = sshCmd('192.168.148.10', 'root', 'oracle', 5, Scopy=True)
# ssh.put_file(r'C:\Users\cheng\Oracle\oradiag_cheng\diag\clients\user_cheng\host_4011349183_82\alert\log.xml','/app/bighead/oracle/log.xml')
# ssh.execute_shell('ls')
