from scrap.selenium_process import SeleniumProcess
from tools.cvs_process import CsvDataAccess

URL = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'

def get_paginators(URL):
    try:
        driver = SeleniumProcess( URL)
        pages = driver.get_paginations()
    finally:
        driver.quit_driver()
    return pages

paginations_list = get_paginators(URL)
paginations_list[0] = URL

for url in paginations_list:
    try:
        company_data=[]
        company_data_and_emails=[]
        selenium_driver = SeleniumProcess( url)
        company_data = selenium_driver.get_businesses_data_from_yellowpage()
        company_data_and_emails = selenium_driver.get_emails_from_urls(company_data)
        CsvDataAccess.safe_in_csv(company_data_and_emails)
    finally:
        selenium_driver.quit_driver()
