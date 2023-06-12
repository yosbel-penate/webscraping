from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tools.get_element_from_page import get_elements_by
from selenium.webdriver.common.by import By
from scrap.load_web import load_web
import re

url = 'https://www.paginasamarillas.es/search/carpinteria/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=carpinteria&qc=true'
driver = load_web(url)

def get_businesses_url_from_page(driver):
    elements = get_elements_by( driver, By.CLASS_NAME, 'web')
    refs = []
    for element in elements:
        ref = element.get_attribute('href')
        if ref:
            refs.append(ref)
    return refs

refs = get_businesses_url_from_page(driver)
print(refs)

def get_emails_from_urls(driver, refs):
    i=0
    emails=[]
    for ref in refs:
        try:
            driver.execute_script("window.open('about:blank', 'tab"+str(i)+"');")
            driver.switch_to.window("tab"+str(i)+"")
            wait = WebDriverWait(driver, 10)
            driver.get(ref)
            wait.until(EC.url_to_be(ref))
            page_source = driver.page_source
            emails+=list( dict.fromkeys( re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", page_source)))
            i+=1
        except Exception as e:
            print("Error open: "+ref)
        return emails

emails = get_emails_from_urls(driver, refs)
print(emails)