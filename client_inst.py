# encoding=utf-8

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

# version
version = "1"
# default assignment for SSH port
PORT = 22
TIMEOUT = 1.0
TESTMODE = ''


# Error class used to handle environment errors (e.g. file not found)
class Error(Exception):
    def __init__(self, msg):
        self.msg = msg


class UsageError(Exception):
    def __init__(self, msg):
        self.msg = msg


def buildIPList(iplist, filename, verbose):
    """
    Build a list of unique cells which will be contacted by dcli.

    Takes a list of cells and a filename.
    The file is read, and each non-empty line that does not start with #
    is assumed to be a cell.
    Unique cells are added to a list.
    Returns the list of unique cells.
    """
    iplist1 = []
    if filename:
        filename = filename.strip()
        try:
            with open(filename) as fd:
                lines = fd.readlines()
                for line in lines:
                    line = line.strip()
                    if len(line) > 0 and not line.startswith("#"):
                        iplist1.append(line)
        except IOError as strerror:
            raise Error("I/O error(%s) on %s: %s".format(filename, strerror))

    if iplist:
        for ipline in iplist:
            iplist1.append(ipline.strip())

    uniqueIPList = []
    for c in iplist1:
        if c not in uniqueIPList:
            uniqueIPList.append(c)
    return uniqueIPList


def findFiles(path):
    '''Return list of files matching pattern in path.'''

    list = []
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    list = glob.glob(path)

    return list

def checkFile(filepath, isExec, verbose):
    """
    Test for existence and permissions of files to be copied or executed remotely.

    The file is tested for read and execute permissions.
    """
    files = findFiles(filepath)

    if not files:
        raise Error("File does not exist: %s" % filepath)
    else:
        for file in files:
            if not os.path.exists(file):
                raise Error("File does not exist: %s" % file)
            if isExec:
                if not os.path.isfile(file):
                    raise Error("Exec file is not a regular file: %s" % file)
            elif not os.path.isfile(file) and not os.path.isdir(file):
                raise Error("File is not a regular file or directory: %s" % file)
            st = os.stat(file)
            mode = st[stat.ST_MODE]
            if isExec and os.name == "posix" and not (mode & stat.S_IEXEC):  # same as stat.S_IXUSR
                raise Error("Exec file does not have owner execute permissions")

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
    testmode=args.TESTMODE
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
                if testmode:
                    print("test mode")
                    print("command:", cmd)
                else:
                    if mode == 'root':
                        stdin, stdout, stderr = self.rootSsh.exec_command(cmd)
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
                if testmode:
                    print("copy test")
                else:
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
                    print("killing child pid %d..." % thread.child.pid)
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

def testIPs(ipaddress, ipfile, verbose):
    """
    Test cells for their ability to talk on their SSH port 22

    Builds a list of cells that can connect (good list)
    and a list of bad ips
    """
    good = []
    bad = []
    if not ipfile:
        ipfile = ipaddress
    for ip in ipfile:
        try:
            res = socket.getaddrinfo(ip, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM)
            sockaddr = 0
            for addr in res:
                if addr[0] == socket.AF_INET:
                    sockaddr = addr[-1]
                    break

            if not sockaddr:
                bad.append(ip)
                continue

            ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ts.settimeout(TIMEOUT)

            if not TESTMODE:
                ts.connect(sockaddr)
            good.append(ip)
        except socket.error as e:
            if verbose:
                print("socket error: %s" % e)
            bad.append(ip)
        except socket.timeout as e:
            if verbose:
                print("socket timeout: %s" % e)
            bad.append(ip)
    return good, bad

def main(argv=None):
    parser = argparse.ArgumentParser(description='安装Oracle客户端脚本')
    parser.add_argument('-V', '--version', help="版本信息", action='version', version=version)
    parser.add_argument("-i", '--ip', help="需要安装客户端的IP地址", nargs='*', metavar="ip", dest="ipaddress")
    parser.add_argument("-g", "--group", help="包含IP列表的文件", action="store", metavar="file", type=str, dest="ipfile")
    parser.add_argument("-u", "--user", default="oracle", help="登陆到远程使用的用户", metavar="user", action="store",dest="user")
    parser.add_argument('-p', '--password', action="store", help='登陆远程的用户密码', metavar="passwd", dest='password')
    parser.add_argument("-v", "--verbose", action="count", dest="verbosity")
    parser.add_argument('-I', "--install", action="store_true", help="执行安装", dest="install")
    parser.add_argument('-f', '--file', action="store", default='/home/oracle/oracle.tar.gz', help='客户端文件位置',
                        metavar="file", dest='clientfile')
    parser.add_argument('-df', '--destfile', action="store", default='/app/bighead', help='远程客户端文件位置',
                        metavar="file", dest='destfile')
    parser.add_argument('--init', action="store_true", help="是否初始化安装", dest="init")
    parser.add_argument("--root", help="初始化必须使用root用户", action="store",dest="root")
    parser.add_argument("--rootpassword", help="root用户的密码", action="store",dest="rootpassword")
    parser.add_argument("-T", help="测试模式", action="store_true",dest="TESTMODE")


    parser.parse_intermixed_args()
    args = parser.parse_args()
    print("args: ", args)

    if args.verbosity:
        print("argv: %s" % argv)
    returnValue = 0

    try:
        if args.init and not (args.root and args.rootpassword):
            raise UsageError('Initial installation requires root account.')

        if not args.install and not (args.ipaddress or args.ipfile) and not args.password and not args.user :
            raise UsageError("No command specified.")

        if args.install and not ((args.password and args.user) or (args.root and args.rootpassword)):
            raise UsageError("Must specify both user or superuser.")

        if args.ipaddress and args.ipfile:
            raise UsageError("Cannot specify both ip and ipfile")

        if args.ipfile:
            checkFile(args.ipfile, False, args.verbosity)

        if args.ipaddress or args.ipfile:
            iplist = buildIPList(args.ipaddress, args.ipfile, args.verbosity)
            if len(iplist) == 0:
                raise UsageError("No ipaddress specified.")

            goodIPs, badIPs = testIPs(args.ipaddress, args.ipfile, args.verbosity)
            if args.verbosity:
                print("iplist: ",iplist,", goodIPs: ",goodIPs,", badIPs: ",badIPs)

            if args.verbosity and len(goodIPs) > 0:
                print("Success connecting to cells: %s" % goodIPs)

            if len(badIPs) == len(args.ipaddress):
                print("All ip failed to connect.Please enter the correct ip address and try again")
                os._exit(1)

            if len(badIPs) > 0:
                print("Unable to connect to cells: %s" % badIPs)


        if len(goodIPs) > 0:
            batchBegin = 0
            loopCount = 0
            batchEnd = len(goodIPs)
            cells = goodIPs[batchBegin:batchEnd]
            while True:
                if len(cells) > loopCount:
                    threads = []
                    if args.verbosity:
                        print("程序开始运行%s" % datetime.datetime.now())
                    # 每一台服务器创建一个线程处理
                    for server in cells:
                        th = threading.Thread(target=sshCmd, args=(server,args.userid,args.password))
                        th.start()
                        threads.append(th)
                    # 等待线程运行完毕
                    for th in threads:
                        th.join()
                    if args.verbosity:
                        print("程序结束运行%s" % datetime.datetime.now())



    except UsageError as err:
        print(sys.stderr, "Error: %s" % err.msg)
        parser.print_help()
        # parser.error(err.msg) -- doesn't print usage options.
        return 2

    except Error as err:
        print(sys.stderr, "Error: %s" % err.msg)
        return 2

    except IOError as err:
        print(sys.stderr, "IOError: [Errno %s] %s" % (err.errno, err.strerror))
        return 2

    except KeyboardInterrupt:
        # sys.exit(1)  does not work after ctrl-c
        os._exit(1)

    # return 1 for any other error
    return returnValue and 1


if __name__ == "__main__":
    sys.exit(main())
