# Configuração e persistência — enunciado, Seção 2.6.
#
# TODO: implemente aqui. montar_robo_de_config(config) e
# montar_pedido_de_json(caminho) — mesmo par de funções do capstone do curso
# (montar_robo_de_config/montar_frota_de_json), adaptado: um arquivo
# configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.

from celular_robo.comandos import CommandColeta

class CarregadorArquivos():
    def montarPedidosJson(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
        
        conteudo_python = conteudo.replace("true", "True").replace("false", "False")
        
        dados = eval(conteudo_python)

        return dados.get("itens", [])


    def criarComandos(self, lista_lotes):
        #Converte uma lista de lotes em uma lista de comandos.
        comandos = []
        for item in lista_lotes:
            comando = CommandColeta(
                codinome=item["codinome"],
                posicao=item["posicao"],
                quantidade=item["quantidade"]
            )
            comandos.append(comando)
            
        return comandos
