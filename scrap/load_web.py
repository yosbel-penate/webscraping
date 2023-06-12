from scrap.init_drive import init_drive

def load_web(url):
    driver = init_drive()
    driver.get(url)
    driver.implicitly_wait(10)
    return driver