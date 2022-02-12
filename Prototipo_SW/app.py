class Aplicacao(Subcamada):
    
    def __init__(self):
        Subcamada.__init__(self, sys.stdin)
  
    def recebe(self, dados:bytes):
      # mostra na tela os dados recebidos da subcamada inferior
      print('RX:', dados)

    def handle(self):
      # lê uma linha do teclado
      dados = sys.stdin.readline()

      # converte para bytes ... necessário somente
      # nesta aplicação de teste, que lê do terminal
      dados = dados.encode('utf8') 

      # envia os dados para a subcamada inferior (self.lower)
      self.lower.envia(dados)
