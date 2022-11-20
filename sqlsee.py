#!/bin/python3
import argparse
import urllib


###### HTTP request ######
class HTTPrequest():

    def __init__(self, url, header, data=None):
        self.url = url
        self.header = self._format_header(header)
        self.data = data
        #self.request = urllib.request.Request(self.url, self.data, self.header)


    def send_request(self):
        pass

    def get_response(self):
        pass

    def _format_header(self, header):
        self.header_list = header.split(", ")
        self.header_dict = dict()
        for i in range(len(self.header_list)):
            self.header_list[i] = self.header_list[i].strip()
            self.header_seperate = self.header_list[i].split(": ")
            self.header_dict[self.header_seperate[0]] = self.header_seperate[1]

        print(self.header_dict)

        return self.header_dict

###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x")
parser.add_argument("-H", "--header", help="header values in comma seperated list ex. Host: x.x.x.x, Accept: text/html")
parser.add_argument("-rF", "--request-file", help="request in the form of a .txt file ex. -rF request.txt")

###### Main function ######
def main():
    args = parser.parse_args()
    url_obj = HTTPrequest(args.url, args.header)

if __name__ == "__main__":
    main()
