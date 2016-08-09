__author__ = 'zbb0263'

import urllib.request
from bs4 import BeautifulSoup
import os
import sys

def check_IP(URL, File):
  #URL = "http://checkip.dyndns.org/"
  #File = "C:\\Users\\Owner\\Desktop\\temp\\currentIP.txt"
  
  with urllib.request.urlopen(URL) as response:
    html = response.read()
    soup = BeautifulSoup(html)
    text = soup.get_text()
    currentIP = text[36:]
    if os.path.isfile(File):
      with open(File, 'rt') as IPFile:
        if currentIP != IPFile.read():
          with open(File, 'w') as IPFile:
            IPFile.write(currentIP)
    else:
      with open(File, 'w') as IPFile:
        IPFile.write(currentIP)

def main():
  if len(sys.argv) != 3:
    print('usage: ./currentIP.py url file')
    sys.exit(1)
  url = sys.argv[1]
  filename = sys.argv[2]
  check_IP(url, filename)


if __name__ == '__main__':
  main()