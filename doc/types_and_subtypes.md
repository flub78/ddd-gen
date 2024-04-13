# Types ans subtypes


Here is a list of the most command data types and subtypes

Foreign keys are also use to generate code.

## Types
bigint
boolean
char        fix size string
enum
date
datetime    
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
boolean
color
csv_int
csv_string
currency         {"subtype": "currency", "currency": "euro"}
date
datetime        from '1000-01-01 00:00:00' to '9999-12-31 23:59:59'
decimal
double
email

enum
file
float
foreign_key
image
integer
json
password
password_confirmation
string

text
time            from '-838:59:59' to '838:59:59'
timestamp       number of seconds since the Unix epoch ('1970-01-01 00:00:00' UTC)
set
url   


## Currency

Using decimal for currency guarantee no rounding errors during storage. But it may be as simple to manage floats with a sufficient precision....all depends on how numbers are manage in the application. Are computations done by the database or the application layer ?

## foreign_key

Foreign keys reference a column in another table.
They are choosen from a list of possible values. Values are displayed as humman readable string.

Note that selectors can be unique ( a single string) or multiple (a date, a name, a type, etc.)
