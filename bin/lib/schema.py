#!/usr/bin/python
# -*- coding:utf8 -*

import os
import mysql.connector
import re
import json

"""
Fetch information about the database schema and metadata

For performance resons, the script fetches all the data and keep them in memory.

"""
tables = []
field_l = {}
attributes = {}


def fetch_data(database, user, password):
    host = os.environ['META_DB_HOST'] if 'META_DB_HOST' in os.environ else 'localhost'
    port = os.environ['META_DB_PORT'] if 'META_DB_PORT' in os.environ else 3306

    db = mysql.connector.connect(host=host, user=user, db=database, passwd=password, port=int(port) )
    tables = get_tables(db, database)
    data = {}
    for table in tables:
        data[table] = get_fields(db, database, table)
    db.close()
    return data    

def get_tables(db, database):
    global tables
    cursor = db.cursor()
    query = " SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = '" + database + "'"
    cursor.execute(query)
    for (table_schema, table_name) in cursor:
        tables.append(table_name)
    return tables


def get_fields(db, database, table):
    cursor = db.cursor()
    query = " SHOW FULL COLUMNS FROM " + table + " FROM " + database
    cursor.execute(query)
    field_l[table] = []
    attributes[table] = {}
    for field in cursor:
        # fields.append(id, type, collation, null, key, extra, privileges, comment)

        elt = {}
        elt['field'] = field[0]
        elt['type'] = field[1]
        elt['collation'] = field[2]
        elt['null'] = field[3]
        elt['key'] = field[4]
        elt['default'] = field[5]
        elt['extra'] = field[6]
        elt['privileges'] = field[7]
        elt['comment'] = field[8]
        attributes[table][elt['field']] = elt
        field_l[table].append(elt['field'])
    return attributes

def check_table_exists(table):
    if table not in attributes:
        raise Exception("Table not found: " + table)
    
def check_field_exists(table, field):
    if table not in attributes:
        raise Exception("Table not found: " + table)
    if field not in attributes[table]:
        raise Exception("Field not found: " + field + " in table " + table)
    
def table_list():
    return tables

def field_list(table):
    check_table_exists(table)
    return field_l[table]

def field_attributes(table, field):
    check_field_exists(table, field)
    return attributes[table][field]

def field_name(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['field']

def field_type(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['type']

def field_collation(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['collation']

def field_null(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['null']

def field_key(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['key']

def field_default(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['default']

def field_extra(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['extra']

def field_privileges(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['privileges']

def field_comment(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['comment']

def field_size(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']
    size = re.sub(r'\D', '', type)
    return size

def field_base_type(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']
    base_type = re.sub(r'\d', '', type)
    base_type = base_type.replace('(', '')
    base_type = base_type.replace(')', '')
    words = base_type.split()
    return words[0]

def field_unsigned(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']
    unsigned = 'unsigned' in type
    return unsigned

def field_nullable(table, field):
    check_field_exists(table, field)
    null = attributes[table][field]['null']
    return null == 'YES'

def field_meta(table, field, key):
    check_field_exists(table, field)
    comment = attributes[table][field]['comment']
    meta = json.loads(comment)
    return meta[key] if key in meta else None

def field_subtype(table, field):
    try:
        return field_meta(table, field, 'subtype')
    except:
        return None

"""
    TODO: indirect attributes access

    field_is_foreign_key check if the field is a foreign key returns a boolean
    field_foreign_table  returns the foreign table or null
    field_foreign_field  returns the foreign field or null

    I likely also need information about allowed ranges, allowed values, etc.
"""