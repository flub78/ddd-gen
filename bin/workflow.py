#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
from lib.schema import *

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

parser = argparse.ArgumentParser(
    description='Generate code for a project from metadata and templates')

parser.add_argument('-a', '--action', type=str, action="store", dest="action",
                    help='action to perform: list, generate | compare | install')

parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-c', '--code', type=str, action="store", dest="code",
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

database, user, password = check_args_and_fetch(args)

tables = table_list()

print ("bye ...")