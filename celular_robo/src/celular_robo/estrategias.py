# Strategy — RotaDireta, RotaComDuplaConferencia — enunciado, Seção 2.3.
# (Não confundir com estrategias_base.py — genérico do curso, não editar. Ao
# contrário de Command/Observer/State, aqui você NÃO herda de `Estrategia`:
# escreva sua própria base, ver TODO abaixo — motivo em estrategias_base.py.)
#
# TODO: implemente aqui. Considere uma base comum (RotaColeta) com
# __init_subclass__ registrando cada rota, ver Seção 2.2 (metaprogramação
# aplicada a uma segunda hierarquia).

from abc import ABC, abstractmethod
from celular_robo.robo_base import Direcao


class RotaColeta(ABC):
    # posicao_alvo_x = 0
    # posicao_alvo_y = 0

    _registro_rotas = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        RotaColeta._registro_rotas[cls.__name__] = cls


    @abstractmethod   
    def mover(self, robo): pass
    


class RotaDireta(RotaColeta):
    #Vai direto até cada pratileira.
    def mover(self, robo, posicao_alvo_x, posicao_alvo_y):

        alvo = (posicao_alvo_x, posicao_alvo_y)

        num_movimentacoes = 0
        max_movimentacoes = 100 #Evitar loops longos.


        while robo.posicao != alvo and (num_movimentacoes < max_movimentacoes):
            direcao = self._direcao_para_alvo(robo, posicao_alvo_x, posicao_alvo_y)
            robo.girar_ate(direcao)

            num_movimentacoes += 1
            if robo.avancar():
                #Se conseguiu avançar, passe para a próxima iteração.
                continue
            else:
                tentativas = 0
                while not robo.sensor_frente() and tentativas < 4:
                    #TODO : Mudar isso para EVITAR a direção oposta a inicial, para evitar "vai e vem" pro mesmo lugar.
                    #Provavelmente deve ser possível ao restringir a apenas um giro para a esquerda e, depois, dois para a direita.
                    robo.girar("DIR")
                    tentativas += 1
            


        if num_movimentacoes < max_movimentacoes:
            print("Rota direta falhou em mover-se ate o alvo antes do maximo")
            return False
        else:
            print("Rota direta conseguiu mover-se até o alvo antes do maximo de movimentacoes.")
            print(f"Num de movimentacoes necessarias: {num_movimentacoes}")
            return True


        







    def _direcao_para_alvo(self, robo, posicao_alvo_x, posicao_alvo_y):
    #Verifica qual direcao deve girar para ir até a posição alvo.
        if robo.x < posicao_alvo_x:
            return Direcao.LESTE

        if robo.x > posicao_alvo_x:
            return Direcao.OESTE    

        if robo.y < posicao_alvo_y:
            return Direcao.NORTE

        return Direcao.SUL




class RotaComDuplaConferencia(RotaColeta):
    #
    pass