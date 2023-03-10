class Mensagem:
    def __init__(self, op:int):
        self._opcode = op
    def serialize(self):
        raise NotImplemented('abstrato')

class Data(Mensagem):
    opcode= 4

    def __init__(self, blocknum:int, body:bytes):
        Mensagem.__init__(self, self.opcode)
        self.blocknum = blocknum
        if len(body)> 512:
            raise ValueError('Corpo deve ter no máximo 512 Bytes')
        self.body = body
def cria_instancia(msg:bytes):
    print()
    # Criar uma instancia de subclasse da classe "Mensagem"