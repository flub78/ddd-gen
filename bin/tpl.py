#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *
from lib.code_generator import *
from lib.template_engine import *

"""
    tpl.py

    Inject snippets into a mustache template. It generates code based
    on a database schema and metadata stored as database comments.

    This script is a CLI interface to generate one file.
"""

parser = argparse.ArgumentParser(
    description='Inject snippets into a mustache template. The idea is to generate code based on a database schema and metadata stored as database comments. The script can use different code generators in different contexes. For example, the same metadata can be used to generate a REST API, a React web site client, etc.', 
    epilog='Database, user and password can also be defined into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.')

parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')
parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-t', '--table', type=str, action="store", dest="table",
                    required=True,
                    help='table name')
parser.add_argument('-tp', '--template', type=str, action="store", dest="template",
                    required=True,
                    help='the name of the mustache template')
parser.add_argument('-o', '--output', type=str, action="store", dest="output",
                    help='name of the file to generate')
parser.add_argument('-c', '--compare', type=str, action="store", dest="compare",
                    help='compare the output with a reference file (e.g. a previous version)')
parser.add_argument('-g', '--generator', type=str, action="store", dest="generator",
                    help='name of the code generator to use')
parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')

args = parser.parse_args()

if (args.verbose):
    print('args', args)

database, user, password = check_args_and_fetch(args)

process(args.table, args.template, args.output, args.compare, "compare", args.verbose)
