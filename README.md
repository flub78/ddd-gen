# ddd-gen

Data Driven Development code generator

This is a set of command line tools to extract information from a MySql database schema to generate code to access the database.
It is the third version of this tool, the initial one was embedeed inside a PHP project and dynamically invoked during every request. The second one was written in PHP as laravel artisan commands. However this tool deserves its own project as it can be used in many different situations and projects.

## The Metadata layer

The database schema is completed by metadata encoded as json inside the database table and field comments. The idea is to extract type from the database schema (e.g. string, integer, float). And to extract subtypes from the metadata description, for exemple string can have subtypes like email, encrypted password, address, phone number. Attributes like ranges, possible values, etc. can be extracted from the schema and the metadata.

The extanded schema description is analyzed by the tools and used to generate code.

There are several layers in this design
* the metadata layer extract information from the database schema and comment additional description

* the generator layer uses the metadata to generate snippets. The generator can be used to creade HTML code, Laravel views, React components, etc. Output of the generator can be pasted into source files.

* the templating mechanism is used to insert the code snippets into templates. This tool can generate code, compare the generated code with pre-existing one and install it into output directories. The tool can process one or several templates and the destination directory can be specified for every template to populate project directories.

## The snippets generator

The code generator layer.

named snippet.py or snp.py it connect to an existing MySql database to extract information and generate code snippets.

  snp --code-gen Laravel --user john --password xxxx --database my-db --table my-table --field first-field  --snippet cell | input | update | rule

the output can be cut and pasted to be manually inserted into source files.

## The template mechanism

cg --template laravel.mst --user john --password xxxx --database my-db --output

