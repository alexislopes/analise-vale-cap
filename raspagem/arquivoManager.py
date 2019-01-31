def criacsv(data):
    arquivo = open('/datasets/csv/sorteio_do_dia_{}.csv'.format(data), "w")
    return arquivo


def criajsonarq(data):
    arquivo = open('/datasets/json/sorteio_do_dia_{}.json'.format(data), 'w')
    return arquivo