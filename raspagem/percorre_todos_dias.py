from bs4 import BeautifulSoup
from selenium import webdriver
import time

diasPorMes = [1, 4, 5, 4, 4 ,5, 4]
clicksPorMes = [6, 1, 2, 3, 4, 5, 6]
meses = 7

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

def abreDatePicker():
    carregarMais = driver.find_element_by_xpath(
        '//*[@id="post-183"]/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/a')
    carregarMais.click()

    time.sleep(2)

    carregarMais.click()

    datepicker = driver.find_element_by_xpath('//*[@id="search-date-input"]')
    datepicker.click()

for i in range(meses):

    abreDatePicker()

    index = 0
    if i == 0:
        prev = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[1]')
        for k in range(clicksPorMes[i]):
            time.sleep(1)
            prev.click()

    else:
        next = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[3]')
        for l in range(clicksPorMes[i]):
            time.sleep(1)
            next.click()


    if clicksPorMes[i] == 6:
        print("ClicksPorMes[i]:", clicksPorMes[i])
        index = 6
    else:
        print("ClicksPorMes[i]:", clicksPorMes[i])
        index = i + 2


    for r in range(diasPorMes[i]):
        dia = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/tbody/tr[{}]/td[1]'.format(index))
        dia.click()

        driver.execute_script("scrollBy(0,-500);")

        time.sleep(2)

        ir = driver.find_element_by_xpath('//*[@id="calendarSelectDate"]/div/div/div/div/div/div/button')
        ir.click()

        #raspa dados...

        #se tiver mais dias...
        if(r > 1):
            abreDatePicker()

    time.sleep(5)

    response = driver.execute_script('return document.documentElement.outerHTML')
    htmlBS = BeautifulSoup(response, 'html.parser')

driver.quit()