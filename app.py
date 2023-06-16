from scrap.selenium_process import SeleniumProcess
from tools.cvs_process import CsvDataAccess

URL = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'

selenium_driver = SeleniumProcess(URL)

company_data = selenium_driver.get_businesses_data_from_yellowpage()
print(company_data)

company_data_and_emails = selenium_driver.get_emails_from_urls(company_data)
print(company_data_and_emails)

if company_data_and_emails:
    csv_file = CsvDataAccess('GFG.csv')
    for row in company_data_and_emails:
        if bool(row):
            csv_file.write_row(row)
