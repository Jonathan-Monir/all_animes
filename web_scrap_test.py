
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import re

def urls_extractor(url, first, last):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    aa = soup.find_all('a',href=True)

    all_decorations = [decoration for decoration in aa if 'colored' in decoration['href']]

    first = 437 - (first - 1)
    last = 437 - (last - 1)

    pages = list(range(last, first+1))
    pages_url = [all_decorations[page]['href'] for page in pages]

    return pages_url





urls_extractor("https://mangaberri.com/one-piece-colored-manga",first=218,last=219)