# RoboColetor + QuantidadeValida — enunciado, Seção 2.1.
#
# `Robo` (posição, __init_subclass__/_registro, avancar/girar, estrategia/modo,
# Observer) já vem pronto em robo_base.py — não precisa reescrever, só importar:
#
#   from celular_robo.robo_base import Robo, Coordenada
#
# TODO: implemente aqui.
# - RoboColetor(Robo): reaproveita Coordenada (x, y) por herança — não precisa
#   redeclarar. Adicione o que for específico da coleta (ex.: bandeja).
# - QuantidadeValida: descriptor novo (mesmo protocolo de Coordenada/Percentual
#   em robo_base.py), validando que a quantidade coletada de um item nunca é
#   negativa nem passa do pedido.
# - __str__/__repr__ (robô) e __len__ (bandeja — quantos itens já coletados).

from celular_robo.robo_base import *
from celular_robo.excecoes import *
#from celular_robo.src.celular_robo.robo_base import Direcao
#from celular_robo.robo_base import Robo, Coordenada


#DESCRIPTOR
class QuantidadeValida:

    def __init__(self, max = 100): #Valor máximo de 100 por padrão.
        self.max = max

    def __set_name__(self, owner, name):
        self.nome = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.nome]

    def __set__(self, instance, valor):
        if valor < 0:
            raise PedidoInvalido(f"Erro : Pedido com valor negativo.")
        if valor > self.max:
            raise PedidoInvalido(f"Erro : A quantidade pedida é maior que a maxima")
        instance.__dict__[self.nome] = valor


#Itens
#Será uma classe que presentará um item que pode ser pedido.
class ItemLotePedido():
    quantidade = QuantidadeValida() 

    def __init__(self, codinome, quantidade, posicao_x, posicao_y, fragil = False, urgente = False):
        self.codinome = codinome

        self.quantidade = quantidade 

        self._posicao_x = posicao_x 
        self._posicao_y = posicao_y 
        self.fragil = fragil
        self.urgente = urgente

    @property
    def posicao(self):
        return (self._posicao_x, self._posicao_y)


#Bandeja
#Ao utilizar como classe ao invés de uma simples lista, me permitirá guardar mais informações caso necessário.
#Ademais, conterá uma lista de ItemPedido
class Bandeja:
    QUANTIDADE_MAXIMA = 20 # Para este exemplo, a bandeja so podera conter 20 items simultaneamente.
    quantidade = QuantidadeValida(QUANTIDADE_MAXIMA)

    def __init__(self):
        self.quantidade = 0
        self.items = {} #Contem todos os items existentes na bandeja.


    def __len__(self):
        return self.quantidade #


    def inserirItem(self, codinome, quantidade_inserida = 1) -> bool:
        try:
            self.quantidade = self.quantidade + quantidade_inserida
            self.items[codinome] = self.items.get(codinome, 0) + quantidade_inserida
            return True
        except Exception as e:
            print(e)
            return False


    def removerItem(self, codinome, quantidade_removida = 1) -> bool:
        if codinome not in self.items:
            print("Não é possível remover o item, pois ele não existe na bandeja.")
            return False

        try:
            self.quantidade = self.quantidade - quantidade_removida
            self.items[codinome] -= quantidade_removida
            return True
        except Exception as e:
            print(e)
            return False
            
        









class RoboColetor(Robo):

    def __init__(self, nome, x=0, y=0, direcao=Direcao.LESTE, obstaculos=None, bateria=100, alcance_sensor=1, alcance_radio=5, estrategia=None, modo=None):
        super().__init__(nome, x, y, direcao, obstaculos, bateria, alcance_sensor, alcance_radio, estrategia, modo)

        self.bandeja = Bandeja()


    def __repr__(self):
        resultado = f"RoboColetor({self.nome!r}), x={self.x}, y={self.y}, direcao={self.direcao}, bateria={self.bateria}"
        return resultado



    def __str__(self):
        #Irá retornar, apenas, o nome, posição atual, bateria, estrategia, modo.
        return f"Robo coletor {self.nome} está em {self.x},{self.y}. A bateria atual eh de {self.bateria}. Modo atual {self.modo} e estrategia eh {self.estrategia}"
    


    def __len__(self):
        return len(self.bandeja)





