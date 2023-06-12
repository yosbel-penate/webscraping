from scrap.selenium_process import Selenium_process

url = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'

selenium_driver = Selenium_process(url)

refs = selenium_driver.get_businesses_url_from_page()
print(refs)

emails = selenium_driver.get_emails_from_urls(refs)
print(emails)
