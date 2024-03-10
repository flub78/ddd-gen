#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *
import chevron
from lib.code_generator import *
import shutil

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
table = args.table

def cg(text, render):
    # print("cg:", text)
    args = text.split()
    snippet = args[0]

    match snippet:
        case "csv_fields":
            code = cg_csv_fields(table)
        case "guarded":
            code = guarded(table)
        case "create_validation_rules":
            code = create_validation_rules(table)
        case "update_validation_rules":
            code = update_validation_rules(table)
        case "create_set_attributes":
            code = create_set_attributes(table)        
        case "update_set_attributes":
            code = update_set_attributes(table)

        case _:
            code = "unknown snippet " + snippet
            print(code)
            # to be able to run several code generators recognizing different snippets
            # we must return the original text
            return '{{#cg}}' + text + '{{/cg}}'

    result = render(code)
    return result

template = args.template
dict = {
    'class': cg_class(table),
    'element': cg_element(table),
    'table': table,
    'cg': cg
}

res = ""
with open(args.template, 'r') as f: 
    res = chevron.render(f, dict)

if (args.output):
    with open(args.output, 'w') as f:
        f.write(res)
    if (args.verbose):
        print(f"file {args.output} generated")
else:
    print(res)

if (args.compare):
    if (not os.path.exists(args.compare)):
        shutil.copyfile(args.output, args.compare)
        print(f"file {args.compare} does did not exist, it has been created")
        
             
    comparator = 'WinMergeU'        # It must be in the PATH
    cmd = comparator + ' ' + args.output + ' ' + args.compare
    print(cmd)
    os.system(cmd)