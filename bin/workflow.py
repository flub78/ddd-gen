#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
import os
from lib.schema import *
from lib.code_generator import *
from lib.template_engine import *


"""
    workflow.py

    Control a project code generation

    This script has information on the type of files to generate, where to generate them, etc.

    The scripts uses the following environment variables:
    - META_DB_HOST: the host name of the MySql server
    - META_DB_PORT: the port number of the MySql server
    - META_DB_USER: the user name to connect to the MySql server
    - META_DB_PASSWORD: the password to connect to the MySql server
    - META_DB_NAME: the name of the database to analyze

    - WF_TEMPLATES_DIR: the directory where the templates are stored
    - WF_BUILD_DIR: the directory where the generated files are stored
    - WF_INSTALL_DIR: the directory where the generated files are installed


    Supported code:

        api_controller, api_model, all

    supported actions:

        - list ??
        - generate generates code into the build directory
        - compare compares the generated code with the installed code
        - install installs the generated code into the install directory hierarchy

"""

epilog = 'Database, user and password can also be defined into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.'
epilog += 'The script uses the following environment variables: WF_TEMPLATES_DIR, WF_BUILD_DIR, WF_INSTALL_DIR'

default_codes = ['api_controller', 'api_model']
template_files = {
    'api_controller': 'ApiController.php',      #  to be converted in {{Class}}Controller.php
    'api_model': 'Model.php'
}

def filenameToGenerate (code, table, install_dir):
    if code == 'api_controller':
        return (os.path.join(install_dir, r'app\Http\Controllers\api', cg_class(table) + 'Controller.php'))
    
    if code == 'api_model':
        return (os.path.join(install_dir, r'app\Models', cg_class(table) + '.php'))
    
def templateFilename (code, templates_dir):
    return os.path.join(templates_dir, template_files[code]) 

def outputFilename (code, table, build_dir):
    if (code == 'api_controller'):
        return os.path.join(build_dir, cg_class(table) + 'Controller.php')
    
    if (code == 'api_model'):
        return os.path.join(build_dir, cg_class(table) + '.php')    

parser = argparse.ArgumentParser(
    description='Generate code for a project from metadata and templates',
        epilog=epilog)

parser.add_argument('-a', '--action', type=str, action="store", dest="action", default="compare",
                    help='action to perform: list, generate | compare | install')

parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')

parser.add_argument('-c', '--code', type=str,  action="append",
                    help='type of code to generate: api_controller | api_model')

parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')
parser.add_argument('-b', '--build_dir', type=str, action="store", dest="build_dir",
                    help='directory where the generated files are stored')
parser.add_argument('-td', '--template_dir', type=str, action="store", dest="template_dir",
                    help='directory for templates')
parser.add_argument('-i', '--install_dir', type=str, action="store", dest="install_dir",
                    help='directory where the APPLICATION is installed')
parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')

parser.add_argument('tables', type=str, action="store", nargs='*',
                    help='List of tables to process')

args = parser.parse_args()

if (args.verbose):
    print('args', args)

def default_tables ():
    reserved = ['failed_jobs', 'migrations', 'password_reset_tokens', 'personal_access_tokens', 'users']
    tbl = table_list()
    result = []
    for t in tbl:
        if t not in reserved:
            result.append(t)
    return result

database, user, password = check_args_and_fetch(args)

templates_dir = os.getenv('WF_TEMPLATES_DIR') if 'WF_TEMPLATES_DIR' in os.environ else ""
if (args.template_dir):
    templates_dir = args.template_dir

build_dir = os.getenv('WF_BUILD_DIR') if 'WF_BUILD_DIR' in os.environ else ""
if (args.build_dir):
    build_dir = args.build_dir

install_dir = os.getenv('WF_INSTALL_DIR') if 'WF_INSTALL_DIR' in os.environ else ""
if (args.install_dir):
    install_dir = args.install_dir

param_error = False
if (templates_dir == ""):
    print("template_dir not defined")
    param_error = True

if (build_dir == ""):
    print("build_dir not defined")
    param_error = True

if (install_dir == ""):
    print("install_dir not defined")
    param_error = True


if (not args.code):
    codes = default_codes
else:
    codes = args.code

for code in codes:
    if (code not in default_codes):
        print("code ", code, " is not supported")
        param_error = True

if (param_error):
    exit(1)

tables = args.tables
if (len(tables) == 0):
    tables = default_tables()

if (args.verbose):
    print("build dir = ", build_dir)
    print("install dir = ", install_dir)
    print("templates dir = ", templates_dir)
    print("action = ", args.action)
    # print('tables', tables)
    # print('codes', codes)

for table in tables:
    for code in codes:
        # if (args.verbose):
        #     print("generating ",code, 'for', table)
        #     print ('install:', filenameToGenerate(code, table, install_dir))
        #     print ('output:', outputFilename(code, table, build_dir))
        #     print ('template:', templateFilename(code, templates_dir))
        #     print ("")
        process(table, templateFilename(code, templates_dir),
            outputFilename(code, table, build_dir), 
            filenameToGenerate(code, table, install_dir), "check", args.verbose)

print ("bye ...")