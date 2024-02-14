# ddd-gen

Data Driven Development code generator

This is a set of tools to extract information from a MySql database schema in order to generate code to access the database.
It is the third version of this tool, the initial one was embedeed inside a PHP project and dynamically invoked during every request. The second one was written in PHP into a Laravel project. Hpwever this tool deserve its own project as it can be used in many different situations and projects.

The database schema is completed by metadata encoded as json inside the database table and field comments.

The extanded schema description is analyzed by the tools and are used to generate code using a templating mechanism.

There are several layers in this design
* the metadata layer extract information from the database schema and comment additional description
* the generator layer uses the metadata to generate snippets. The generator can be used to creade HTML code, Laravel views, React components, etc.
* the templating mechanism is used to insert the code snippets in code templates. This tool can generate code, compare the generated code with pre-existing code and install the generated code into output directories. The tool can process one or several templates and the destination directory can be specified for every template in order to populate project directories.

## The snippets generator

named snippet.py or snp.py it connect to an existing MySql database to extract information and generate code snippets.

  snp --code-gen Laravel --user john --password xxxx --database my-db --table my-table --field first-field  --snippet cell | input | update | rule

the output can be cut and pasted to be manually inserted into source files.

## The template

cg --template laravel.mst --user john --password xxxx --database my-db --output
