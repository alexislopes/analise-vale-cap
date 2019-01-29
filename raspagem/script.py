from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import json

NUMERO = 0
CERTIFICADO = 1
NOME = 2
ENDERECO = 3
BAIRRO = 4
CIDADE = 5
PONTODEVENDA = 6

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

carregarMais = driver.find_element_by_xpath(
    '//*[@id="post-183"]/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/a')
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

time.sleep(2)

ir = driver.find_element_by_xpath('//*[@id="calendarSelectDate"]/div/div/div/div/div/div/button')
ir.click()

time.sleep(5)

response = driver.execute_script('return document.documentElement.outerHTML')
htmlBS = BeautifulSoup(response, 'html.parser')

driver.quit()

# Arrumar
data = htmlBS.find('span', class_='pull-left dateTitle').text

listaDeSorteios = htmlBS.findAll('div', class_='row row-buffer10 sorteioItem')


def limpa(string):
    palavra = str(string)

    if palavra.startswith('Nome:'):
        palavra = palavra.replace("Nome:", "")

    elif palavra.startswith('End.:'):
        palavra = palavra.replace('End.:', "")

    else:
        palavra = palavra.replace('Bairro:', "")

    return palavra.strip()


def criacsv():
    arquivo = open('{}.csv'.format(data), "w")
    return arquivo


def criajsonarq(nome):
    arquivo = open('../datasets/{}.json'.format(nome), 'w')
    return arquivo


print('\tSORTEIO DO DIA {}\n'.format(data))

for i in range(int(len(listaDeSorteios) / 2 - 1)):

    dezenas = []

    sorteio = listaDeSorteios[i]
    numeroDoPremio = sorteio.h4.text
    premio = sorteio.find('div', class_='row row-bufferTop10').div.p.text
    dezenasSorteadas = sorteio.findAll('span', class_='numberDicker pull-left')
    contemplados = sorteio.findAll('div', class_='col-md-6 col-sm-6 col-xs-12 contemplated')

    print('\n**********************************************************************************\n')
    # print(numeroDoPremio)
    # print(premio)
    for i in range(len(dezenasSorteadas)):
        dezenas.append(dezenasSorteadas[i].text)
    # print('Dezenas Soreteadas: ', dezenas)

    for k in range(len(contemplados)):
        informacoes = contemplados[k].ul.findAll('li')
        numero = informacoes[NUMERO].text
        certificado = informacoes[CERTIFICADO].strong.text
        nome = limpa(informacoes[NOME].text)
        endereco = limpa(informacoes[ENDERECO].text)
        bairro = limpa(informacoes[BAIRRO].text)
        cidade = informacoes[CIDADE].strong.text
        pontoDeVenda = informacoes[PONTODEVENDA].strong.text
        strDezenas = ' '.join(e for e in dezenas)

        # print("Contemplado Número: {}\nCertificado: {}\nNome: {}\nEndereço: {}\nBairro: {}\nCidade: {}\nPonto de venda: {}\n"
        # .format(numero, certificado, limpa(nome), limpa(endereco), limpa(bairro), cidade, pontoDeVenda))

        # df = pd.DataFrame(

        sorteio = {
            "Data": data,
            "NumeroDoPremio": numeroDoPremio,
            "Premio": premio,
            "Dezenas": dezenas,
            "Contemplado": {
                "Numero": numero,
                "Certificado": certificado,
                "Nome": nome,
                "Endereço": endereco,
                "Bairro": bairro,
                "Cidade": cidade,
                "PontoDeVenda": pontoDeVenda
            }
        }
        # index=[1,2,3,4,5,6,7,8,9,10]
        # )

        # df.reset_index()

        # df.to_csv(path_or_buf=arquivo)

        serilaized = json.dumps(sorteio, indent=3, ensure_ascii=False)
        jsonarq = criajsonarq('boom')
        jsonarq.write(serilaized)

jsonarq.close()
