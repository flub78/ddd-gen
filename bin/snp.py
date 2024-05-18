#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *
from lib.code_generator import *

"""
    snp.py

    generate code snippets from MySQL database schema and metadata

    There will be likely several code generators, one for each type of code to generate: Laravel REST API, React web site client, etc.
"""

"""
The simpliest user interface is likely tp pass a set of positional arguments with the name of the snippet as first arguments and arguments to apply to the snippet as the following arguments.
"""

epilog = """
Database, user and password can also be define into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.
"""


parser = argparse.ArgumentParser(
    description='Inject snippets into a mustache template. The idea is to generate code based on a database schema and metadata stored as database comments. The script can use different code generators in different contexes. For example, the same metadata can be used to generate a REST API, a React web site client, etc.', 
    epilog=epilog)

parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')
parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-g', '--generator', type=str, action="store", dest="generator",
                    help='name of the code generator to use')

parser.add_argument('-l', '--list', action="store_true", dest="list",
                    help='list of the supported snippets')

parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')

parser.add_argument('snippet', type=str, action="store",
                    help='snippet to generate')
parser.add_argument('cg_args', type=str, action="store",  nargs='*',
                    help='arguments for code generator')

args = parser.parse_args()

if (args.verbose):
    print('args', args)

database, user, password = check_args_and_fetch(args)

table = args.table if 'table' in args else ""
field = args.field if 'field' in args else ""
snippet = args.snippet
cg_arg = args.cg_args

snippets = ["cg_class", "cg_element", "cg_table", "cg_primary_key", "cg_url",
             "cg_subtype", "csv_fields", "guarded", "create_validation_rules",
             "update_validation_rules", "create_set_attributes", "update_set_attributes",
             "primary_key_declaration", "factory_referenced_models", "factory_field_list",
             "csv_high_variability_fields",
             "field_list_translation", "field_list_cells", "field_list_titles", "field_list_input_form",
             "join_for_images"]

if (args.list):
    print("supported snippets:")
    for s in snippets:
        print(s)
    exit(0)
"""
The following code is likely to be considered as evil because it uses eval to call the code generator functions. This is a security risk. 
The code generator function should be called by name 
and the name should be checked against a list of authorized code generators. 

However the operatro of this script has already access to the database and the operating system and can do anything he wants
"""
if (not snippet in globals()):
    print("unknown snippet", snippet)
    exit(1)

func=globals()[snippet]
if callable(func):
    print(func(*cg_arg))
