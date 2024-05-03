#!/usr/bin/python
# -*- coding:utf8 -*
import chevron
import shutil
import filecmp
import os

from lib.code_generator import *

"""
    template_engine.py

    Inject snippets into a mustache template. The idea is to generate code based
    on a database schema and metadata stored as database comments.

    The script can use different code generators in different contexes. 
    For example, the same metadata can be used to generate a REST API, 
    a React web site client, etc.

    The script work on the following markers:
    {{#cg}}  snippet definition  {{/cg}}

    and replace them with the content of the snippet.
"""

table = ""

def cg(text, render):
    # print("cg:", text)
    args = text.split()
    snippet = args[0]

    match snippet:
        case "csv_fields":
            code = csv_fields(table)
        case "guarded":
            code = guarded(table)
        case "create_validation_rules":
            code = create_validation_rules(table)
        case "update_validation_rules":
            code = update_validation_rules(table)
        case "create_set_attributes":
            code = create_set_attributes(table)        
        case "update_set_attributes":
            code = update_set_attributes(table)
        case "primary_key_declaration":
            code = primary_key_declaration(table)
        case "factory_referenced_models":
            code = factory_referenced_models(table)
        case "factory_field_list":
            code = factory_field_list(table)
        case "csv_high_variability_fields":
            code = csv_high_variability_fields(table)
        case "field_list_translation":
            code = field_list_translation(table)
        case "field_list_cells":
            code = field_list_cells(table)
        case "field_list_titles":
            code = field_list_titles(table)
        case "field_list_input_form":
            code = field_list_input_form(table)
        case "set_form_data":
            code = set_form_data(table)
                    
        case _:
            code = "unknown snippet " + snippet
            print(code)
            # to be able to run several code generators recognizing different snippets
            # we must return the original text
            return '{{#cg}}' + text + '{{/cg}}'

    result = render(code)
    return result

def process(current_table, template, output_file, install_file, action, verbose):

    global table 
    table = current_table

    if (verbose):
        print('processing', table, template, output_file, install_file, action)

    dict = {
       'class': cg_class(table),
        'element': cg_element(table),
        'table': table,
        'url': cg_url(table),
        'words': cg_to_words(table),
        'primary_key': cg_primary_key(table),
        'cg': cg
    }

    res = ""
    with open(template, 'r') as f: 
        res = chevron.render(f, dict).replace("\}\}", "}}").replace("\{\{", "{{")

    if (output_file):
        with open(output_file, 'w') as f:
            f.write(res)
        if (verbose):
            print(f"file {output_file} generated")
            
    if (action == 'generate'):
        print(res)
        exit(0)

    if (install_file):
        if (not os.path.exists(install_file)):
            print("copying", output_file, "to", install_file)
            shutil.copyfile(output_file, install_file)
            print(f"file {install_file} did not exist, it has been created")

    if (action == 'compare'):
        if (not filecmp.cmp(output_file, install_file)):
            comparator = 'WinMergeU'        # It must be in the PATH
            cmd = comparator + ' ' + output_file + ' ' + install_file
            print(cmd)
            os.system(cmd)
        else:
            print("no differences for", table, os.path.basename(template))

    if (action == 'install'):
        shutil.copyfile(output_file, install_file)
        print(f"file {install_file} has been replaced")

    if (action == 'check'):
        if (not filecmp.cmp(output_file, install_file)):
            # print(f"file {output_file} is different from {install_file}")
            print("differences for", table, os.path.basename(template))
        else:
            if (verbose):
                print(f"file {output_file} is the same as {install_file}")