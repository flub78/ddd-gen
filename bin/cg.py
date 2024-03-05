#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *
from lib.code_generator import *


"""
    cg.py

    generate code snippets from MySQL database schema and metadata

    There will be likely several code generators, one for each type of code to generate: Laravel REST API, React web site client, etc.
"""

parser = argparse.ArgumentParser(
    description='Inject snippets into a mustache template. The idea is to generate code based on a database schema and metadata stored as database comments. The script can use different code generators in different contexes. For example, the same metadata can be used to generate a REST API, a React web site client, etc.', 
    epilog='Database, user and password can also be define into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.')

parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')
parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-g', '--generator', type=str, action="store", dest="generator",
                    help='name of the code generator to use')
parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')
parser.add_argument('-t', '--table', type=str, action="store", dest="table",
                    help='table name')
parser.add_argument('-f', '--field', type=str, action="store", dest="field",
                    help='field name')
parser.add_argument('snippet', type=str, action="store",
                    help='snippet to generate')

args = parser.parse_args()

if (args.verbose):
    print('args', args)

database, user, password = check_args_and_fetch(args)

table = args.table if 'table' in args else ""
field = args.field if 'field' in args else ""
snippet = args.snippet

match snippet:
    case "class":
        print(cg_class(table))
    case "element":
        print(cg_element(table))
    case "table":
        print(cg_table(table))
    case "csv_fields":
        print(cg_csv_fields(table))
    case _:
        print("unknown snippet", snippet)

print ("bye ...")