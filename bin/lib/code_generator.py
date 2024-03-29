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

def cg_primary_key(table):
    return primary_key(table)

"""
    Possible values are:
    url, password, email, phone, image, file, enumerate, boolean, bitfield, currency, foreign_key, color,
    csv_int, csv_string
"""
def cg_subtype(table, field):
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

    if (field_type(table, field) == 'tinyint(1)'):
        return 'boolean'    

    return None
    

"""
    Return a comma separated list of fields with double quotes for a given table
"""
def csv_fields(table):
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
        if field_guarded(table, field):
            continue
        list.append(field)
    return list

def high_variability_list(table):
    list = []
    flist = field_list(table)
    for field in flist:
        if field_is_primary_key(table, field):
            continue
        if field_guarded(table, field):
            continue
        if field_is_unique(table, field):
            continue
        if field_base_type(table, field) == 'tinyint':
            continue
        if field_base_type(table, field) == 'enum':
            continue
        if field_foreign_key(table, field):
            continue
        list.append(field)
    return list

def csv_high_variability_fields(table):
    list = high_variability_list(table)
    list_with_quotes = [f"\"{x}\"" for x in list]
    return ", ".join(list_with_quotes)

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
    reg_expr = False
    if (not field_nullable(table, field)) and create:
        rules.append('required')

    if field_base_type(table, field) == 'varchar':
        rules.append('string')
        size = field_size(table, field)
        rules.append(f'max:{size}')

    if cg_subtype(table, field) == 'email':
        rules.append('email')

    if cg_subtype(table, field) == 'boolean' or field_base_type(table, field) == 'boolean':
        rules.append('boolean')

    if cg_subtype(table, field) == 'date':
        rules.append('date')

    if cg_subtype(table, field) == 'time':
        rules.append('time')

    if cg_subtype(table, field) == 'csv_int':
        reg_expr = True
        rules.append(r'regex:(\d+),?')

    if cg_subtype(table, field) == 'csv_string':
        reg_expr = True
        # 'regex:/(^([a-zA-Z]+)(\d+)?$)/u'
        # 'regex://\'(.+?)\'|\"(.+?)\"'
        rx = 'regex:/' + "\\\'(.+?)\\\'"  + '|' + '\\\"(.+?)\\\"' +   '/'
        rules.append(rx)

    if field_base_type(table, field) == 'enum':
        values = field_enum_values(table, field)
        rules.append('in:' + ",".join(values))

    if field_foreign_key(table, field):
        fk = field_foreign_key(table, field)
        rules.append('exists:' + fk['table'] + ',' + fk['field'])

    if (reg_expr):
        rules_list = '[' + ", ".join( '"' + rule + '"' for rule in rules) + ']'
        return f"\"{field}\" => " +  rules_list + ","
    else:
        rules_list = "|".join(rules)      
        return f"\"{field}\" => '" +  rules_list + "',"

"""
    Return the list of validation rules for the fillable fields of a table
"""
def validation_rules(table, ntabs = 3, create = True):
    flist = fillable_list(table)
    res = ""
    tabs = "\t"*int(ntabs)
    cnt = 0
    for field in flist:
        if (cnt):
            res = res + tabs
        res = res + create_validation_rule(table, field, create) + "\n"
        cnt = cnt + 1
    return res

def create_validation_rules(table, ntabs = 4):
    return validation_rules(table, ntabs, True)

"""
    Return the list of validation rules for the fillable fields of a table
"""
def update_validation_rules(table, ntabs = 4):
    return validation_rules(table, ntabs, False)

"""
    set element attributes
"""
def create_set_attributes(table, ntabs = 3):
    flist = fillable_list(table)
    res = ""
    tabs = "\t"*int(ntabs)
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
def update_set_attributes(table, ntabs=3):
    flist = fillable_list(table)
    res = ""
    tabs = "\t"*int(ntabs)
    cnt = 0
    for field in flist:
        if (cnt):
            res = res + tabs
        res = res + 'if ($request->' + field + ') {' + "\n"
        res = res + tabs + "\t" + '$element->' + field + ' = $request->' + field + ";\n"
        res = res + tabs + '}' + "\n"
        cnt = cnt + 1
    return res

"""
    when the primary key is not bigint('id') we must declare it
"""
def primary_key_declaration(table):
    flist = field_list(table)
    for field in flist:
        if field_is_primary_key(table, field):
            if (field == 'id'):
                return ""
            else:
                res = f"protected $primaryKey = '{field}';"
                if (field_base_type(table, field) == 'varchar'):
                    res = res + "\n\t" + "protected $keyType = 'string';"
                return res
    return ""

"""
    return a list of models referenced by a factory
"""
def factory_referenced_models(table):
    flist = fillable_list(table)
    res = ""
    for field in flist:
        if field_foreign_key(table, field):
            fk = field_foreign_key(table, field)
            model = cg_class(fk['table'])
            res = res + f"use App\\Models\\{model};\n"
    return res

"""
    return a faker line for a field
"""
def factory_field(table, field):

    subtype = cg_subtype(table, field)
    # print(table, field, f"subtype: {subtype}")

    unique = 'unique()->' if (field_is_unique(table, field)) else ''

    if (field_meta(table, field, 'faker')):
        return f"'{field}' => $this->faker->{unique}{field_meta(table, field, 'faker')},"
    
    # this one needs to be confirmed after some experiment, it could match
    # too many cases
    if ('name' in field):
        return f"'{field}' => $this->faker->{unique}name,"        

    if subtype == 'email':
        return f"'{field}' => $this->faker->{unique}safeEmail,"
    
    
    if subtype == 'csv_string':
        size = field_size(table, field)
        nb = 6
        return f"'{field}' => $this->faker->csv_string({nb}),"
    
    if field_foreign_key(table, field):
        fk = field_foreign_key(table, field)
        target_table = fk['table']
        target_model = cg_class(target_table)
        target_key = cg_primary_key(target_table)
        return f"'{field}' => {target_model}::inRandomOrder()->first()->{target_key},"
    
    if field_base_type(table, field) == 'varchar':
        size = field_size(table, field)
        nb = int(size / 15)
        return f"'{field}' => $this->faker->{unique}sentence({nb}),"
    
    if field_base_type(table, field) == 'int':
        return f"'{field}' => $this->faker->randomNumber(5),"
    
    if field_base_type(table, field) == 'tinyint':
        return f"'{field}' => $this->faker->boolean,"
    
    if field_base_type(table, field) == 'enum':
        values = field_enum_values(table, field)
        return f"'{field}' => $this->faker->randomElement({values}),"
    
    if field_base_type(table, field) == 'date':
        return f"'{field}' => $this->faker->date(),"
    
    if field_base_type(table, field) == 'time':
        return f"'{field}' => $this->faker->time(),"
    
    if field_base_type(table, field) == 'datetime':
        return f"'{field}' => $this->faker->dateTime(),"
    
    if field_base_type(table, field) == 'timestamp':
        return f"'{field}' => $this->faker->dateTime(),"
    
    if field_base_type(table, field) == 'text':
        return f"'{field}' => $this->faker->text,"
    
    return f"'{field}' => $this->faker->{unique}word,"


"""
    return a list of fields creation methods for a factory
"""
def factory_field_list(table, indent=3):
    flist = fillable_list(table)
    res = ""
    cnt = 0
    tabs = "\t"*indent
    for field in flist:
        if (cnt): res = res + tabs
        res = res + factory_field(table, field) + "\n"
        cnt = cnt + 1
    return res