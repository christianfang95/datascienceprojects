from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import concurrent.futures
import time
import csv
import random

#import identifiers
identifiers = pd.read_csv('/Users/christianfang/GitHub/analyzing-mdpi-papers/data/identifiers.csv')
URLs = identifiers["identifier"].to_list()
URLs = [item.replace('"', '') for item in URLs]


# Scrape in parallel

#Set max_threads to 30
MAX_THREADS = 30

#define fake user agents
user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

#Define function to go to paper website, get pub infos and write to .csv
def download(link):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, "html.parser")
    history = soup.find("div", {"class":'pubhistory'})
    history = re.findall('style="display: inline-block">(.*)</span>', str(history))
    history = str(history)
    with open('/Users/christianfang/GitHub/analyzing-mdpi-papers/data/pubhistory_test.csv', "a", newline='') as f:
     writer = csv.writer(f, delimiter = ',')
     writer.writerow([link, history])
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
    print(f"{t1-t0} seconds to scrape {len(URLs)} URLs.")

#Scrape papers! Warning: this takes about a day. Proceed in batches if you don't want to let it run for so long
#e.g., do identifiers[1:1001], then identifiers[1001:2001] etc.
main(URLs[300200:302200])



#ident = str(identifiers[5])

#
#resp = requests.get(URLs[1])
#soup = BeautifulSoup(resp.content, "html.parser")
#history = soup.find("div", {"class":'pubhistory'})
#history = re.findall('style="display: inline-block">(.*)</span>', str(history))
#history = str(history)
#with open('/Users/christianfang/GitHub/analyzing-mdpi-papers/data/pubhistory_test.csv', "a", newline='') as f:
#     writer = csv.writer(f, delimiter = ',')
#     writer.writerow([link, history])


imp = pd.read_csv('/Users/christianfang/GitHub/analyzing-mdpi-papers/data/pubhistory_test.txt', header = None)