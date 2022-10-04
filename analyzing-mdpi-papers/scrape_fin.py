from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import concurrent.futures
import time

#import identifiers
identifiers = pd.read_csv('/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/identifiers.csv')
identifiers = list(identifiers["identifier"])

# Scrape in parallel

#Set max_threads to 30
MAX_THREADS = 30

#Define function to go to paper website, get pub infos and write to .txt
def download(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, "html.parser")
    history = soup.find("div", {"class":'pubhistory'})
    history = re.findall('style="display: inline-block">(.*)</span>', str(history))
    history = str(history)
    with open('/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/pubhistory.txt', "a") as f:
        f.write(link + ':' + history)
    time.sleep(0.25)

#Define function to scrape in parallel
def download_info(URLs):
    threads = min(MAX_THREADS, len(URLs))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download, URLs)        

#Integrate above functions in main function that also prints information on how long this takes
def main(URLs):  
    t0 = time.time()
    download_info(URLs)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(URLs)} URLs.")

#Scrape papers! Warning: this takes about a day. Proceed in batches if you don't want to let it run for so long
#e.g., do identifiers[1:1001], then identifiers[1001:2001] etc.
main(identifiers[:1001])