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
        self.response = None


    def send_request(self, payload):
        """ Send HTTP request and decompress response if gzip compressed. """
        self.payload = self._encode_url(payload)
        self.request = urllib.request.Request(self.payload, self.data, self.header)
        with urllib.request.urlopen(self.request) as response:
            self.response = response.read()
            # Check if gzip compressed.
            if self.response[0:2] == b'\x1f\x8b':
                self.response = gzip.decompress(self.response)

    def get_response(self):
        """ Return HTTP response. """
        return self.response

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
        self.payload_parts = urllib.parse.urlparse(payload)
        self.path = self.payload_parts.path
        self.params = self.payload_parts.params
        self.query = self.payload_parts.query
        self.path_encoded = urllib.parse.quote(self.path)
        self.params_encoded = urllib.parse.quote(self.params)
        self.query_encoded = urllib.parse.quote(self.query)
        self.payload_encoded = self.payload_parts._replace(path=self.path_encoded)
        self.payload_encoded = self.payload_parts._replace(params=self.params_encoded)
        self.payload_encoded = self.payload_parts._replace(query=self.query_encoded)
        print(self.payload_encoded.geturl())
        return self.payload_encoded.geturl()

###### Injection base class ######

class BaseInjection(HTTPrequest):

    def __init__(self, url, header, data=None):
        super().__init__(url, header, data)

    def get_version(self):
        pass

    def get_column_num(self):
        pass

    def get_database_num(self, query):
        for i in range(0, 50):
            self.payload = self.url + query
            time_start = time.time()
            self.send_request(self.payload.format(i))
            time_finish = time.time()
            total_time = time_finish - time_start
            print(total_time)

    def get_databases(self):
        pass

    def get_table_names(self):
        pass

    def get_table_columns(self):
        pass


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

###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x:port/path")
parser.add_argument("-H", "--header", help="Header values in comma seperated list. See README for formatting. ex. Host: x.x.x.x, Accept: text/html")


###### Main function ######
def main():
    args = parser.parse_args()
    test_obj = MariaDB(url=args.url, header=args.header)
    test_obj.get_database_num()

if __name__ == "__main__":
    main()
