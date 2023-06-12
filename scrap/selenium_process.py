from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from tools.cvs_process import Csv_data_access
import re

class Selenium_process:
    def __init__(self, url):
        self.driver = self.__load_chrome_driver(url)

    def __load_chrome_driver(self, url):
        chrome_driver = self.__set_chrome_options()
        chrome_driver.get(url)
        chrome_driver.implicitly_wait(10)
        return chrome_driver

    def __set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        chrome_driver = webdriver.Chrome(options)
        return chrome_driver

    def get_element_by(self, by, element):
        return self.driver.find_element(by, element)

    def get_elements_by(self, by, element):
        return self.driver.find_elements(by, element)

    def get_businesses_url_from_page(self):
        elements = self.get_elements_by(By.CLASS_NAME, 'web')
        refs = []
        for element in elements:
            ref = element.get_attribute('href')
            if ref:
                refs.append(ref)
        return refs

    def get_emails_from_urls(self, refs):
        i=0
        emails=[]
        for ref in refs:
            emails += self.get_email_from_url(ref, i)
            i+=1
        return emails

    def get_email_from_url(self, ref, i):
        email=""
        try:
            self.driver.execute_script("window.open('about:blank', 'tab"+str(i)+"');")
            self.driver.switch_to.window("tab"+str(i)+"")
            wait = WebDriverWait(self.driver, 10)
            self.driver.get(ref)
            wait.until(EC.url_to_be(ref))
            page_source = self.driver.page_source
            email = list( dict.fromkeys( re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_source)))
            if email:
                csv_file = Csv_data_access('GFG.csv')
                csv_file.Write_rows(list(email))
        except Exception as e:
            print("Error open: "+ref+". ")
        return email