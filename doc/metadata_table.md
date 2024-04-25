# Metadata table

Initially I decided to implement the metadata as json comments inside the database table and column comments.

The justification for that was to keep all the information describing the data in the same place. As part of this information is extracted form the database schema it was making sense to keep every source of information in the same place; the database sructure.

However it is not so convenient, every update of the metadata implies to erase, recreate and reseed the database. The current development state erased and that even for the most trivial modification.

Something a little more flexible is to use a special table in the database.

It is possible to modify it on the fly and the seed procedure can be generated from the table itself. https://github.com/orangehill/iseed


## Metadata structure

table metadata
* id
* table
* column
* key
* value

column can be null to manage metadata at the table level.

table could also be null in case I need global metadata not attached to anything (to be confirmed)

value is either a scalar value or a json encoded string, in which case the key equal json.

Note that it could be a good idea to validate the fields and 
reject incorrect values for table and column. Easy to do do if I implement a Laravel API and React views on this table. It should be protected by a dev role.

## Development

    php artisan make:migration create_metadata_table
    php artisan migrate --env=testing

    meta -t boards -v






