#!/usr/bin/python
# -*- coding:utf8 -*
from lib.schema import *

"""
    code_generator.py

    Generate code for Laravel RESTful API
"""

def cg_class(table):
    return ''.join(x.capitalize() for x in table.split('_')).rstrip('s')

def cg_element(table):
    return table.rstrip('s')

def cg_table(table):
    return table

"""
    Possible values are:
    datetime, date, time, timestamp, year
    url, password, email, phone, image, file, enumerate, boolean, bitfield, currency, foreign_key, color


"""
def subtype(table, field):
    if (field_subtype(table, field)):
        return field_subtype(table, field)
    if ('mail' in field):
        return 'email'
    if ('password' in field):
        return 'password'
    if ('date' in field):
        return 'date'
    if ('time' in field):
        return 'time'
    if ('url' in field):
        return 'url'
    if ('phone' in field):
        return 'phone'
    if ('image' in field):
        return 'image'
    if ('file' in field):
        return 'file'
    return None
    

"""
    Return a comma separated list of fields with double quotes for a given table
"""
def cg_csv_fields(table):
    list = field_list(table)
    list_with_quotes = [f"\"{x}\"" for x in list]
    return ", ".join(list_with_quotes)

"""
    Return a list of fillable fields for a given table
"""
def fillable_list(table):
    list = []
    flist = field_list(table)
    for field in flist:
        if not field_guarded(table, field):
            list.append(field)
    return list

"""
    Return a comma separated list of not fillable (guarded) fields with double quotes for a given table
"""
def guarded(table):
    list = []
    flist = field_list(table)
    for field in flist:
        if field_guarded(table, field):
            list.append(field)
    list_with_quotes = [f"\"{x}\"" for x in list]
    return ", ".join(list_with_quotes)

"""
    Return the validation rule for one field
"""
def create_validation_rule(table, field, create = True):
    rules = []
    if (not field_nullable(table, field)) and create:
        rules.append('required')
    if field_base_type(table, field) == 'varchar':
        rules.append('string')
        size = field_size(table, field)
        rules.append(f'max:{size}')
    if subtype(table, field) == 'email':
        rules.append('email')
    if subtype(table, field) == 'boolean' or field_base_type(table, field) == 'boolean':
        rules.append('boolean')
    if subtype(table, field) == 'date':
        rules.append('date')
    if subtype(table, field) == 'time':
        rules.append('time')

    if field_base_type(table, field) == 'enum':
        values = field_enum_values(table, field)
        rules.append('in:' + ",".join(values))
        
    rules_list = "|".join(rules)               
    return f"\"{field}\" => '" +  rules_list + "',"

"""
    Return the list of validation rules for the fillable fields of a table
"""
def validation_rules(table, create = True):
    flist = fillable_list(table)
    res = ""
    tabs = "\t\t\t"
    cnt = 0
    for field in flist:
        if (cnt):
            res = res + tabs
        res = res + create_validation_rule(table, field, create) + "\n"
        cnt = cnt + 1
    return res

def create_validation_rules(table):
    return validation_rules(table, True)

"""
    Return the list of validation rules for the fillable fields of a table
"""
def update_validation_rules(table):
    return validation_rules(table, False)

"""
    set element attributes
"""
def create_set_attributes(table):
    flist = fillable_list(table)
    res = ""
    tabs = "\t\t"
    cnt = 0
    for field in flist:
        if (cnt):
            res = res + tabs
        res = res + '$element->' + field + ' = $request->' + field + ";\n"
        cnt = cnt + 1
    return res

"""
    set element attributes

    to test it:
    cg -t boards -f name update_set_attributes
"""
def update_set_attributes(table):
    flist = fillable_list(table)
    res = ""
    tabs = "\t\t"
    cnt = 0
    for field in flist:
        if (cnt):
            res = res + tabs
        res = res + 'if ($request->' + field + ') {' + "\n"
        res = res + tabs + "\t" + '$element->' + field + ' = $request->' + field + ";\n"
        res = res + tabs + '}' + "\n"
        cnt = cnt + 1
    return res