class Contemplado:

    def __init__(self, numero, certificado, nome, endereco, bairro, cidade, pontoDeVenda):

        self.numero = numero
        self.certificado = certificado
        self.nome =nome
        self.endereco = endereco
        self.bairro = bairro
        self.cidade = cidade
        self.pontoDeVenda = pontoDeVenda

    def get_numero(self):
        return self.numero

    def set_numero(self, numero):
        self.numero = numero

    def get_certificado(self):
        return self.certificado

    def set_certificado(self, certificado):
        self.certificado = certificado

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_endereco(self):
        return self.endereco

    def set_endereco(self, endereco):
        self.endereco = endereco

    def get_bairro(self):
        return self.bairro

    def set_bairro(self, bairro):
        self.bairro = bairro

    def get_cidade(self):
        return self.cidade

    def set_cidade(self, cidade):
        self.cidade

    def get_pontoDeVenda(self):
        return self.pontoDeVenda

    def set_pontoDeVenda(self, pontoDeVenda):
        self.pontoDeVenda = pontoDeVenda