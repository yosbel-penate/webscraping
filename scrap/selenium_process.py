import re
import simplejson
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC

class SeleniumProcess:
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
        options.add_argument("--disable-extensions")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        prefs = {
                    "media.autoplay.enabled" : False,
                    "profile.managed_default_content_settings.images": 2,
                    "network.proxy.autoconfig_url.include_path" : True,
                    'profile.default_content_setting_values': {
                        'cookies': 2,
                        'images': 2,
                        'javascript': 2,
                        'plugins': 2,
                        'popups': 2,
                        'geolocation': 2,
                        'notifications': 2,
                        'auto_select_certificate': 2,
                        'fullscreen': 2,
                        'mouselock': 2,
                        'mixed_script': 2,
                        'media_stream': 2,
                        'media_stream_mic': 2,
                        'media_stream_camera': 2,
                        'protocol_handlers': 2,
                        'ppapi_broker': 2,
                        'automatic_downloads': 2,
                        'midi_sysex': 2,
                        'push_messaging': 2,
                        'ssl_cert_decisions': 2,
                        'metro_switch_to_desktop': 2,
                        'protected_media_identifier': 2,
                        'app_banner': 2,
                        'site_engagement': 2,
                        'durable_storage': 2,
                    }
                }
        options.add_experimental_option("prefs", prefs)
        chrome_driver = webdriver.Chrome(options)
        return chrome_driver

    def get_businesses_data_from_yellowpage(self):
        elements_web = self.driver.find_elements(By.CLASS_NAME, 'web')
        data_company = []
        for web in elements_web:
            url = web.get_attribute('href')
            try:
                ancestor_div = web.find_element(By.XPATH,
                                    "ancestor::*[@class='listado-item item-ip']"
                                )
            except NoSuchElementException:
                pass
            except WebDriverException:
                pass
            company_name, activity,  province = self.get_data_from_company(ancestor_div)
            if url:
                data_company.append({
                    'url': url,
                    'name': company_name,
                    'activity': activity,
                    'province': province
                })
        return data_company

    def get_data_from_company(self, ancestor_div: WebElement) -> tuple:
        dictionary = ancestor_div.get_attribute('data-analytics')
        data_analistic = simplejson.loads(dictionary)
        company_name = data_analistic.get('name')
        activity = data_analistic.get('activity')
        province = data_analistic.get('province')
        return  company_name, activity,  province

    def get_emails_from_urls(self, data_companys:list[dict]) -> list:
        for i, data_company in enumerate(data_companys):
            company = data_company
            if company:
                url = company['url']
                company['email'] = self.get_email_and_company_name_from_url(url, i)
                data_companys[i] = company
        return data_companys

    def get_email_and_company_name_from_url(self, url, i):
        email=list
        try:
            wait = self.open_new_tab(sub_name = i)
            self.driver.get(url)
            wait.until(EC.url_to_be(url))
            page_source = self.driver.page_source
            email = list(
                dict.fromkeys(
                    re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
                    page_source
                )))
        except Exception as error:
            print("Error open: "+url+". ", error)
        return email

    def open_new_tab(self, sub_name:int) -> WebDriverWait:
        self.driver.execute_script("window.open('about:blank', 'tab"+str(sub_name)+"');")
        self.driver.switch_to.window("tab"+str(sub_name)+"")
        wait = WebDriverWait(self.driver, 10)
        return wait
