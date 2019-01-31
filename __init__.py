from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json



driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

response = driver.execute_script('return document.documentElement.outerHTML')
htmlBS = BeautifulSoup(response, 'html.parser')

diasPorMes = [1, 4, 5, 4, 4 ,5, 4]
meses = 7

diasPorMes = [1, 4, 5, 4, 4 ,5, 4]
meses = 7

index = 0

numeroDoPremioS = []
premioS = []
dezenasSorteadaS = []
numeroS = []
certificadoS = []
nomeS = []
enderecoS = []
bairroS = []
cidadeS = []
pontoDeVendaS = []

listaSorteios = []

NUMERO = 0
CERTIFICADO = 1
NOME = 2
ENDERECO = 3
BAIRRO = 4
CIDADE = 5
PONTODEVENDA = 6

data = ""
dataArq = ""

#abre o calendário para escolher o dia do sorteio desejado
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

def mesAno():
    return driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[2]').text.replace(" ", " de ")

def formataData(dia):
    dataFormatada = dia.text + " de " + mesAno()
    global data
    data = dataFormatada
    return dia.text

def formataDataToArqName(dia):
    global dataArq
    dataArq = formataData(dia).replace(" ", "_")

def pegaListaDeSorteios():
    return htmlBS.findAll('div', class_='row row-buffer10 sorteioItem')

def limpa(string):
    palavra = str(string)

    if palavra.startswith('Nome:'):
        palavra = palavra.replace("Nome:", "")

    elif palavra.startswith('End.:'):
        palavra = palavra.replace('End.:', "")

    else:
        palavra = palavra.replace('Bairro:', "")

    return palavra.strip()

def criacsv(data):
    arquivo = open('/datasets/csv/sorteio_do_dia_{}.csv'.format(data), "w")
    return arquivo


def criajsonarq(data):
    arquivo = open('/datasets/json/sorteio_do_dia_{}.json'.format(data), 'w')
    return arquivo

def raspa():
    for i in range(int(len(pegaListaDeSorteios()) / 2 - 1)):
        listaContemplados = []
        dezenas = []

        sorteio = pegaListaDeSorteios()[i]
        numeroDoPremio = sorteio.h4.text
        premio = sorteio.find('div', class_='row row-bufferTop10').div.p.text
        dezenasSorteadas = sorteio.findAll('span', class_='numberDicker pull-left')
        contemplados = sorteio.findAll('div', class_='col-md-6 col-sm-6 col-xs-12 contemplated')

        print('\n**********************************************************************************\n')
        print(numeroDoPremio)
        print(premio)
        for i in range(len(dezenasSorteadas)):
            dezenas.append(dezenasSorteadas[i].text)
        print('Dezenas Soreteadas: ', dezenas)

        numeroDoPremioS.append(numeroDoPremio)
        premioS.append(premio)

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
            print(strDezenas)
            dezenasSorteadaS.append(strDezenas)

            numeroS.append(numero)
            certificadoS.append(certificado)
            nomeS.append(nome)
            enderecoS.append(endereco)
            bairroS.append(bairro)
            cidadeS.append(cidade)
            pontoDeVendaS.append(pontoDeVenda)

            print("Contemplado Número: {}\nCertificado: {}\nNome: {}\nEndereço: {}\nBairro: {}\nCidade: {}\nPonto de venda: {}\n"
                .format(numero, certificado, limpa(nome), limpa(endereco), limpa(bairro), cidade, pontoDeVenda))

            contemplado = {
                    "Numero": numero,
                    "Certificado": certificado,
                    "Nome": nome,
                    "Endereço": endereco,
                    "Bairro": bairro,
                    "Cidade": cidade,
                    "PontoDeVenda": pontoDeVenda
                }
            listaContemplados.append(contemplado)


        sorteio = {
            "Data": data,
            "NumeroDoPremio": numeroDoPremio,
            "Premio": premio,
            "Dezenas": dezenas,
            "Contemplados": listaContemplados
        }

        listaSorteios.append(sorteio)



        serilaized = json.dumps(listaSorteios, indent=3, ensure_ascii=False)
        jsonarq = criajsonarq(data)
        jsonarq.write(serilaized)
        jsonarq.close()

def run():
    for i in range(meses):


        for r in range(diasPorMes[i]):

            if diasPorMes[i] == 1:
                index = 6
            else:
                index = r + 2

            print('O index é: \n', index)

            dia = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/tbody/tr[{}]/td[1]'.format(index))

            print('Cliquei no dia {}\n'.format(formataData(dia)))
            print('Cliquei no dia {}\n'.format(formataDataToArqName(dia)))
            dia.click()



            driver.execute_script("scrollBy(0,-500);")
            print('Scrollei\n')

            time.sleep(2)

            ir = driver.find_element_by_xpath('//*[@id="calendarSelectDate"]/div/div/div/div/div/div/button')
            ir.click()
            print('Apertei ir\n')

            #raspa dados...
            raspa()
            print('raspando dados...\n')

            #espera a página carregar
            time.sleep(3)

            #abre DatePicker
            abreDatePicker()


        proximoMes()
        time.sleep(5)

        #response = driver.execute_script('return document.documentElement.outerHTML')
        #htmlBS = BeautifulSoup(response, 'html.parser')

abreDatePicker()

vaiParaJulho()

run()

driver.close()

