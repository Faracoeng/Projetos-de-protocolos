# This is a sample Python script.
import attr
from enum import Enum

class Estado(Enum):
    S0=0
    S1=1
    S2=2

# usa um decorator para definir a classe
@attr.s
class MEF:
    estado=attr.ib(default=Estado.S0)
    # tabela de tratadores para cada estado
    buffer=attr.ib(default='')

    def trata_evento(self, caractere):
        if self.estado == Estado.S0:
            return self.trata_S0(caractere)
        elif self.estado == Estado.S1:
            return self.trata_S1(caractere)
        elif self.estado == Estado.S2:
            return self.trata_S2(caractere)

    def trata_s0(self, caractere):
        # transição ?F -> S1
        if caractere == 'F':
            self.estado = Estado.S1

    def trata_s1(self, caractere):
        # transição ?F/processa -> S0
        if caractere == 'F':
            self.estado = Estado.S0
            buffer = self.buffer
            self.buffer = ''
            return buffer
        # transição ?D -> S2
        elif caractere == 'D':
            self.estado = Estado.S2
        # transição ?X/armazena -> S1
        else:
            self.buffer += caractere

    def trata_s2(self, caractere):
        # transição ?D ou ?F/descarta -> S0
        if caractere in ('F', 'D'):
            self.buffer = ''
            self.estado = Estado.S0
        # transição ?X/armazena -> S1
        else:
            self.buffer += caractere
            self.estado = Estado.S1