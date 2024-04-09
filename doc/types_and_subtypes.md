# Types ans subtypes


Here is a list of the most command data types and subtypes

Foreign keys are also use to generate code.

## Types
bigint
boolean
char        fix size string
enum
date
datetime    from '1000-01-01 00:00:00' to '9999-12-31 23:59:59'
decimal
double
float
int
set
text
time        from '-838:59:59' to '838:59:59'
timestamp   number of seconds since the Unix epoch ('1970-01-01 00:00:00' UTC)
varchar


## Subtypes

int.bitfield, bigint.bitfield       use rather a set
decimal.currency
    {"subtype": "currency", "currency": "euro"}
varchar.csv_int
varchar.csv_string
varchar.email
varchar.enumerate                   use rather enum
varchar.file
varchar.json
varchar.image
varchar.url


## Currency

Using decimal for currency guarantee no rounding errors during storage. But it may be as simple to manage floats with a sufficient precision....all depends on how numbers are manage in the application. Are computations done by the database or the application layer ?

## foreign_key

Foreign keys reference a column in another table.
They are choosen from a list of possible values. Values are displayed as humman readable string.

Note that selectors can be unique ( a single string) or multiple (a date, a name, a type, etc.)
