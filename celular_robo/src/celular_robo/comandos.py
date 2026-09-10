# Command — ComandoColeta — enunciado, Seção 2.3.
#
# Herde de `Comando` (comandos_base.py — ABC com registro automático):
#
#   from celular_robo.comandos_base import Comando
#
# TODO: implemente aqui. ComandoColeta(Comando): __init__(codinome, posicao,
# quantidade), com .executar(robo) e .desfazer(robo) (remove o item da
# bandeja, decrementa a contagem coletada).
from celular_robo.comandos_base import Comando

class CommandColeta(Comando):

    def __init__(self, codinome, posicao, quantidade):
        super().__init__()

        self.codinome = codinome
        self.posicao = posicao
        self.quantidade = quantidade


    def executar(self, robo):

        #Primeiro, vai até a localização
        robo.mover()
        
