from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import simplejson
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
        prefs = {"media.autoplay.enabled" : False,
                    "profile.managed_default_content_settings.images": 2,
                    "network.proxy.autoconfig_url.include_path" : True
                }
        options.add_experimental_option("prefs", prefs)
        chrome_driver = webdriver.Chrome(options)
        return chrome_driver

    def get_element_by(self, by, element):
        return self.driver.find_element(by, element)

    def get_elements_by_element(self, by, element):
        return self.driver.find_elements(by, element)

    def get_businesses_data_from_yellowpage(self):
        elements_web = self.get_elements_by_element(By.CLASS_NAME, 'web')
        data_company = [{}]
        for web in elements_web:
            url = web.get_attribute('href')
            try:
                ancestor_div = web.find_element(By.XPATH, "ancestor::*[@class='listado-item item-ip']")
            except NoSuchElementException:
                pass
            company_name, activity,  province = self.get_data_from_company(ancestor_div)
            if url:
                data_company.append({'url': url, 'name': company_name, 'activity': activity, 'province': province})
        return data_company

    def get_data_from_company(self, ancestor_div):
        dictionary = ancestor_div.get_attribute('data-analytics')
        data_analistic = simplejson.loads(dictionary)
        company_name = data_analistic.get('name')
        activity = data_analistic.get('activity')
        province = data_analistic.get('province')
        return  company_name, activity,  province

    def get_emails_from_urls(self, data_companys=[{}])->list:
        for i in range(len(data_companys)):
            company = data_companys[i]
            if company:
                url = company['url']
                company['email'] = self.get_email_and_companyName_from_url(url, i)
                data_companys[i] = company
        return data_companys

    def get_email_and_companyName_from_url(self, url, i):
        email=""
        try:
            wait = self.open_new_tab(subName = i)
            self.driver.get(url)
            wait.until(EC.url_to_be(url))
            page_source = self.driver.page_source
            email = list( dict.fromkeys( re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_source)))
        except Exception as e:
            print("Error open: "+url+". ")
        return email

    def open_new_tab(self, subName):
        self.driver.execute_script("window.open('about:blank', 'tab"+str(subName)+"');")
        self.driver.switch_to.window("tab"+str(subName)+"")
        wait = WebDriverWait(self.driver, 10)
        return wait