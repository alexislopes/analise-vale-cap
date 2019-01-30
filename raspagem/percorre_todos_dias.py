#Este script percorre desde o primeiro dia de sorteios (29/07/2018) até o último dia (27/01/2019)
#disponibilizados pelo site até o desenvolvimennto deste script.

from bs4 import BeautifulSoup
from selenium import webdriver
import time

diasPorMes = [1, 4, 5, 4, 4 ,5, 4]
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
    print('abri DatePicker\n')

#vai até o primeiro dia de sorteio que encontra-se em julho de 2018
def vaiParaJulho():
    print('Indo para Julho')
    prev = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[1]')
    for k in range(6):
        time.sleep(1)
        prev.click()

#vai para o próximo mes
def proximoMes():
    next = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[3]')
    time.sleep(1)
    next.click()
    print('fui para o próximo mês')

def pegaMesAno():
    mesano = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[2]')
    mesanostr = str(mesano).replace(" ", " de ")
    return  mesano.text.replace(" ", " de ")



abreDatePicker()
vaiParaJulho()

for i in range(meses):
    index = 0

    for r in range(diasPorMes[i]):

        if diasPorMes[i] == 1:
            index = 6
        else:
            index = r + 2

        print('O index é: \n', index)

        dia = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/tbody/tr[{}]/td[1]'.format(index))
        print('Cliquei no dia {} de {}\n'.format(dia.text, pegaMesAno()))
        dia.click()


        driver.execute_script("scrollBy(0,-500);")
        print('Scrollei\n')

        time.sleep(2)

        ir = driver.find_element_by_xpath('//*[@id="calendarSelectDate"]/div/div/div/div/div/div/button')
        ir.click()
        print('Apertei ir\n')

        #raspa dados...
        print('raspando dados...\n')

        #espera a página carregar
        time.sleep(3)

        #abre DatePicker
        abreDatePicker()


    proximoMes()
    time.sleep(5)

    response = driver.execute_script('return document.documentElement.outerHTML')
    htmlBS = BeautifulSoup(response, 'html.parser')

driver.quit()