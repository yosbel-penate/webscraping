from scrap.selenium_process import Selenium_process
from tools.cvs_process import Csv_data_access

url = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'

selenium_driver = Selenium_process(url)

refs = selenium_driver.get_businesses_url_from_page()
print(refs)

emails = selenium_driver.get_emails_from_urls(refs)
print(emails)

if emails:
    csv_file = Csv_data_access('GFG.csv')
    for row in emails:
        csv_file.Write_row({'company': 'none', 'emails': row})
