from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from numpy.lib.user_array import container
from scrapy.utils import job


def scrapper(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    url = 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=1&pageNum=0'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup


def main_scraper(soup):
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card' )
    for item in jobs:
        title = item.find('a').text.strip()
        company = item.find('h4').text.strip()
        link = item.a['href']
        location = item.find('span', class_='job-search-card__location').text.strip()
        job_posted = item.find('time',class_='job-search-card__listdate')
        if job_posted is not None:
            time = job_posted.text.strip()
            job = {
                'Title':title,
                'Link': link,
                'Company': company,
                'Location': location,
                'Job_posted' : time,
            }
            joblist.append(job)
    return
joblist = []
page = int(input(f'Enter the  page number you are looking for:'))
for i in range(0,100,20):
    print(f'Getting Page, {i}')
    c = scrapper(page)
    main_scraper(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('Linkedin_job_list.csv')
