# CLI — enunciado, Seção 4.
#
# TODO: implemente aqui. Menu interativo (ou argparse, à sua escolha):
# listar pedido carregado, processar pedido, ver estado da bandeja,
# aprovar/rejeitar retirada da equipe de testes.

import json
import sys
from celular_robo.robo import RoboColetor
from celular_robo.persistencia import CarregadorArquivos
from celular_robo.fabrica import *
from celular_robo.observadores import RegistroAuditoria, EquipeDeTestes


class ErroInput(Exception):
    pass

class ErroObjetosNaoInicializados(ErroInput):
    pass

#Mapeamento de prompts
CONFIGS_ROBOS = {
    0: "dados/robos_json/coletor_padrao.json",
    1: "dados/robos_json/coletor_quarentena.json",
}

LOTES_PEDIDOS = {
    0: "dados/pedidos_json/lote0_conflitoConf.json",
    1: "dados/pedidos_json/lote1.json",
}


#FUNÇÕES
class CliApp:
    
    def __init__(self):
        self.robo_atual: RoboColetor = None
        self.comandos_pendentes = []
        self.carregador = CarregadorArquivos()
        self.registro_auditoria = RegistroAuditoria()
        self.equipe_testes = EquipeDeTestes()


    def menu_criar_robo(self):
        #Menu de criação do robo. Sobrescreve a instância de robo atual.
        print("===============================================")
        print("===== Criação de robo =====")    
        if self.robo_atual is not None:
            resposta = input(f"Robô atual: '{self.robo_atual.nome}'. Deseja sobrescrever? \n Digite o caractere 's' para sim, 'n' para não: ").strip().lower()
            if resposta != 's':
                print("Operação de criação do robo cancelada.")
                return False
            elif resposta != 'n':
                print("Input de cli invalido. Cancelando operação...")
                return False

        #Caso o robo não exista OU o usuario queira sobrescrever:
        print("\n--- Insira o inteiro que corresponde ao arquivo de configuração do robo a ser criado ---")
        for chave, caminho in CONFIGS_ROBOS.items():
            print(f" [{chave}] -> {caminho}")

        opcao = input("Digite o número da configuração: ").strip()

        try:
            if int(opcao) not in CONFIGS_ROBOS:
                print("Seleção inválida!")
                return False
        except:
            raise ErroInput("Input invalido ao selecionar a configuracao do robo.")


        caminho_config = CONFIGS_ROBOS[int(opcao)]

        try:
            with open(caminho_config, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            nome = dados.get("nome", "Coletor-Default")
            tipo_nome = dados.get("tipo_nome", "RoboColetor")
            estrategia_nome = dados.get("estrategia_nome", "RotaDireta")
            area_nome = dados.get("area_nome", "centro_padrao")

            novo_robo = criar_robo_configurado(
                tipo_nome=tipo_nome,
                nome_robo=nome,
                estrategia_nome=estrategia_nome,
                area_nome=area_nome
            )

            novo_robo.adicionar_observador(self.registro_auditoria)
            novo_robo.adicionar_observador(self.equipe_testes)

            self.robo_atual = novo_robo
            print(f"Robô '{self.robo_atual.nome}' foi criado com sucesso usando a seguinte configuração: '{caminho_config}'!")
            return True

        except Exception as e:
            print(f"Erro ao criar robô. Erro capturado {e}")
            return False


    def menu_carregar_pedidos(self):
        print("=================================")
        print("Carregador de pedidos")
        print("Insira o inteiro correspondente ao arquivo de lote")
        for chave, caminho in LOTES_PEDIDOS.items():
            print(f"[{chave}] --> {caminho}")

        opcao = input("Digite o numero do lote: ").strip()

        try:
            if int(opcao) not in LOTES_PEDIDOS:
                print("Erro : A seleção é inválida")
                return False            
        except:
            raise ErroInput('Input invalido ao selecionar pedido para carregar')

        caminho_lote = LOTES_PEDIDOS[int(opcao)]

        try:
            itens = self.carregador.montarPedidosJson(caminho_lote)
            self.comandos_pendentes = self.carregador.criarComandos(itens)
            print(f"[ OK ] Lote '{caminho_lote}' carregado. {len(self.comandos_pendentes)} comando(s) prontos.")
            return True
        except Exception as e:
            print(f"[ ERRO ] Falha ao carregar lote: {e}")
            return False



    def listar_pedidos(self):
        for idx, cmd in enumerate(self.comandos_pendentes):
            print(f" {idx+1}. {cmd}")


    def processar_lote(self):
        #Processa o lote de pedidos.
        if self.robo_atual is None:
            print("É necessário criar um robo para criar um pedido")
            return

        if isinstance(self.robo_atual.modo, ModoAguardandoAnalise):
            print("O robo atual está aguardando a análise da equipe de testes. É necessário finalizar esta análise antes de processar o próximo lote.")
            return

        if not self.comandos_pendentes:
            print("\n[!] Nenhum comando restante na fila.")
            return

        for cmd in self.comandos_pendentes:
            cmd.executar(self.robo_atual)



    def ver_estado_bandeja(self):
        if self.robo_atual is None:
            print("Não há robo ativo atualmente.")
            return
        
        print(f"Estado da Bandeja de {self.robo_atual.nome}")
        print(f"Quantidade: {len(self.robo_atual.bandeja)} / {self.robo_atual.bandeja.QUANTIDADE_MAXIMA}")
        print(f"Itens: {self.robo_atual.bandeja}")


    def analisar_bandeja(self):
        if self.robo_atual is None:
            raise ErroObjetosNaoInicializados("Não há robo ativo atualmente")
    
        if not isinstance(self.robo_atual.modo, ModoAguardandoAnalise):
            print("O robo nao esta aguardando analise.")
            return

        self.ver_estado_bandeja()

        print("A bandeja do robo está aprovada? Digite 's' para sim, e 'n' para não. Para Nenhum dos casos, qualquer outro valor serve.")

        opcao = input("Resposta: ").strip().lower()
        if opcao == 's':
            print("Bandeja aprovada. Robo retoma o ModoColetando.")
            self.robo_atual.aprovarBandeja()
        elif opcao == 'n':
            self.robo_atual.rejeitarBandeja()
            print("Bandeja rejeitada")
        else:
            return 


    def menu_exibir_log(self):
        print("\n===================")
        print("Relatorio de Auditoria")
        print("Deseja exibir o relatorio detalhado?")
        print("Digite 's' para relatorio completo (detalhado) ou 'n' para relatorio resumido:")
        
        opcao = input("Resposta: ").strip().lower()
        if opcao == 's':
            self.registro_auditoria.imprimir_relatório(imprimir_detalhes=True)
        elif opcao == 'n':
            self.registro_auditoria.imprimir_relatório(imprimir_detalhes=False)
        else:
            print("Opcao invalida. Retornando ao menu principal.")




    def iniciar_aplicacao(self):
        print("Inicializando o Robo handler 3000. Por favor, aguarde.")
        print("Programa carregado com sucesso.")
        print("Por favor, comece criando um robo e, depois, escolha um pedido")

        while True:
            self.exibir_menu_principal()
            opcao = input("Escolha uma opcao: ").strip()

            if opcao == "1 : Criar robo":
                self.menu_criar_robo()
            elif opcao == "2 : Carregar um lote de pedidos":
                self.menu_carregar_pedidos()
            elif opcao == "3 : Listar todos os pedidos":
                self.listar_pedidos()
            elif opcao == "4 : Processar lote de pedidos":
                self.processar_lote()
            elif opcao == "5 : Verificar conteúdo da bandeja":
                self.ver_estado_bandeja()
            elif opcao == "6 : Analisar bandeja":
                self.aprovar_bandeja()
            elif opcao == "7 : Verificar LOG do robo":
                self.menu_exibir_log()
            elif opcao == "0":
                print("\nEncerrando o programa.")
                sys.exit(0)
            else:
                print("Opcao invalida. Tente novamente.")
        
        
        

        

