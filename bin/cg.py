#!/usr/bin/python
# -*- coding:utf8 -*
import os
import argparse
from lib.schema import *

"""
    cg.py

    Code generator.

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

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-d', '--database', type=str, action="store", dest="database",
                    help='database name')
parser.add_argument('-t', '--table', type=str, action="store", dest="table",
                    help='table name')
parser.add_argument('-f', '--field', type=str, action="store", dest="field",
                    help='field name')
parser.add_argument('action', type=str, action="store", nargs='?',
                    help='action to perform')

args = parser.parse_args()
print("Metadata code generator")
print('args', args)


print ("bye ...")