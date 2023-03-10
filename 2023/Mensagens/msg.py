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

    def serialize(self):
        
        msg = Mensagem.serialize(self)
        extra = struct.pack('!H', self._blocknum)
        return msg + extra + self.body

def cria_instancia(msg:bytes):
    print()
    # Criar uma instancia de subclasse da classe "Mensagem"


# Para decodificar as mensagens que chegam:

# Aqui descompacta os 4 prmeiros bytes
struct.unpack_from('!HH',msg)
# Aqui pega o restante da mensagem que não qual o tamanhho,
# por isso fazer assim
body = msg[struct.calcsize('!HH'):]