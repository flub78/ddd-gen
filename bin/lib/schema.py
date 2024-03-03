#!/usr/bin/python
# -*- coding:utf8 -*

import os
import mysql.connector

"""
Fetch information about the database schema and metadata
"""



def db_connect():
    if 'META_DB' not in os.environ:
        print ("Missing environment variable: META_DB")
        exit(1)

    if 'META_DB_USER' not in os.environ:
        print ("Missing environment variable: META_DB_USER")
        exit(1)

    if 'META_DB_PASSWORD' not in os.environ:
        print ("Missing environment variable: META_DB_PASSWORD")
        exit(1)
    user = os.environ['META_DB_USER']
    password = os.environ['META_DB_PASSWORD']
    database = os.environ['META_DB']
    host = os.environ['META_DB_HOST'] if 'META_DB_HOST' in os.environ else 'localhost'
    port = os.environ['META_DB_PORT'] if 'META_DB_PORT' in os.environ else 3306
    db = mysql.connector.connect(host=host, user=user, db=database, passwd=password, port=int(port) )
    return db

def close_db(db):
    db.close()

def get_tables(db, database):
    tables = []

    cursor = db.cursor()

    query = " SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = '" + database + "'"
    cursor.execute(query)

    for (table_schema, table_name) in cursor:
        tables.append(table_name)

    return tables

def get_fields(db, database, table):
    fields = []

    cursor = db.cursor()

    query = " SHOW COLUMNS FROM " + table + " FROM " + database
    cursor.execute(query)

    for line in cursor:
        # fields.append(id, type, collation, null, key, extra, privileges, comment)
        print("\t\t", line)

    return fields
