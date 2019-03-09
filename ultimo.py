import data
from selenium import webdriver
import time
import json
import pandas as pd
#import main
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
url = 'http://valecaperegiao.com.br/resultados/'

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

def criacsv(data):
    arquivo = open('datasets/csv/sorteio-do-dia-{}.csv'.format(data), "w")
    return arquivo


def criajsonarq(data):
    arquivo = open('datasets/json/sorteio-do-dia-{}.json'.format(data), 'w')
    return arquivo

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


def raspa():
    listaSorteios = []
    time.sleep(5)
    print("DATAAAAAAAA: ", data)

    listaDeSorteios = []
    for i in range(4):
        divSorteio = driver.find_element_by_xpath("/html/body/div[1]/div/div/article/div/div[1]/div[2]/div/div/div/div/div/div/div[1]/div[2]")
        divSorteio = divSorteio.get_attribute('outerHTML')
        divSorteio = BeautifulSoup(divSorteio, 'html.parser')
        # print(divSorteio)
        listaDeSorteios.append(divSorteio)

    for i in range(int(len(listaDeSorteios))):
        print(len(listaDeSorteios))
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

        for k in range(len(contemplados)):
            informacoes = contemplados[k].ul.findAll('li')
            #nome = informacoes[2].text
            numero = informacoes[0].text
            certificado = informacoes[1].strong.text
            nome = informacoes[2].text
            endereco = informacoes[3].text
            bairro = informacoes[4].text
            cidade = informacoes[5].strong.text
            pontoDeVenda = informacoes[6].strong.text

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

        print(
            "Contemplado Número: {}\nCertificado: {}\nNome: {}\nEndereço: {}\nBairro: {}\nCidade: {}\nPonto de venda: {}\n"
            .format(numero, certificado, nome, endereco, bairro, cidade, pontoDeVenda))

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


    criaDataFrame(dataS, numeroDoPremioS, premioS, dezenasSorteadaS, numeroS, certificadoS, nomeS, enderecoS, bairroS,
              cidadeS, pontoDeVendaS)


#def abreDatePicker():
#    carregarMais = driver.find_element_by_xpath(
#        '//*[@id="post-183"]/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[3]/div/a')
#    carregarMais.click()
#
#    time.sleep(2)
#
#    carregarMais.click()
#
#    datepicker = driver.find_element_by_xpath('//*[@id="search-date-input"]')
#    datepicker.click()
#    print('abri DatePicker\n')


driver.get(url)

#abreDatePicker()

#dia = driver.find_element_by_css_selector(
#        'html.js body.page-template-default.page.page-id-183.et_pb_button_helper_class.et_fixed_nav.et_show_nav.et_hide_fixed_logo.et_hide_mobile_logo.et_cover_background.et_pb_gutter.linux.et_pb_gutters2.et_primary_nav_dropdown_animation_fade.et_secondary_nav_dropdown_animation_fade.et_pb_footer_columns4.et_header_style_centered.et_pb_pagebuilder_layout.et_right_sidebar.et_divi_theme.gecko div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-top div.datepicker-days table.table-condensed tbody tr td.today.day')
#mesano = driver.find_element_by_xpath("/html/body/div[8]/div[1]/table/thead/tr[2]/th[2]")
#diamesano = dia.text + " " + mesano.text
#diamesano = diamesano.replace(" ", " de ")
#print(diamesano)

raspa()
