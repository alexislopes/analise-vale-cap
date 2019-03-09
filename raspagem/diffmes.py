from _datetime import datetime
import math

agora = datetime.now()
dia = agora.day
mes = agora.month
ano = agora.year

def diffMes():
    d2 = datetime.strptime('{}-{}-{}'.format(ano, mes, dia), '%Y-%m-%d')
    d1 = datetime.strptime('2018-07-27', '%Y-%m-%d')


    quantidade_dias = abs((d2 - d1).days)

    return math.ceil(quantidade_dias/30)