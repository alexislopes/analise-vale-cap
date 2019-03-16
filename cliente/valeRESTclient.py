import requests

def salva_dia(dia): #dia has to be jsoned
    headers = {'content-type': 'application/json'}
    requests.post("http://vale-rest.herokuapp.com/dia", data=dia, headers=headers)
