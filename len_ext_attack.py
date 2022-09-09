#!/usr/bin/python3

# Run me like this:
# $ python3 len_ext_attack.py "https://project1.eecs388.org/uniqname/lengthextension/api?token=...."
# or select "Length Extension" from the VS Code debugger

import sys
from urllib.parse import quote
from pymd5 import md5, padding


class URL:
    def __init__(self, url: str):
        # prefix is the slice of the URL from "https://" to "token=", inclusive.
        self.prefix = url[:url.find('=') + 1]
        self.token = url[url.find('=') + 1:url.find('&')]
        # suffix starts at the first "command=" and goes to the end of the URL
        self.suffix = url[url.find('&') + 1:]

    def __str__(self) -> str:
        return f'{self.prefix}{self.token}&{self.suffix}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self).__repr__()})'


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND", file=sys.stderr)
        sys.exit(-1)

    url = URL(sys.argv[1])

    #
    # TODO: Modify the URL
    #
    modm = quote(url.suffix)
    modmlen = len(modm) + 8     #add 8 for the 8 byte password at the beginning
    bits = (modmlen + len(padding(modmlen*8)))*8    #account for padding length in original and convert to bits
    h = md5(state = bytes.fromhex(url.token), count = bits)     #update md5 using token and length
    x = '&command=UnlockSafes'
    modx = quote(x)

    #MANUALLY ADD PADDING
   # h.update(padding(modmlen*8))

    h.update(x) #update md5

    #h.update(padding(len(modx*8)))

    url.token = h.hexdigest()
    url.suffix += quote(padding((len(url.suffix) + 8)*8)) + x
    print(url)



    #Restarting above
    #print("url token= ",url.token)
    #print("url suffix= ",url.suffix)
    #print("len(url.suffix)= ",len(url.suffix))
   # print("quoted suffix= ", quote(url.suffix))
   # print(quote('&command=UnlockSafes'))


if __name__ == '__main__':
    main()
