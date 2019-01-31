from selenium import webdriver

def getDriver():
    driver = webdriver.Firefox()
    url = 'http://valecaperegiao.com.br/resultados/'
    return driver.get(url)

def closeDriver():
    return getDriver().close()
