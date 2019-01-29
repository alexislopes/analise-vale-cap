#Este sceript simula a navegação na página de resultados até o dia de sorteio desejado, no caso: 29/07/2018.

from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

response = driver.execute_script('return document.documentElement.outerHTML')
htmlBS = BeautifulSoup(response, 'html.parser')

carregarMais = driver.find_element_by_xpath('//*[@id="post-183"]/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/a')
carregarMais.click()

time.sleep(2)

carregarMais.click()

datepicker = driver.find_element_by_xpath('//*[@id="search-date-input"]')
datepicker.click()

prev = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[1]')
for i in range(6):
    prev.click()
    time.sleep(1)

dia = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/tbody/tr[6]/td[1]')
dia.click()

driver.execute_script("scrollBy(0,-500);")

time.sleep(5)

ir = driver.find_element_by_xpath('//*[@id="calendarSelectDate"]/div/div/div/div/div/div/button')
ir.click()

driver.quit()