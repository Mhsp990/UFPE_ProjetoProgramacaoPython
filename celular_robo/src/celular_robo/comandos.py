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
from celular_robo.excecoes import PedidoInvalido

class CommandColeta(Comando):
    """Representa um comando específico para a realização de coleta de itens por um robô.
    Armazena as informações do item a ser coletado que são necessárias para realizar a coleta.
    Também controla o fluxo para que a coleta seja feita com sucesso a partir de um dado robo.
    Os pedidos que chegam via arquivo são tratados utilizando a classe Carregador Arquivo, em persistencia.py.

    Atributos:
        codinome (str): Identificador do item a ser coletado.
        posicao (tuple/list): Coordenadas (x, y) onde o item se encontra.
        quantidade (int): Quantidade total do item a ser coletada.
        fragil (bool): Indica se o item exige manuseio delicado (padrão: False).
        urgente (bool): Indica se o pedido possui prioridade de coleta (padrão: False).
    """

    def __init__(self, codinome, posicao, quantidade, fragil = False, urgente = False):
        super().__init__()

        self.codinome = codinome
        self.posicao = posicao
        self.quantidade = quantidade
        self.fragil = fragil
        self.urgente = urgente


    # def __repr__(self):
    #     return f"CommandColeta(codinome='{self.codinome}', posicao={self.posicao}, quantidade={self.quantidade})"

    def __str__(self):
        return f"O comando é : Coletar {self.quantidade} de '{self.codinome}' na posição {self.posicao}. Fragil : {self.fragil}, Urgente : {self.urgente}"



    def executar(self, robo):      
        """Executa a movimentação até a posição informada e realiza a coleta do item.

        Desloca o robô até o local indicado, aciona o sistema de sucção para cada item.

        Parâmetros:
            robo (RoboColetor): A instância do robô responsável por executar o comando.

        Retorna:
            bool/None: True se a coleta for concluída com sucesso, False se falhar a navegação 
        """  
        try:
            if self.quantidade <= 0:
                raise PedidoInvalido

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
     
            return True
        except Exception as e:
            print(e)


    def desfazer(self, robo):
        """Reverte a ação de coleta, removendo a quantidade coletada da bandeja do robô.
        Parâmetros:
            robo (RoboColetor): A instância do robô onde a operação será desfeita.
        """
        #Neste caso, o desfazer apenas remove o item da bandeja.
        #Este método é acessível via robo ao fazer : Robo.desfazerUltimoComando

        robo.removerItemBandeja(self.codinome, self.quantidade)
        
