#!/usr/bin/python
# -*- coding:utf8 -*
import os
import argparse
import mysql.connector
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

parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
parser.add_argument('--level', type=int, choices=[0, 1, 2, 3, 4, 5],
                    action="store", dest="level",
                    help='criticity level, from 0 to 5')

args = parser.parse_args()


def print_env(env):
    try:
        print(env, ": ", os.environ[env])
    except Exception as e:
        print ("Unknown environment variable: ", env)
        # print (e)   
    
# Check required environment variables

db = db_connect()

database = os.environ['META_DB']
tables = get_tables(db, database)

print(database)
for table in tables:
    print("\t", table)
    fields = get_fields(db, database, table)
    print (fields)

close_db(db)
print ("bye ...")