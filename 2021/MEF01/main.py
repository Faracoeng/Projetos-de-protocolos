# Lembre de instalar o pacote attrs no seu ambiente Python !
import attr

# usa um decorator para definir a classe
@attr.s
class MEF:
    estado=attr.ib(default=0)
    # tabela de tratadores para cada estado
    tratadores=attr.ib(factory=dict)

    @staticmethod
    def cria():
        mef = MEF()
        mef.tratadores[0] = mef.trata_s0
        mef.tratadores[1] = mef.trata_s1
        mef.tratadores[2] = mef.trata_s2
        return mef

    def trata_evento(self, caractere):
        tratador_atual = self.tratadores[self.estado]
        tratador_atual(caractere)

    def trata_s0(self, caractere):
        print(f'tratou {caractere} no estado S0')
        self.estado = 1

    def trata_s1(self, caractere):
        print(f'tratou {caractere} no estado S1')
        self.estado = 2

    def trata_s2(self, caractere):
        print(f'tratou {caractere} no estado S2')
        self.estado = 0