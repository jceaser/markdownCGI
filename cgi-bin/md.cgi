#!/usr/bin/python2.6

################################################################################
# imports

import os
import sys
import cgi
import cgitb
import subprocess
import re

from subprocess import call

################################################################################
# globals

page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>%s</title>
</head>
<body>
%s
</body>
</html>
"""

################################################################################
# functions

def readCgiParam(name, default):
    ret = default
    if (name in os.environ):
        val = os.environ[name]
        if (val!=None):
            ret = val
    return ret

def main():
    root = readCgiParam("DOCUMENT_ROOT", "")
    req_uri = readCgiParam("REQUEST_URI", "/index.md")

    if (req_uri=="/"):
        req_uri = "/index.md"
    req_uri = re.sub("[^a-zA-Z0-9\.\/-]", "_", req_uri)
    file = "%s%s" % (root, req_uri)

    cmd = "cat %s%s | /home/jceaser/bin/markdown" % (root, req_uri)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    cOut = ""
    for line in p.stdout.readlines():
        cOut += line.decode('utf-8')

    print ("Content-type: text/html; charset=utf-8")
    print
    print

    print page % (req_uri, cOut)

################################################################################

main()
