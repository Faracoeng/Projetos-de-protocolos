# This is a sample Python script.
from enum import Enum

class Estado(Enum):
    S0=0
    S1=1
    S2=2

class MEF:

    def __init__(self):
        self.estado = Estado.S0
        self.buffer = ''
        self.tratadores = {
            Estado.S0: self.trata_s0,
            Estado.S1: self.trata_s1,
            Estado.S2: self.trata_s2,
        }

    def trata_evento(self, caractere):
        tratador_atual = self.tratadores[self.estado]
        return tratador_atual(caractere)

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