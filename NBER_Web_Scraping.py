from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

# Preparing for chromedriver for browsing on NBER web site
executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://admin.nber.org/xsearch?q=early+childhood+development+OR+Education&whichsearch=ftpub&restrict_papers=yes&fullresults=1&datefilter=&b=search+again"
browser.visit(url)

# Scraping the most recent 5 pages
for i in range(0, 5):
    try:
        html = browser.html
        page_soup = BeautifulSoup(html, 'html.parser')
        
        # results are returned as an iterable list
        headers = soup.find_all('a', class_="resultTitle")
        title.append(headers)
        date = soup.find_all('span', class_='searchResultNiceDate')
        authors = soup.find_all('span', class_='searchResultAuthor')
        abstract = soup.find_all('div', class_='searchResultAbstract')
        link_path = soup.find_all('p', class_='url')
        
        # Create a random timer for the click action
        t = random.randint(5, 15)
        
        browser.is_element_present_by_text('More results', wait_time=t)
        browser.click_link_by_text('More results.')
    except AttributeError as e:
        print(e)  