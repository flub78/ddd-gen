#!/usr/bin/python
# -*- coding:utf8 -*

import os
import mysql.connector
import re
import json
from lib.schema import *

"""
Fetch information about the database schema and metadata

For performance resons, the script fetches all the data and keep them in memory.

"""
tables = []
field_l = {}
attributes = {}
foreign = {}

# Utility functions
def toBoolean(str):
    if str == None: return False
    return str.lower() in ['true', 'yes', '1']

# Database functions
"""
    Fetch the database schema and metadata and store them in memory
"""
def fetch_data(database, user, password):
    host = os.environ['META_DB_HOST'] if 'META_DB_HOST' in os.environ else 'localhost'
    port = os.environ['META_DB_PORT'] if 'META_DB_PORT' in os.environ else 3306

    db = mysql.connector.connect(host=host, user=user, db=database, passwd=password, port=int(port) )
    tables = get_tables(db, database)
    data = {}
    for table in tables:
        data[table] = get_fields(db, database, table)
        fetch_foreign_key_information(db, database, table)
    db.close()

    return data    

"""
    Get the list of tables in the database
"""
def get_tables(db, database):
    global tables
    cursor = db.cursor()
    query = " SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = '" + database + "'"
    cursor.execute(query)
    for (table_schema, table_name) in cursor:
        tables.append(table_name)
    return tables

"""
    Analyze the CLI arguments and fetch the data from the database
"""
def check_args_and_fetch(args):
    # Analyze CLI parameters and env variables
    database = os.environ['META_DB'] if 'META_DB' in os.environ else ""
    if args.database:
           database = args.database

    user = os.environ['META_DB_USER'] if 'META_DB_USER' in os.environ else ""
    if args.user:
        user = args.user

    password = os.environ['META_DB_PASSWORD'] if 'META_DB_PASSWORD' in os.environ else ""
    if args.password:
        password = args.password

    if (not database):
        print ("database not defined: META_DB or -d argument²")
        exit(1)

    if (not user):
        print ("user not defined: META_DB_USER or -u argument")
        exit(1)

    if (not password):
        print ("password not defined: META_DB_PASSWORD or -p argument")
        exit(1)
    fetch_data(database, user, password)
    return database, user, password

"""
    Fetch the list of fields for a table
"""
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

"""
    Fetch the foreign key information for a table
    and store them in memory
"""
def fetch_foreign_key_information(db, database, table):
    fields = field_l[table]
    cursor = db.cursor()
    query = "SELECT CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
    query = query + "FROM information_schema.KEY_COLUMN_USAGE "
    query = query + "WHERE CONSTRAINT_SCHEMA = '" + database + "' AND TABLE_NAME = '" + table + "'" 
    cursor.execute(query)
    
    foreign[table] = {}

    for line in cursor:
        referenced_table = line[4]
        table = line[2]
        field = line[3]
        reference = {}
        reference['table'] = line[4]
        reference['field'] = line[5]
        if (referenced_table):
            foreign[table][field] = reference
    return foreign

"""
    Check if a table exists 
"""
def check_table_exists(table):
    if table not in attributes:
        raise Exception("Table not found: " + table)

"""
    Check if a field exists in a table
"""    
def check_field_exists(table, field):
    if table not in attributes:
        raise Exception("Table not found: " + table)
    if field not in attributes[table]:
        raise Exception("Field not found: " + field + " in table " + table)

"""
    List the tables in the database
"""    
def table_list():
    return tables

"""
    List the fields in a table
"""
def field_list(table):
    check_table_exists(table)
    return field_l[table]

""" 
    return the attributes of a field
"""
def field_attributes(table, field):
    check_field_exists(table, field)
    return attributes[table][field]

"""
    return the name of a field
"""
def field_name(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['field']

"""
    return the type of a field
"""
def field_type(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['type']

"""
    return the collation of a field
"""
def field_collation(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['collation']

"""
    return the nullability of a field
"""
def field_null(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['null']

"""
    return the key of a field
"""
def field_key(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['key']

"""
    return the default value of a field
"""
def field_default(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['default']

"""
    return the extra values for a field
"""
def field_extra(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['extra']

"""
    return the privileges of a field
"""
def field_privileges(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['privileges']

"""
    return the comment of a field
"""
def field_comment(table, field):
    check_field_exists(table, field)
    return attributes[table][field]['comment']

"""
    return the size of a field
"""
def field_size(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']

    reg = r'(.+)\((.*)\)'
    match = re.match(reg, type)

    if match:
        insideBracket = match.group(2)
        if insideBracket.isdigit():
            return insideBracket
        else:
            return 0
    else:
        return 0

"""
    Extract the base type from the type
    some types are just string like date, timestamp, etc.
    some types have a size inside parenthesis like varchar(255), int(11), etc.
    some types have a size and a number of decimal digits like decimal(10,2), float(10,2), etc.
    some types have a range like enum('a', 'b', 'c'), set('a', 'b', 'c'), etc. 

"""
# re.search(r'\((.*?)\)',s).group(1)    
def field_base_type(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']

    reg = r'(.+)\((.*)\)'
    match = re.match(reg, type)

    if match:
        return match.group(1)
    else:
        return type

"""
    return the enum values of a field
    if the field is not an enum returns an empty list
"""
def field_enum_values(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']
    reg = r'enum\((.*)\)'
    match = re.match(reg, type)
    if match:
        insideBracket = match.group(1)
        insideBracket = insideBracket.replace("'", "")
        return insideBracket.split(',')
    else:
        return []

"""
    return the unsignedness of a field
"""
def field_unsigned(table, field):
    check_field_exists(table, field)
    type = attributes[table][field]['type']
    unsigned = 'unsigned' in type
    return unsigned

"""
    return the nullable of a field
"""
def field_nullable(table, field):
    check_field_exists(table, field)
    null = attributes[table][field]['null']
    return null == 'YES'

# Indirect metadata functions
def field_meta(table, field, key):
    check_field_exists(table, field)
    comment = attributes[table][field]['comment']
    if not comment:
        return None
    meta = json.loads(comment)
    return meta[key] if key in meta else None

"""
    return the subtype of a field
"""
def field_subtype(table, field):
    try:
        return field_meta(table, field, 'subtype').strip()
    except:
        return None

"""
    check if a field is mass assignable
"""
def field_fillable(table, field):
    check_field_exists(table, field)
    if field in ["id", "created_at", "updated_at"]: return False
    if (field_meta(table,field, 'fillable') != None): 
        return toBoolean(field_meta(table,field, 'fillable'))
    return not toBoolean(field_meta(table,field, 'guarded'))
    
def field_guarded(table, field):
    return not field_fillable(table, field)

"""
If a field is a foreign key returns information about it
else returns None
"""
def field_foreign_key(table, field):
    check_field_exists(table, field)
    if table in foreign:
        if field in foreign[table]:
            return foreign[table][field]
    return None

"""
    TODO: indirect attributes access

    field_is_foreign_key check if the field is a foreign key returns a boolean
    field_foreign_table  returns the foreign table or null
    field_foreign_field  returns the foreign field or null

    I likely also need information about allowed ranges, allowed values, etc.
"""