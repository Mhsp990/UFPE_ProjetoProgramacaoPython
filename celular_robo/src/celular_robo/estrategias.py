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


#OBS: Pela forma que fiz a arquitetura, estrategia é responsável apenas por decidir COMO chegar no local alvo.
#Portanto, o comando coletar usa a estratégia para se locomover até lá e, depois ele mesmo coleta ativando o robo e adiciona na bandeja.
#Portanto, na dupla conferência, não há uma revalidação de item antes de despejar na bandeja.



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
    """Implementa uma estratégia de navegação direta para robôs de coleta.
    """


    #Vai direto até cada pratileira.
    def mover(self, robo, posicao_alvo_x, posicao_alvo_y):
        """Move o robô em direção às coordenadas informadas até atingir o alvo. Há um limite de passos.
        Parâmetros:
            robo (Robo): Instância do robô que executará os movimentos.
            posicao_alvo_x (int): Coordenada X do destino final.
            posicao_alvo_y (int): Coordenada Y do destino final.

        Retorna:
            bool: True se o robô alcançar a posição alvo dentro do limite de movimentações, 
            False caso contrário.
        """

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
            


        if num_movimentacoes > max_movimentacoes:
            print("Rota direta falhou em mover-se ate o alvo antes do maximo")
            return False
        else:
            print("Rota direta conseguiu mover-se até o alvo antes do maximo de movimentacoes.")
            print(f"Num de movimentacoes necessarias: {num_movimentacoes}")
            return True



    def __str__(self):
        return "Rota Direta"


        







    def _direcao_para_alvo(self, robo, posicao_alvo_x, posicao_alvo_y):
    #Verifica qual direcao deve girar para ir até a posição alvo.
        if robo.x < posicao_alvo_x:
            return Direcao.LESTE

        if robo.x > posicao_alvo_x:
            return Direcao.OESTE    

        if robo.y < posicao_alvo_y:
            return Direcao.NORTE

        return Direcao.SUL




class RotaComDuplaConferencia(RotaDireta):
    """Implementa uma estratégia de navegação com verificação de integridade posicional.

    Extende a classe RotaDireta adicionando uma etapa de validação que confirma
    se o robô realmente atingiu as coordenadas esperadas após o término do movimento.
    """

    #Como a checagem da bandeja foi implementada de forma que não é responsabilidade da estratégia, fiz com que essa
    #estrategia duplaConferencia fosse responsável apenas por verificar duas vezes se a posição atual realmente é a desejada.
    #Ademais, devido a arquitetura escolhida, a validação dos items é feita ANTES da execução de cada comando,
    #no qual comandos incompativeis são ignorados. (Não há troca de estratégia, conforme explicado no readme.)
        

    def mover(self, robo, posicao_alvo_x: int, posicao_alvo_y: int) -> bool:

        chegou = super().mover(robo, posicao_alvo_x, posicao_alvo_y)

        if not chegou:
            return False

        posicao_esperada = (posicao_alvo_x, posicao_alvo_y)
        posicao_real = (robo.x, robo.y)

        if posicao_real != posicao_esperada:
            print(f"[Dupla Conferência Falhou]: Esperado {posicao_esperada}, mas robô está em {posicao_real}")
            return False

        return True

    def __str__(self):
        return "Rota com Dupla Conferência"
