from requests import get
from bs4 import BeautifulSoup as bs

url = 'http://valecaperegiao.com.br/resultados/'

response = get(url)
# print(response.text)

html_soup = bs(response.text, 'html.parser')

container_de_sorteios = html_soup.findAll('div', class_='row row-buffer10 sorteioItem')

primeiro_sorteio = container_de_sorteios[5]

numero_sorteio = primeiro_sorteio.find('div', class_='col-md-12').h4.text

premio = primeiro_sorteio.find('div', class_='row')

#print(type(contaioner_de_sorteios))
#print(len(contaioner_de_sorteios))
print(premio)
