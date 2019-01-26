from bs4 import BeautifulSoup
from selenium import webdriver

NUMEROCONTEMPLADO = 0
CERTIFICADOCONTEMPLDO = 1
NOMECONTEMPLADO = 2
ENDERECOCONTEMPLADO = 3
BAIRROCONTEMPLADO = 4
CIDADECONTEMPLADO = 5
PONTODEVENDA = 6

dezenas = []

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

response = driver.execute_script('return document.documentElement.outerHTML')
driver.quit()

htmlBS = BeautifulSoup(response, 'html.parser')

data = htmlBS.find('span', class_='pull-left dateTitle').text

listaDeSorteios = htmlBS.findAll('div', class_='row row-buffer10 sorteioItem')

primeiroSorteio = listaDeSorteios[0]

numeroDoPremio = primeiroSorteio.h4.text

premio = primeiroSorteio.find('div', class_='row row-bufferTop10').div.p.text

dezenasSorteadas = primeiroSorteio.findAll('span', class_='numberDicker pull-left')

contemplados = primeiroSorteio.findAll('div', class_='col-md-6 col-sm-6 col-xs-12 contemplated')

informacoesContemplado = contemplados[0].ul.findAll('li')

numeroContemplado = informacoesContemplado[NUMEROCONTEMPLADO].text

certificadoContemplado = informacoesContemplado[CERTIFICADOCONTEMPLDO].strong.text

nomeContemplado = informacoesContemplado[NOMECONTEMPLADO].text

enderecoContemplado = informacoesContemplado[ENDERECOCONTEMPLADO].text

bairroContemplado = informacoesContemplado[BAIRROCONTEMPLADO].text

cidadeContemplado = informacoesContemplado[CIDADECONTEMPLADO].strong.text

pontoDeVendaContemplado = informacoesContemplado[PONTODEVENDA].strong.text
# nomeContemplado = contemplados[0].

print('******************* {} *******************'.format(data))
print(numeroDoPremio)
print(premio)
for i in range(len(dezenasSorteadas)):
    dezenas.append(dezenasSorteadas[i].text)
print("Dezenas Sorteadas: ", dezenas)
print(numeroContemplado)
print(certificadoContemplado)
print(nomeContemplado)
print(enderecoContemplado)
print(bairroContemplado)
print(cidadeContemplado)
print(pontoDeVendaContemplado)
