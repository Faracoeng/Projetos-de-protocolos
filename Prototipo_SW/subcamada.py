from poller import Callback

class Subcamada(Callback):

    def __init__(self, fonte, tout:float):
        'font: fonte de dados a ser monitorada (um descritor de arquivo ou um objeto que implemente a interface tout: valor de timeout em segundos)'
        Callback.__init__(self, fonte, tout)
        self.lower = None
        self.upper = None

    def envia(self, dados:bytes):
        raise NotImplementedError('abstrato')
    def recebe(self, dados:bytes):
        raise NotImplementedError('abstrato')
    def conecta(self, uplayer):
        'Conecta esta subcamada à sua subcamada superior'
        self.upper = uplayer
        'Conecta esta subcamada à sua subcamada inferior'
        self.upper = self

