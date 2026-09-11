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
#from celular_robo.robo import Robo


class ModoColetando(ModoOperacao):
#Anda até o local e coleta.
    def mover():
        #Explicação : Pela arquitetura definida, tornaria-se redundante, pois é o que o método de coleta já está fazendo.
        #Ordem -> Comando --> Modo --> strategy --> robo
        print('NOT IMPLEMENTED')
        pass


    def coletar(self, robo , posicao_alvo_x, posicao_alvo_y):
       return robo.estrategia.mover(robo, posicao_alvo_x, posicao_alvo_y)

    def __str__(self):
        return "Modo de operacao : Coletando"
           





class ModoAguardandoAnalise(ModoOperacao):
    def mover(self, robo):
        print("NÃO PODE MOVER ENQUANTO ESTÁ EM ANALISE.")
        return False

    def coletar(self, robo):
        print("Não pode coletar enquanto está em analise!!!!")
        return False
