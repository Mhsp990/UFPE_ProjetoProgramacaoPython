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
#from celular_robo.robo import RoboColetor

class CommandColeta(Comando):

    def __init__(self, codinome, posicao, quantidade):
        super().__init__()

        self.codinome = codinome
        self.posicao = posicao
        self.quantidade = quantidade


    def __repr__(self):
        return f"CommandColeta(codinome='{self.codinome}', posicao={self.posicao}, quantidade={self.quantidade})"

    def __str__(self):
        return f"O comando é : Coletar {self.quantidade} de '{self.codinome}' na posição {self.posicao}"



    def executar(self, robo):        
        try:
            #Primeiro, vai até a localização
            resultado_coleta = robo.modo.coletar(robo, self.posicao[0], self.posicao[1])

            if not resultado_coleta:
                print(f"Não foi possível realizar a coleta do item {self.codinome} em {self.posicao}")
                return False

            #Agora, já que estamos na localização correta:
            #quantidade_restante = self.quantidade
            for i in range(self.quantidade):
                if robo.ativarSuccao():
                    robo.guardarItemBandeja(self.codinome, 1) #Neste caso, estou considerando um por vez.


            #Comando concluido. Emitir sinal.
            
            return True
        except Exception as e:
            print(e)


        
