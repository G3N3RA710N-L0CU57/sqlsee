#!/bin/python3
import argparse


###### HTTP request ######
class HTTPrequest():

        def __init__(self, url, header):
                self.url = url
                self.header = header


        def send_request(self):
                pass

        def get_response(self):
                pass


###### Command line parser ######
parser = argparse.ArgumentParser()

parser.add_argument("url", help="url of target in format http://x.x.x.x")
parser.add_argument("-H", "--header", help="header values in comma seperated list ex. Host: x.x.x.x, Accept: text/html")
parser.add_argument("-rF", "--request-file", help="request in the form of a .txt file ex. -rF request.txt")

###### Main function ######
def main():
        args = parser.parse_args()
        print(args.url)
        print(args.header)

if __name__ == "__main__":
        main()
