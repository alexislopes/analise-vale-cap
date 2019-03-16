class Sorteio:

    def __init__(self, numero, premio, dezenas, contemplados):

        self.numero = numero
        self.premio = premio
        self.dezenas = dezenas
        self.contemplados = contemplados

    def get_numero(self):
        return self.numero

    def set_numero(self, numero):
        self.numero = numero

    def get_premio(self):
        return self.premio

    def set_premio(self, premio):
        self.premio = premio

    def get_dezenas(self):
        return self.dezenas

    def set_dezenas(self, dezenas):
        self.dezenas = dezenas

    def get_contemplados(self):
        return self.contemplados

    def set_contemplados(self, contemplados):
        self.contemplados = contemplados