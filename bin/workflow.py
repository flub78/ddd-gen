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

        api_controller, api_model, factory, test_api, test_model

    supported actions:

        - list ??
        - generate generates code into the build directory
        - compare compares the generated code with the installed code
        - install installs the generated code into the install directory hierarchy

"""

epilog = 'Database, user and password can also be defined into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.'
epilog += 'The script uses the following environment variables: WF_TEMPLATES_DIR, WF_BUILD_DIR, WF_INSTALL_DIR'

# List of all templates
default_codes = ['api_controller', 'api_model', 'factory', 'test_model', 'test_api',
                  'react_list_page', 'react_create_page', 'react_edit_page', 'react_list', 'react_edit_form', 'react_create_form', 'translation']
template_files = {
    'api_controller': 'ApiController.php',      #  to be converted in {{Class}}Controller.php
    'api_model': 'Model.php',
    'factory': 'factory.php',
    'test_model': 'ModelTest.php',
    'test_api': 'ApiControllerTest.php',
    'react_list_page' : 'ListPage.js.mustache', 
    'react_create_page': 'CreatePage.js.mustache',
    'react_edit_page': 'EditPage.js.mustache',
    'react_list': 'List.js.mustache',
    'react_edit_form': 'EditForm.js.mustache',
    'react_create_form': 'CreateForm.js.mustache',
    'translation': 'lang.json.mustache'
}

"""
    Intalled file
"""
def filenameToGenerate (code, table, install_dir):
    # Laravel API server
    if code == 'api_controller':
        return (os.path.join(install_dir, r'app\Http\Controllers\api', cg_class(table) + 'Controller.php'))
    
    if code == 'api_model':
        return (os.path.join(install_dir, r'app\Models', cg_class(table) + '.php'))
    
    if code == 'factory':
        return (os.path.join(install_dir, r'database\factories', cg_class(table) + 'Factory.php'))
    
    if code == 'test_model':
        return (os.path.join(install_dir, r'tests\unit', cg_class(table) + 'ModelTest.php'))

    if code == 'test_api':
        return (os.path.join(install_dir, r'tests\Feature\api', cg_class(table) + 'ApiControllerTest.php'))
    
    # React client
    if code == 'react_list_page':
        return (os.path.join(install_dir, r'src\pages', cg_class(table) + 'ListPage.js'))
    
    if code == 'react_create_page':
        return (os.path.join(install_dir, r'src\pages', cg_class(table) + 'CreatePage.js'))
    
    if code == 'react_edit_page':
        return (os.path.join(install_dir, r'src\pages', cg_class(table) + 'EditPage.js'))
    
    if code == 'react_list':
        return (os.path.join(install_dir, r'src\components', cg_class(table) + 'List.js'))
    
    if code == 'react_edit_form':
        return (os.path.join(install_dir, r'src\components', cg_class(table) + 'EditForm.js'))
    
    if code == 'react_create_form':
        return (os.path.join(install_dir, r'src\components', cg_class(table) + 'CreateForm.js'))
    
    if code == 'translation':
        return (os.path.join(install_dir, r'public\locales\en', table + '.json'))

"""
    Filename for the template
"""
def templateFilename (code, templates_dir):
    return os.path.join(templates_dir, template_files[code]) 

"""
    Filename for the generated file
"""
def outputFilename (code, table, build_dir):
    # Laravel API server
    if (code == 'api_controller'):
        return os.path.join(build_dir, cg_class(table) + 'Controller.php')
    
    if (code == 'api_model'):
        return os.path.join(build_dir, cg_class(table) + '.php')    
    
    if (code == 'factory'):
        return os.path.join(build_dir, cg_class(table) + 'Factory.php')
    
    if (code == 'test_model'):
        return os.path.join(build_dir, cg_class(table) + 'ModelTest.php')
    
    if (code == 'test_api'):
        return os.path.join(build_dir, cg_class(table) + 'ApiControllerTest.php')
    
    # React client
    if code == 'react_list_page':
        return os.path.join(build_dir, cg_class(table) + 'ListPage.js')
    
    if code == 'react_create_page':
        return os.path.join(build_dir, cg_class(table) + 'CreatePage.js')
    
    if code == 'react_edit_page':
        return os.path.join(build_dir, cg_class(table) + 'EditPage.js')
    
    if code == 'react_list':
        return os.path.join(build_dir, cg_class(table) + 'List.js')
    
    if code == 'react_edit_form':
        return os.path.join(build_dir, cg_class(table) + 'EditForm.js')
    
    if code == 'react_create_form':
        return os.path.join(build_dir, cg_class(table) + 'CreateForm.js')
    
    if code == 'translation':
        return os.path.join(build_dir, table + '.json')

"""
================================================================================================
"""
parser = argparse.ArgumentParser(
    description='Generate code for a project from metadata and templates',
        epilog=epilog)

parser.add_argument('-a', '--action', type=str, action="store", dest="action", default="generate",
                    help='action to perform: check, generate | compare | install')

parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')

parser.add_argument('-c', '--code', type=str,  action="append",
                    help='type of code to generate: api_controller | api_model | factory | test_model | test_api | react_list_page | react_create_page | react_edit_page | react_list | react_edit_form | react_create_form | translation')

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

"""
    When no table are specified use all of them
"""
def default_tables ():
    reserved = ['failed_jobs', 'migrations', 'password_reset_tokens', 'personal_access_tokens', 'users']
    tbl = table_list()
    result = []
    for t in tbl:
        if t not in reserved:
            result.append(t)
    return result

database, user, password = check_args_and_fetch(args)

# Set the parameters from the environment variables and CLI parameters
templates_dir = os.getenv('WF_TEMPLATES_DIR') if 'WF_TEMPLATES_DIR' in os.environ else ""
if (args.template_dir):
    templates_dir = args.template_dir

build_dir = os.getenv('WF_BUILD_DIR') if 'WF_BUILD_DIR' in os.environ else ""
if (args.build_dir):
    build_dir = args.build_dir

install_dir = os.getenv('WF_INSTALL_DIR') if 'WF_INSTALL_DIR' in os.environ else ""
if (args.install_dir):
    install_dir = args.install_dir

# Check the minimal requirements for the parameters
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

# Generate the code
for table in tables:
    for code in codes:
        process(table, templateFilename(code, templates_dir),
            outputFilename(code, table, build_dir), 
            filenameToGenerate(code, table, install_dir), args.action, args.verbose)

print ("bye ...")