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

from celular_robo.robo_base import Robo, Direcao
from celular_robo.excecoes import PedidoInvalido

from celular_robo.modos import ModoColetando
#from celular_robo.robo_base import Robo, Coordenada


#from celular_robo.fabrica import *



#DESCRIPTOR
class QuantidadeValida:
    """
    Descriptor para validação de quantidade em atributos de classe.

    Garante que o valor atribuído seja um número não negativo e que não 
    exceda o limite máximo especificado.

    Parâmetros:
        max (int/float, opcional): Valor máximo permitido. Padrão é 100.
    """

    def __init__(self, max = 100): #Valor máximo de 100 por padrão.
        """Inicializa o descriptor definindo o limite máximo permitido.

        Parâmetros:
            max (int/float, opcional): Valor máximo aceito. Padrão é 100.
        """
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




#Bandeja
#Ao utilizar como classe ao invés de uma simples lista, me permitirá guardar mais informações caso necessário.
class Bandeja:
    """Gerencia os items coletados em uma bandeja.
    Controla o armazenamento e a quantidade total de itens, garantindo 
    que o limite máximo suportado não seja ultrapassado através do descriptor.

    Atributos:
        QUANTIDADE_MAXIMA (int): Limite máximo de itens suportados (padrão: 20).
        quantidade (int): Quantidade total de itens atuais na bandeja.
        items (dict): Dicionário mapeando o codinome do item à sua quantidade.
    """

    QUANTIDADE_MAXIMA = 20 # Para este exemplo, a bandeja so podera conter 20 items simultaneamente.
    quantidade = QuantidadeValida(QUANTIDADE_MAXIMA)

    def __init__(self):
        self.quantidade = 0
        self.items = {} #Contem todos os items existentes na bandeja.


    def __str__(self):
        if not self.items:
            return "Bandeja vazia."
        
        itens_formatados = [f"{codinome}: {qtd}" for codinome, qtd in self.items.items()]
        return f"Itens na Bandeja ({self.quantidade}): " + ", ".join(itens_formatados)


    def __len__(self):
        return self.quantidade #


    def inserirItem(self, codinome, quantidade_inserida = 1) -> bool:
        """Adiciona uma determinada quantidade de um item à bandeja.
        Parâmetros:
            codinome (str): Identificador do item a ser inserido.
            quantidade_inserida (int, opcional): Quantidade a adicionar. Padrão é 1.
        Retorna:
            bool: True se o item foi inserido com sucesso, False caso ocorra um erro de validação.
        """
        try:
            self.quantidade = self.quantidade + quantidade_inserida
            self.items[codinome] = self.items.get(codinome, 0) + quantidade_inserida
            return True
        except Exception as e:
            print(e)
            
            return False


    def removerItem(self, codinome, quantidade_removida = 1) -> bool:
        """Remove uma determinada quantidade de um item existente na bandeja.

        Parâmetros:
            codinome (str): Identificador do item a ser removido.
            quantidade_removida (int, opcional): Quantidade a remover. Padrão é 1.
        Retorna:
            bool: True se a remoção for bem-sucedida, False se o item não existir ou se a operação falhar.
        """

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
    """Representa um robô especializado na coleta e transporte de itens.
    Atributos: Além dos herdados.
        bandeja (Bandeja): Instância responsável por armazenar e controlar 
            os itens coletados pelo robô.
    """

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


    def ativarSuccao(self):
        """Simula a ativação do sistema de sucção para captura de itens. Sempre retorna true, para este projeto.

        Retorna:
            bool: True indicando que a sucção foi ativada e o item foi coletado com sucesso. False caso o contrário
        """
        #Representa a ativação da ferramenta que realiza a sucção para pegar o item.
        #Neste caso, sempre retorna true, pois é apenas para simoblizar o sistema de sucção. (True == sucção funcionou e pegou o item.)
        return True
    

    def guardarItemBandeja(self, codinome_item, quantidade):
        """Armazena um item na bandeja e emite um sinal avisando sobre a coleta.
        Parâmetros:
            codinome_item (str): Identificador do item a ser guardado.
            quantidade (int): Quantidade do item a ser adicionada.
        """
        self.bandeja.inserirItem(codinome_item, quantidade)
        if self.bandeja.quantidade >= self.bandeja.QUANTIDADE_MAXIMA:
            self.notificar("bandeja_pronta", bandeja = self.bandeja)
            return True

        #print("NOTIFICANDO COLETA")
        self.notificar("item_coletado", codinome_item = codinome_item, quantidade = quantidade)
        


    def removerItemBandeja(self, codinome_item, quantidade):
        """Retira uma determinada quantidade de um item da bandeja do robô. Normalmente executado ao usar comando.desfazer.
        Parâmetros:
            codinome_item (str): Identificador do item a ser removido.
            quantidade (int): Quantidade do item a ser retirada.
        """
        self.bandeja.removerItem(codinome_item, quantidade)


    def aprovarBandeja(self):
        """Aprova o conteúdo da bandeja, limpa os itens guardados e reinicia o modo de coleta.
        Envia o sinal de "bandeja_aprovada" e, depois, volta para o modo coletando.
        """
        self.notificar("bandeja_aprovada")
        self.bandeja.items.clear()
        self.bandeja.quantidade = 0
        self.modo = ModoColetando()


    def rejeitarBandeja(self):
        """Registra a rejeição da bandeja e restaura o estado de coleta do robô.

        Altera o modo do robô de volta para ModoColetando e envia uma notificação 
        informando que a bandeja atual foi rejeitada, mantendo seus dados para análise.
        """
        self.modo = ModoColetando()
        self.notificar("bandeja_rejeitada", bandeja = self.bandeja)


    def processarComandosColeta(self, lista_comandos: list):
        """Valida e executa os comandos de coleta recebidos pelo robo.
        Caso existam comandos invalidos com a configuração do robo, estes são ignorados.
        Parâmetros:
            lista_comandos (list): Lista de objetos do tipo CommandColeta a serem validados e executados.

        Retorna:
            tuple: Tupla no formato (qtd_sucesso, qtd_total_cmds), contendo a quantidade 
            de comandos executados com sucesso e o total de comandos recebidos.
        """

        from celular_robo.fabrica import validar_compatibilidade_robo_pedido
        #MOTIVO : Estava dando um conflito com pytest. Ao rodar via CLI, funcionava, mas algo ao fazer via pytest dava erro.

        comandos_validos = []
        comandos_invalidos = []

        for comando in lista_comandos:
            if validar_compatibilidade_robo_pedido(self, comando):
                comandos_validos.append(comando)
            else:
                comandos_invalidos.append(comando)

        qtd_total_cmds = len(lista_comandos)
        qtd_invalidos = len(comandos_invalidos)

        if qtd_invalidos > 0:
            print(f"[Aviso] Dos {qtd_total_cmds} comandos recebidos, {qtd_invalidos} foram ignorados por incompatibilidade/invalidação.")

        qtd_sucesso = 0
        for comando in comandos_validos:
            if comando.executar(self):
                self._historico_comandos.append(comando)
                qtd_sucesso += 1

        if qtd_sucesso > 1:
            self.notificar("bandeja_pronta", bandeja=self.bandeja)

        return (qtd_sucesso, qtd_total_cmds)



    def desfazerUltimoComando(self):
            """Desfaz a execução do último comando armazenado no histórico do robô.
            Para isto, ele vai no ultimo comando e usa "desfazer".

            Retorna:
                bool: True se o último comando foi desfeito com sucesso, 
                False se não houver comandos no histórico para desfazer.
            """
            if not self._historico_comandos:
                print(" Não há comandos no histórico para desfazer.")
                return False

            ultimo_comando = self._historico_comandos.pop()
            ultimo_comando.desfazer(self)
            return True
        

    






# #STUB TEST
# my_robo = RoboColetor('Robo R.D')
# my_robo.estrategia = RotaDireta()
# my_robo.modo = ModoColetando()






# print('Testando robo criado manualmente')

# #comando = CommandColeta('Item AX', (3,4), 5)
# #comando.executar(my_robo)

# print(my_robo)


# carregadorArquivos = CarregadorArquivos()
# lotePedidos = carregadorArquivos.montarPedidosJson('dados/pedidos_json/lote1.json')
# lotePedidos = carregadorArquivos.criarComandos(lotePedidos)

# for command in lotePedidos:
#     command.executar(my_robo)

# print(f'Minha bandeja tem : {len(my_robo)}')

# print(lotePedidos)


# print("TESTANDO AGORA O ROBO FABRICADO.")

# try:
#     robo_fabricado = criar_robo_configurado("RoboColetor", "Robo Ford")
#     print(f'Robo fabricado com sucesso : {robo_fabricado}')
#     lote_itens = carregadorArquivos.montarPedidosJson('dados/pedidos_json/lote1.json')
#     lote_pedidos = carregadorArquivos.criarComandos(lote_itens)

    
#     observador_registro = RegistroAuditoria()
#     robo_fabricado.adicionar_observador(observador_registro)

#     for cmd in lote_pedidos:
#         cmd.executar(robo_fabricado)

#     print(f"Quantidade de items na bandeja de {robo_fabricado.nome}: {len(my_robo)}")
#     print("Requisitando informações do log")
#     observador_registro.imprimir_relatório()



# except Exception as e:
#     print("---------------------------------------")
#     print(e)