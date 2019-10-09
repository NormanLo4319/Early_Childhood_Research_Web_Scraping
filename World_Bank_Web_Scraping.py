# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# Create a loop that can navigate to the next page
report_title = []
report_summary = []
report_citation = []
report_link = []
report_publish_date = []
report_author = []

executable_path = {'executable_path': './chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://openknowledge.worldbank.org/discover'
browser.visit(url)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Loop through the first 5 pages
for j in range(0, 2250):
    titles = []

    for i in range(0, 10):
        try:
            html = browser.html
            page_soup = BeautifulSoup(html, 'html.parser')
            
            if browser.is_text_present('No, thanks.') == True:
                browser.click_link_by_text('No, thanks.')
            
            #Look for the title on the main page under 'h4' tag
            browser.is_element_present_by_css('h4')
            name = page_soup.find_all('h4')[i].text

            # Remove the new line split '\n' from the title name
            if (name):
                t = name.splitlines()
                titles.append(t[1])

            # Click on the book title link and nevigate to the report page
            browser.is_element_present_by_text(titles[i], wait_time=2)
            browser.click_link_by_text(titles[i])
                
            # Creating the BeautifulSoup parser to extract the information from the report page
            html = browser.html
            reports_soup = BeautifulSoup(html, 'html.parser')
            report = reports_soup.select_one('div.main-content')

            # Extracting the information from the report page
            title = report.find('h2', class_='ds-div-head').get_text()
            summary = report.find('div', class_='okr-item-page-field-wrapper abstract').get_text().splitlines()
            citation = report.find('div', class_='citation').get_text().splitlines()
            link_path = report.find('div', class_='okr-item-page-field-wrapper uri').get_text()
            link = link_path[4:].splitlines()
            publish_date = report.find('div', class_='simple-item-view-other word-break').get_text()
            author = report.find('div', class_='authorprofile-item-view-link').get_text().splitlines()

            # Append the information into the empty lists
            report_title.append(title)
            report_summary.append(summary[1])
            report_citation.append(citation[1])
            report_link.append(link[1])
            report_publish_date.append(publish_date)
            report_author.append(author[1])
            
            # Go back to the main page after extracting the information
            browser.back()
            # Stop the loop for 2 seconds to make sure catching the popup window
            time.sleep(2)
            
        except AttributeError as e:
            print(e)
    
    # Create a click action to navigate to the next page
    browser.is_element_present_by_css('a[class="next-page-link"]', wait_time=1)
    next_page = browser.find_by_css('a[class="next-page-link"]')
    next_page[1].click()
    time.sleep(2)

print(report_link)
print(len(report_summary))

# Take out the "Abstract" word out of summary
report_abstract = []
for i in report_summary:
    abstract = i[8:]
#     print(abstract)
    report_abstract.append(abstract)
# print(report_abstract)

# Storing the variables into a dataframe
data_df = pd.DataFrame(list(zip(report_title, report_abstract, report_link, report_publish_date, report_author)), 
                       columns=["title", "summary", "link", "publish_date", "author"])

# Saving the dataframe into CSV
data_df.to_csv("data.csv", index=False, encoding='utf-8')