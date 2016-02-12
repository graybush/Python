__author__ = 'zbb0263'

import urllib.request
from bs4 import BeautifulSoup

URL = "http://checkip.dyndns.org/"
File = "C:\\Users\\Owner\\Dropbox\\CurrentIP\\currentIP.txt"

with urllib.request.urlopen(URL) as response:
    html = response.read()
    soup = BeautifulSoup(html)
    text = soup.get_text()
    currentIP = text[36:]
    with open(File, 'rt') as IPFile:
        storedIP = IPFile.read()
    if currentIP != storedIP:
        with open(File, 'w') as IPFile:
            IPFile.write(currentIP)