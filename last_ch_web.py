

import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import zipfile
import io
import re

def urls_extractor(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    aa = soup.find_all('a',href=True)
    all_decorations = [decoration for decoration in aa if 'colored' in decoration['href']]
    last_chapter = int(all_decorations[1].text)







urls_extractor("https://mangaberri.com/one-piece-colored-manga")