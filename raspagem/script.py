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
    arquivo = open('../datasets/csv/{}.csv'.format("boom"), "w")
    return arquivo


def criajsonarq(nome):
    arquivo = open('../datasets/json/{}.json'.format(nome), 'w')
    return arquivo


print('\tSORTEIO DO DIA {}\n'.format(data))

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

for i in range(int(len(listaDeSorteios) / 2 - 1)):
    listaContemplados = []
    dezenas = []

    sorteio = listaDeSorteios[i]
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
    jsonarq = criajsonarq('sorteio_do_dia_{}'.format(str(k)))
    jsonarq.write(serilaized)
    jsonarq.close()

df = pd.DataFrame(
        {
            "NumeroDoPremio": numeroDoPremioS,
            "Premio": premioS,
            "Dezenas": dezenasSorteadaS,
            "Numero": numeroS,
            "Certificado": certificadoS,
            "Nome": nomeS,
            "Endereço": enderecoS,
            "Bairro": bairroS,
            "Cidade": cidadeS,
            "PontoDeVenda": pontoDeVendaS
        }
)

df.reset_index()

df.to_csv(path_or_buf=criacsv())
