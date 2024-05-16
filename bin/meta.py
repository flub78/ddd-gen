#!/usr/bin/python
# -*- coding:utf8 -*
import argparse
import sys
from lib.schema import *

"""
    Meta.py

    Analyze a MySql database schema and metadata stored as database comments.

    The scripts uses the following environment variables:
    - META_DB_HOST: the host name of the MySql server
    - META_DB_PORT: the port number of the MySql server
    - META_DB_USER: the user name to connect to the MySql server
    - META_DB_PASSWORD: the password to connect to the MySql server
    - META_DB_NAME: the name of the database to analyze

	meta database						# returns the database name
	
	meta -d boards tables				# returns all the table names
	
	meta -d boards -t users fields		# returns the field names for a table
	
	meta -d boards -t users -f email	# returns the field attributes
	
		id
		type
		collation
		null
		key
		extra
		privileges
		comments
		
		base_type	returns the type with no size
		size		returns the size
		meta_attribute (database, table, field, attribute) the value or null
		
		others functions
		nullable
		is_foreign_key
		foreign_table
		foreign_field
"""

def print_field(table, field, full=False):
    if (full):
        print ("\t\t", field)

        print ("\t\t\t field:",field_name(table, field))
        print ("\t\t\t type:",field_type(table, field))
        print ("\t\t\t subtype :",field_subtype(table, field))
        print ("\t\t\t size:",field_size(table, field))
        print ("\t\t\t base_type:",field_base_type(table, field))
        print ("\t\t\t enum_values:",field_enum_values(table, field))
        print ("\t\t\t unsigned:",field_unsigned(table, field))

        print ("\t\t\t collation:",field_collation(table, field))
        print ("\t\t\t null:",field_null(table, field))
        print ("\t\t\t nullable:", field_nullable(table, field))

        print ("\t\t\t key:",field_key(table, field))
        print ("\t\t\t default:",field_default(table, field))
        print ("\t\t\t extra:",field_extra(table, field))
        print ("\t\t\t privileges:",field_privileges(table, field))
        print ("\t\t\t comment:",field_comment(table, field))
        print ("\t\t\t foreign_key:",field_foreign_key(table, field))
        print ('')
    else:
        subtype = field_subtype(table, field) 
        if subtype == None:
            subtype = ""
        print ("\t\t", field, ' ', field_type(table, field),  subtype)

def print_foreign_key(tables):
    referenced_by = {}

    for table in tables:
        cnt = 0
        fields = field_list(table)
        for field in fields:
            fk = field_foreign_key(table, field)
            if fk:
                if (cnt == 0):
                    print("\t", table)
                print ("\t\t", field)
                print ("\t\t\t foreign_key:", fk)
                cnt += 1
                if (referenced_by.get(fk['table']) == None):
                    referenced_by[fk['table']] = []
                referenced_by[fk['table']].append(table)

    print ("")
    print ("Referenced by:")
    for table in referenced_by:
        print("\t", table)
        for ref in referenced_by[table]:
            print("\t\t", ref)
            

parser = argparse.ArgumentParser(
    description='Extract meta data from a MySql database.',
    epilog='Database, user and password can also be define into the META_DB, META_DB_USER, META_DB_PASSWORD environment variables.')

parser.add_argument('-v', '--verbose', action="store_true", dest="verbose",
                    help='verbose mode')
parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-t', '--table', type=str, action="store", dest="table",
                    help='table name')
parser.add_argument('-f', '--field', type=str, action="store", dest="field",
                    help='field name')
parser.add_argument('action', type=str, action="store", nargs='?',
                    help='action to perform')
parser.add_argument('-u', '--user', type=str, action="store", dest="user",
                    help='database user')
parser.add_argument('-p', '--password', type=str, action="store", dest="password",
                    help='database user')
args = parser.parse_args()

if (args.verbose):
    print('args = ', args)


try:
    database, user, password = check_args_and_fetch(args)
except Exception as e:
    print(type(e))
    print(e)
    print(e.args)
    exit(1)

if (args.table):
    if (args.field):
        # table and field are specified
        print("\t", args.table)
        print_field(args.table, args.field, args.verbose)
        exit(0)

    # only table is specified
    table = args.table
    fields = field_list(table)
    print("\t", args.table)
    for field in fields:
        print_field(table, field, args.verbose)

    tm = table_meta(table)
    print("\n")
    print("\t", table, " metadata:", tm)
    exit(0)

# only database is specified
tables = table_list()

print(database)

if (args.action == "list"):
    print("tables", tables)
    exit(0)

elif (args.action == "foreign"):
    print_foreign_key(tables)
    exit(0)

else:    
    for table in tables:
        print("\t", table)

        fields = field_list(table)
        for field in fields:
            print_field(table, field, args.verbose)

        tm = table_meta(table)
        print("\n")
        print("\t", table, " metadata:", tm)
        print("\n")

print ("bye ...")