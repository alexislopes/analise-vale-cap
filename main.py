from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import  pandas as pd
from datetime import datetime


driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)



diasPorMes = [1, 4, 5, 4, 4 ,4, 4]
meses = 7

index = 0

dataS = []
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



NUMERO = 0
CERTIFICADO = 1
NOME = 2
ENDERECO = 3
BAIRRO = 4
CIDADE = 5
PONTODEVENDA = 6

#data = ""
#dataArq = data.replace(" ", "_")
#mesano = ""

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
    for k in range(7):
        time.sleep(1)
        prev.click()



#vai para o próximo mes
def proximoMes():
    next = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[3]')
    time.sleep(1)
    next.click()
    print('fui para o próximo mês')

#def mesAno():
#    return driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[2]').text.replace(" ", " de ")

#def formataData(dia):
#    dataFormatada = dia + " de " + mesAno()
#    return dataFormatada

#def formataDataToArqName(dia):
#    formataData(dia).replace(" ", "_")

#def pegaListaDeSorteios():
#    return htmlBS.findAll('div', class_='row row-buffer10 sorteioItem')

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
    arquivo = open('datasets/csv/sorteio_do_dia_{}.csv'.format(data), "w")
    return arquivo


def criajsonarq(data):
    arquivo = open('datasets/json/sorteio_do_dia_{}.json'.format(data), 'w')
    return arquivo

def raspa():
    listaSorteios = []
    time.sleep(5)
    print("DATAAAAAAAA: ", data)

    listaDeSorteios = []
    for i in range(4):
        divSorteio = driver.find_element_by_xpath('/html/body/div[1]/div/div/article/div/div[1]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div/div[{}]'.format(i+2))
        divSorteio = divSorteio.get_attribute('outerHTML')
        divSorteio = BeautifulSoup(divSorteio, 'html.parser')
        #print(divSorteio)
        listaDeSorteios.append(divSorteio)

    for i in range(int(len(listaDeSorteios))):
        print(len(listaDeSorteios))
        listaContemplados = []
        dezenas = []

        sorteio = listaDeSorteios[i]
        numeroDoPremio = sorteio.h4.text

        excecoes = [
            {
                "Data": "23 de Setembro de 2018",
                "0" : "5 mil reais - valor líquido",
                "1" : "10 mil reais - valor líquido",
                "2" : "15 mil reais - valor líquido",
                "3" : "300 mil reais - valor líquido"
             },
            {
                "Data": "7 de Outubro de 2018",
                "0": "5 mil reais - valor líquido",
                "1": "10 mil reais - valor líquido",
                "2": "15 mil reais - valor líquido",
                "3": "500 mil reais - valor líquido"
            },
            {
                "Data" : "14 de Outubro de 2018",
                "0": "1 Fiat MOBI Easy Comfort 1.0 Flex 4P Mec. 0km Sugestão de uso do prêmio no valor líquido de R$ 34.500,00.",
                "1": "1 Chevrolet ONIX Hatch Joy 1.0 8V Flex Mec. 4P 0km Sugestão de uso do prêmio no valor líquido de R$ 44.000,00.",
                "2": "1 HB20 Unique 1.0 Flex Mec. 4P 0km Sugestão de uso do prêmio no valor líquido de R$ 44.000,00.",
                "3": "1 Hilux Cabine Dupla SR 4X2 15V Flex AUT. 0km Sugestão de uso do prêmio no valor líquido de R$ 115.000,00."

            },
            {
                "Data": "21 de Outubro de 2018",
                "0": "10 mil reais - valor líquido",
                "1": "10 mil reais - valor líquido",
                "2": "10 mil reais - valor líquido",
                "3": "1 Casa no valor de 200.000,00 + 100.000,00 Sugestão de uso do prêmio no valor líquido de R$ 300.000,00."
            }
                    ]


        datasExcecoes = [x.get("Data") for x in excecoes]

        if data in datasExcecoes:
            for c in range(len(excecoes)):
                if data == excecoes[c].get("Data"):
                    premio = excecoes[c].get(str(i))
        else:
            premio = sorteio.find('div', class_='row row-bufferTop10').div.p.text


        dezenasSorteadas = sorteio.findAll('span', class_='numberDicker pull-left')
        contemplados = sorteio.findAll('div', class_='col-md-6 col-sm-6 col-xs-12 contemplated')

        print('\n**********************************************************************************\n')
        print(numeroDoPremio)
        print(premio)
        for i in range(len(dezenasSorteadas)):
            dezenas.append(dezenasSorteadas[i].text)
        print('Dezenas Soreteadas: ', dezenas)

        for k in range(len(contemplados)):
            informacoes = contemplados[k].ul.findAll('li')
            nome = limpa(informacoes[NOME].text)
            if nome != "MARIA JACIRA FERREIRA":
                numero = informacoes[NUMERO].text
                certificado = informacoes[CERTIFICADO].strong.text
                nome = limpa(informacoes[NOME].text)
                endereco = limpa(informacoes[ENDERECO].text)
                bairro = limpa(informacoes[BAIRRO].text)
                cidade = informacoes[CIDADE].strong.text
                pontoDeVenda = informacoes[PONTODEVENDA].strong.text
            else:
                numero = informacoes[0].text
                certificado = informacoes[1].text
                nome = limpa(informacoes[2].text)
                endereco = "null"
                bairro = limpa(informacoes[3].text)
                cidade = informacoes[4].strong.text
                pontoDeVenda = informacoes[5].text

            if pontoDeVenda == '':
                pontoDeVenda = "null"


            numeroDoPremioS.append(numeroDoPremio)
            premioS.append(premio)

            strDezenas = ' '.join(e for e in dezenas)
            print(strDezenas)
            dezenasSorteadaS.append(strDezenas)

            dataS.append(data)
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
        jsonarq = criajsonarq(data.replace(" ", "_"))
        jsonarq.write(serilaized)
        jsonarq.close()


        print("Largura das listas: \n"
              + "dataS: {}\n".format(len(dataS))
              + "numeroDoPremioS: {}\n".format(len(numeroDoPremioS))
              + "premioS: {}\n".format(len(premioS))
              + "dezenasSorteadaS: {}\n".format(len(dezenasSorteadaS))
              + "certificadoS: {}\n".format(len(certificadoS))
              + "nomeS: {}\n".format(len(nomeS))
              + "bairroS: {}\n".format(len(bairroS))
              + "cidadeS: {}\n".format(len(cidadeS))
              + "pontoDeVendaS: {}\n".format(len(pontoDeVendaS))

              )


    criaDataFrame(dataS, numeroDoPremioS, premioS, dezenasSorteadaS, numeroS, certificadoS, nomeS, enderecoS, bairroS, cidadeS, pontoDeVendaS)

def criaDataFrame(lista0, lista1, lista2, lista3, lista4, lista5, lista6, lista7, lista8, lista9, lista10):
    df = pd.DataFrame(
        {
            "Data" : lista0,
            "NumeroDoPremio": lista1,
            "Premio": lista2,
            "Dezenas": lista3,
            "Numero": lista4,
            "Certificado": lista5,
            "Nome": lista6,
            "Endereço": lista7,
            "Bairro": lista8,
            "Cidade": lista9,
            "PontoDeVenda": lista10
        }
    )

    df.reset_index()
    df.to_csv(path_or_buf=criacsv(data.replace(" ", " _")))
    lista0.clear()
    lista1.clear()
    lista2.clear()
    lista3.clear()
    lista4.clear()
    lista5.clear()
    lista6.clear()
    lista7.clear()
    lista8.clear()
    lista9.clear()
    lista10.clear()


def run():
    global data
    global mesano

    for i in range(meses):
        mesano = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/thead/tr[2]/th[2]').text.replace(" ",
                                                                                                               " de ")
        for r in range(diasPorMes[i]):

            if diasPorMes[i] == 1:
                index = 6
            else:
                index = r + 2

            print('O index é: \n', index)

            dia = driver.find_element_by_xpath('/html/body/div[8]/div[1]/table/tbody/tr[{}]/td[1]'.format(index))


            data = dia.text + " de " + mesano

            dia.click()

            driver.execute_script("scrollBy(0,-600);")
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
