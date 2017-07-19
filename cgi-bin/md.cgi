#!/usr/bin/python2.6

################################################################################
# imports

import os
import sys
import cgi
import cgitb
import subprocess
import re
import os.path

from subprocess import call

################################################################################
# globals

page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>%s</title>
    <link rel="stylesheet" type="text/css" href="/css/markdown.css">
    <link rel="stylesheet" type="text/css" href="%s.css">
</head>
<body>
<header>
    <div id="logo" style="&#x0f4f;"></div>
    <div id="title"></div>
    <div id="title_caption"></div>
</header>
%s
<footer>
    <div>
        Thomas Cherry. <a href="mailto:me@thomas.name">Contact</a> &copy; 2017.
    </div>
</footer>
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

def read(name):
    if (os.path.exists(name)):
        with open(name) as f:
            lines = f.readlines()
            text = "".join(lines)
            return text
    return None

def loadTemplate(base):
    txt = read("%s/%s" % (base, "_template.html"))
    if txt is None:
        txt = read("%s/%s" % (base, "../_template.html"))
    if txt is None:
        txt = page
    return txt

def main():
    root = readCgiParam("DOCUMENT_ROOT", "")
    req_uri = readCgiParam("REQUEST_URI", "/index.md")
    accept = readCgiParam("HTTP_ACCEPT", "*/*")
    
    resp = """<html>
    <head><title>debug</title></head>
    <body>
        Root: %s<br>
        req_uri: %s<br>
        accept: %s
    </body>
</html>""" % (root, req_uri, accept)
    
    if (req_uri=="/"):
        req_uri = "/index.md"
    if req_uri.startswith("/~"):
        req_uri = re.sub(r"/~([a-zA-Z]+)/(.*)", r"\1/Sites/\2", req_uri)
        root = "/Users/"
    else:
        req_uri = re.sub("[^a-zA-Z0-9\.\/-]", "_", req_uri)
    file = "%s%s" % (root, req_uri)
    
    if accept == "text/markdown":
        with open ("%s/%s" % (root, req_uri), "r") as myfile:
            resp = myfile.read()
    else:
        cmd = "cat %s%s | /usr/local/bin/markdown -F 0x200000 " % (root,req_uri)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        cOut = ""
        for line in p.stdout.readlines():
            cOut += line.decode('utf-8')
        css = req_uri.split("/")[-1:][0]
        #resp = loadTemplate(root) % (req_uri, css, "%s/%s" % (root, "_page.html"))
        resp = loadTemplate(root) % (req_uri, css, cOut)
    
    print ("Content-type: text/html; charset=utf-8")
    print
    print

    print resp

################################################################################

main()
