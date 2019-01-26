from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'
driver.get(url)

response = driver.execute_script('return document.documentElement.outerHTML')
driver.quit()

htmlBS = BeautifulSoup(response, 'html.parser')

data = htmlBS.find('span', class_='pull-left dateTitle')

listaDeSorteios = htmlBS.findAll('div', class_='row row-buffer10 sorteioItem')

primeiroSorteio = listaDeSorteios[0]

numeroDoPremio = primeiroSorteio.h4.text

premio = primeiroSorteio.find('div', class_='row row-bufferTop10').div.p.text

dezenasSorteadas = primeiroSorteio.findAll('span', class_='numberDicker pull-left')

primeiraDezena = dezenasSorteadas[0].text

print(dezenasSorteadas[0].text)






























#

#numero_sorteio = primeiro_sorteio.find('div', class_='col-md-12').h4.text



#print(type(contaioner_de_sorteios))
#print(len(contaioner_de_sorteios))
#print(premio)