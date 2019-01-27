from bs4 import BeautifulSoup
from selenium import webdriver

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
driver.quit()

htmlBS = BeautifulSoup(response, 'html.parser')

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


print('\tSORTEIO DO DIA {}\n'.format(data))

for i in range(int(len(listaDeSorteios)/2-1)):

    dezenas = []

    sorteio = listaDeSorteios[i]
    numeroDoPremio = sorteio.h4.text
    premio = sorteio.find('div', class_='row row-bufferTop10').div.p.text
    dezenasSorteadas = sorteio.findAll('span', class_='numberDicker pull-left')
    contemplados = sorteio.findAll('div', class_='col-md-6 col-sm-6 col-xs-12 contemplated')

    print('\n****************************************************\n')
    print(numeroDoPremio)
    print(premio)


    for k in range(len(contemplados)):
        informacoes = contemplados[k].ul.findAll('li')
        numero = informacoes[NUMERO].text
        certificado = informacoes[CERTIFICADO].strong.text
        nome = informacoes[NOME].text
        endereco = informacoes[ENDERECO].text
        bairro = informacoes[BAIRRO].text
        cidade = informacoes[CIDADE].strong.text
        pontoDeVenda = informacoes[PONTODEVENDA].strong.text

        print("Número: {}\nCertificado: {}\nNome: {}\nEndereço: {}\nBairro: {}\nCidade: {}\nPonto de venda: {}\n"
              .format(numero, certificado, limpa(nome), limpa(endereco), limpa(bairro), cidade, pontoDeVenda))


