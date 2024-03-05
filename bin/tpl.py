#!/usr/bin/python
# -*- coding:utf8 -*
import os
import argparse
from lib.schema import *

"""
    tpl.py

    Inject snippets into a mustache template. The idea is to generate code based
    on a database schema and metadata stored as database comments.

    The script can use different code generators in different contexes. 
    For example, the same metadata can be used to generate a REST API, 
    a React web site client, etc.
"""

parser = argparse.ArgumentParser(
    description='Inject snippets into a mustache template. The idea is to generate code based on a database schema and metadata stored as database comments. The script can use different code generators in different contexes. For example, the same metadata can be used to generate a REST API, a React web site client, etc.', 
    epilog='Database, user and password can also be define into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.')

parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-t', '--template', type=str, action="store", dest="template",
                    help='the name of the mustache template')
parser.add_argument('-o', '--output', type=str, action="store", dest="output",
                    help='name of the file to generate')
parser.add_argument('-g', '--generator', type=str, action="store", dest="generator",
                    help='name of the code generator to use')
parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')
parser.add_argument('action', type=str, action="store",  
                    help='action to perform: generate | compare | install')

args = parser.parse_args()
print('args', args)



print ("bye ...")