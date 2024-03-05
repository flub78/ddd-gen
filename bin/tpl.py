#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *
import chevron
from lib.code_generator import *



"""
    tpl.py

    Inject snippets into a mustache template. The idea is to generate code based
    on a database schema and metadata stored as database comments.

    The script can use different code generators in different contexes. 
    For example, the same metadata can be used to generate a REST API, 
    a React web site client, etc.

    The script work on the following markers:
    {{#cg}}  snippet definition  {{/cg}}

    and replace them with the content of the snippet.


"""

parser = argparse.ArgumentParser(
    description='Inject snippets into a mustache template. The idea is to generate code based on a database schema and metadata stored as database comments. The script can use different code generators in different contexes. For example, the same metadata can be used to generate a REST API, a React web site client, etc.', 
    epilog='Database, user and password can also be define into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.')

parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')
parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-t', '--template', type=str, action="store", dest="template",
                    required=True,
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

if (args.verbose):
    print('args', args)

database, user, password = check_args_and_fetch(args)

def first(text, render):
    # return only first occurance of items
    print("first", text)
    result = render(text)
    return [ x.strip() for x in result.split(" || ") if x.strip() ][0]

def cg(text, render):
    print("cg:", text)
    args = text.split()
    snippet = args[0]

    match snippet:
        case "class":
            code = cg_class(args[1])
        case "element":
            code = cg_element(args[1])
        case "table":
            result = cg_table(args[1])
        case "csv_fields":
            code = cg_csv_fields(args[1])
        case _:
            code = "unknown snippet " + snippet

    result = render(code)
    return result

template = args.template
dict = {
    'mustache': 'World',
    'first': first,
    'cg': cg
}

with open(template, 'r') as f:
    res = chevron.render(f, dict)
    print(res)

print ("bye ...")