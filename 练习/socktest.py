#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from subprocess import Popen, PIPE
import tempfile
import os
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

Host = "192.168.148.10"
User = "oracle"
outputLines = []

sshCommand="ssh -l oracle@192.168.148.10" + " 'ls' "

tmpBannerFile = ""
tmpBannerFd = None
tmpBannerFd, tmpBannerFile = tempfile.mkstemp(suffix="_"+ Host, prefix="banner_")
print("tmpBannerFile:",tmpBannerFile,",tmpBannerFd:" ,tmpBannerFd)
tmpFd = os.fdopen(tmpBannerFd, "r+")
sshCommand += " 2>"+ tmpBannerFile
print(sshCommand)
child = Popen( sshCommand, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
if child.stderr:
    err = child.stderr
    out = err.readlines()
    print(bytes(out[0]).decode("gb2312"))
    err.close()
else:
    r = child.stdout
    out = r.readlines()
    print(bytes(out[0]).decode("gb2312"))
    r.close()
w = child.stdin
w.close()

