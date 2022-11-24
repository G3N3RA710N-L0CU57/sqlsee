#!/bin/python3
import argparse
import urllib.request
import urllib.parse
import gzip

###### HTTP request ######

class HTTPrequest():
    """ Sends HTTP request and retrieves response. """

    def __init__(self, url, header, data=None):
        self.url = url
        self.header = self._format_header(header)
        self.data = data
        self.response = None


    def send_request(self, evil_url):
        """ Send HTTP request and decompress response if gzip compressed. """
        self.evil_url = urllib.parse.quote_plus(evil_url)
        self.request = urllib.request.Request(self.url, self.data, self.header)
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



###### Injection base class ######

class BaseInjection(HTTPrequest):

    def __init__(self, url, header, data=None):
        super().__init__(url, header, data)

    def get_version(self):
        pass

    def get_column_num(self):
        pass

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


###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x:port/path")
parser.add_argument("-H", "--header", help="Header values in comma seperated list. See README for formatting. ex. Host: x.x.x.x, Accept: text/html")


###### Main function ######
def main():
    args = parser.parse_args()
    test_obj = MariaDB(url=args.url, header=args.header)
    test_obj.send_request(args.url)
    print(test_obj.get_response())

if __name__ == "__main__":
    main()
