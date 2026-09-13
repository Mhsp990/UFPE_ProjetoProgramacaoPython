# Configuração e persistência — enunciado, Seção 2.6.
#
# TODO: implemente aqui. montar_robo_de_config(config) e
# montar_pedido_de_json(caminho) — mesmo par de funções do capstone do curso
# (montar_robo_de_config/montar_frota_de_json), adaptado: um arquivo
# configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.

from celular_robo.comandos import CommandColeta

class CarregadorArquivos():
    """Responsável por converter os arquivos json para "data" legível para o software.
    A partir de um json, que contém uma lista de items a serem pedidos, converte-os em uma lista de items e, depois
    converte-os em uma lista de commandColeta, pronta para uso.
    """

    def montarPedidosJson(self, caminho):
        """Lê um arquivo JSON contendo a estrutura de pedidos e extrai a lista de itens.
        A estrutura deve seguir a observada nos arquivos em dados -> pedidos_json
        Parâmetros:
            caminho (str): O caminho do arquivo a ser lido.

        Retorna:
            list: Lista de dicionários representando os itens a serem coletados.
        """
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
        
        conteudo_python = conteudo.replace("true", "True").replace("false", "False")
        
        dados = eval(conteudo_python)

        return dados.get("itens", [])


    def criarComandos(self, lista_lotes):
        """Gera uma lista de instâncias de CommandColeta a partir de dicionários de pedidos.
        Parâmetros:
            lista_lotes (list): Lista de dicionários contendo os dados dos itens (codinome, posição, quantidade, etc).
        Retorna:
            list: Lista de objetos CommandColeta prontos para execução.
        """
        #Metodo utilizado para gerar os comandos a partir de uma lista de pedidos.
        comandos = []
        for item in lista_lotes:
            comando = CommandColeta(
                codinome=item["codinome"],
                posicao=item["posicao"],
                quantidade=item["quantidade"],
                fragil=item.get("fragil", False),
                urgente=item.get("urgente", False)
            )
            comandos.append(comando)
            
        return comandos
