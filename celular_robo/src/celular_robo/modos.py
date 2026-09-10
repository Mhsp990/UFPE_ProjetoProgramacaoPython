# State — ModoColetando, ModoAguardandoVerificacao — enunciado, Seção 2.3.
#
# Herde de `ModoOperacao` (modos_base.py — ABC com registro automático):
#
#   from celular_robo.modos_base import ModoOperacao
#
# TODO: implemente aqui. A transição ModoColetando -> ModoAguardandoVerificacao
# acontece via Observer (não é o próprio modo que decide sozinho), quando a
# bandeja completa.

from celular_robo.modos_base import ModoOperacao
from celular_robo.robo import Robo


class ModoColetando(ModoOperacao):
#Anda até o local e coleta.
    def mover():
        #Explicação : 
        print('NOT IMPLEMENTED')
        pass


    def coletar(self, robo : Robo, posicao_alvo_x, posicao_alvo_y):
       return robo.estrategia.mover(robo, posicao_alvo_x, posicao_alvo_y)
           





