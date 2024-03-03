#!/usr/bin/python
# -*- coding:utf8 -*

import os
import mysql.connector

"""
Fetch information about the database schema and metadata
"""


def check_env_variable():
    if 'META_DB' not in os.environ:
        print ("Missing environment variable: META_DB")
        exit(1)

    if 'META_DB_USER' not in os.environ:
        print ("Missing environment variable: META_DB_USER")
        exit(1)

    if 'META_DB_PASSWORD' not in os.environ:
        print ("Missing environment variable: META_DB_PASSWORD")
        exit(1)



def get_schema():
    print("Get schema")
    database = os.environ['META_DB']
    user = os.environ['META_DB_USER']
    password = os.environ['META_DB_PASSWORD']
    host = os.environ['META_DB_HOST'] if 'META_DB_HOST' in os.environ else 'localhost'
    port = os.environ['META_DB_PORT'] if 'META_DB_PORT' in os.environ else 3306

    print ("Connecting to database: ", os.environ['META_DB'])
    print ("Using user: ", os.environ['META_DB_USER'])

    db = mysql.connector.connect(host=host, user=user, db=database, passwd=password, port=int(port) )
    cursor = db.cursor()

    query = "SELECT table_schema, table_name FROM INFORMATION_SCHEMA.TABLES"
    cursor.execute(query)

    for (table_schema, table_name) in cursor:
        print (table_schema, table_name)

    db.close()
    return "Get schema"
