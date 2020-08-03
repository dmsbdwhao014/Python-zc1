
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
import glob

# version
version = "1"
# default assignment for SSH port
PORT = 22
# timeout used to check aliveness of hosts
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
    parser.add_argument("-l", "--user", default="oracle", help="登陆到远程使用的用户", metavar="user", action="store",
                        dest="userid")
    parser.add_argument('-p', '--password', action="store", help='登陆远程的用户密码', metavar="passwd", dest='password')
    parser.add_argument("-v", "--verbose", action="count", dest="verbosity")
    parser.add_argument('-I', "--install", action="store_true", help="执行安装", dest="install")
    parser.add_argument('-f', '--file', action="store", default='/home/oracle/oracle.tar.gz', help='客户端文件位置',
                        metavar="file", dest='clientfile')
    parser.parse_intermixed_args()
    args = parser.parse_args()
    print("args: ", args)

    if args.verbosity:
        print("argv: %s" % argv)
    returnValue = 0

    try:
        if not args.install and not (args.ipaddress or args.ipfile or args.password):
            raise UsageError("No command specified.")

        if args.ipaddress and args.ipfile:
            raise UsageError("Cannot specify both ip and ipfile")

        if args.ipfile:
            checkFile(args.ipfile, False, args.verbosity)

        if args.ipaddress or args.ipfile:

            iplist = buildIPList(args.ipaddress, args.ipfile, args.verbosity)
            if len(iplist) == 0:
                raise UsageError("No cells specified.")

            goodIPs, badIPs = testIPs(args.ipaddress, args.ipfile, args.verbosity)
            print("iplist: ",iplist,", goodIPs: ",goodIPs,", badIPs: ",badIPs)

            if args.verbosity and len(goodIPs) > 0:
                print("Success connecting to cells: %s" % goodIPs)

            if len(badIPs) == len(args.ipaddress):
                print("All ip failed to connect.Please enter the correct ip address and try again")
                os._exit(1)

            if len(badIPs) > 0:
                print("Unable to connect to cells: %s" % badIPs)

        #
        # if len(goodIPs) > 0:
        #     sampleCount = 1
        #     loopCount = 0
        #     while True:


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
