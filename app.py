from scrap.selenium_process import Selenium_process
from tools.cvs_process import Csv_data_access

url = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'

selenium_driver = Selenium_process(url)

company_data = selenium_driver.get_businesses_data_from_yellowpage()
print(company_data)

company_data_and_emails = selenium_driver.get_emails_from_urls(company_data)
print(company_data_and_emails)

if company_data_and_emails:
    csv_file = Csv_data_access('GFG.csv')
    for row in company_data_and_emails:
        if bool(row):
            csv_file.Write_row(row)
