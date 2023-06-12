
def get_element_by(driver, by, element):
    return driver.find_element(by, element)

def get_elements_by(driver, by, element):
    return driver.find_elements(by, element)