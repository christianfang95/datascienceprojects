from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
!pip install selenium
from selenium import webdriver
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0,'/Users/christianfang/Downloads/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(ChromeDriverManager().install())


#import identifiers
identifiers = pd.read_csv('/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/identifiers.csv')
identifiers = list(identifiers["identifier"])

import requests
import concurrent.futures

hist=[]
def download(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, "html.parser")
    history = soup.find("div", {"class":'pubhistory'})
    history = re.findall('style="display: inline-block">(.*)</span>', str(history))
    history = str(history)
    with open('/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/pubhistory.txt', "a") as f:
        f.write(link + ':' + history)

#
def download_info(URLs):
    for url in URLs:
        download(url)

import time

def main(URLs):
    t0 = time.time()
    download_info(URLs)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(URLs)} URLs.")


#Do only two identifiers

main(identifiers[:5])


download(identifiers[2])


####### Parallel

MAX_THREADS = 30

def download(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, "html.parser")
    history = soup.find("div", {"class":'pubhistory'})
    history = re.findall('style="display: inline-block">(.*)</span>', str(history))
    history = str(history)
    with open('/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/pubhistory.txt', "a") as f:
        f.write(link + ':' + history)
    time.sleep(0.25)

def download_info(URLs):
    threads = min(MAX_THREADS, len(URLs))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download, URLs)        


def main(URLs):  
    t0 = time.time()
    download_info(URLs)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(URLs)} URLs.")

main(identifiers[:1001])





