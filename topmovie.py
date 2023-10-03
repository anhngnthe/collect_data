# Import libraries and packages for the project 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions  
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import csv

print('- Finish importing packages')

# Open Chrome and Access website
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
sleep(2)
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
driver.get(url)
print('- Finish initializing a driver')
sleep(2)

# Write a function to extract the URLs of one page
def GetURL():
    page_source = BeautifulSoup(driver.page_source)
    profiles = page_source.find_all('td', class_ = 'titleColumn')
    result = []
    for a in profiles:
        result.extend(a.find_all('a'))
    all_profile_URL = []
    for profile in result:
        profile_ID = profile.get('href')
        profile_URL = "https://www.imdb.com/" + profile_ID
        if profile_URL not in all_profile_URL:
            all_profile_URL.append(profile_URL)
    return all_profile_URL

URLs = GetURL()
print('- Finish Scrape the URLs')

# Scrape the data, and write the data to a .CSV file
with open('movies.csv', 'w',  newline = '') as file_output:
    headers = ['movie_id', 'name', 'year_release', 'rating', 'duration', 'director']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    movie_id = 0
    for movie_URL in URLs[:100]:
        driver.get(movie_URL)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        movie_id = movie_id + 1
        info_div = page_source.find('ul',{'class':'ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt'})
        info_loc = info_div.find_all('li')
        name = page_source.find('span',{'class':'sc-afe43def-1 fDTGTb'}).get_text().strip()
        year_release = info_loc[0].find('a',{'class':'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text().strip()
        rating = page_source.find('span',{'class':'sc-bde20123-1 iZlgcd'}).get_text().strip()
        duration = info_loc[2].get_text().strip()
        director = page_source.find('a',{'class':'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'}).get_text().strip()
        writer.writerow({headers[0]:movie_id, headers[1]:name, headers[2]:year_release, headers[3]:rating, headers[4]:duration, headers[5]:director})

print('Mission Completed!')