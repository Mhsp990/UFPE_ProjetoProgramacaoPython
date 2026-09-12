# Observer — EquipeDeTestes, RegistroAuditoria — enunciado, Seção 2.3.
#
# Herde de `Observador` (observadores_base.py — ABC com registro automático):
#
#   from celular_robo.observadores_base import Observador
#
# TODO: implemente aqui. EquipeDeTestes(Observador) reage a "bandeja_pronta";
# RegistroAuditoria(Observador) loga todo evento (coleta, bandeja pronta,
# pedido rejeitado), pensando em trilha de auditoria, não só depuração.

from celular_robo.observadores_base import Observador
from celular_robo.modos import ModoAguardandoAnalise


class EquipeDeTestes(Observador):
    #Observa (reage) as seguintes mudanças:
    #   Quando a bandeja está cheia.
    #       O que faz: Avalia se aprova ou rejeita a bandeja atual.
    def atualizar(self, evento, **dados):
        if evento == "bandeja_pronta":
            robo = dados.get('robo')

            robo.modo = ModoAguardandoAnalise()
            print(f'Bandeja do robo {robo} está pronta para ser analisada. Entrando em modo ANALISE')
            


class RegistroAuditoria(Observador):
    #Registra todos os eventos, independente de quais sejam.
    def __init__(self):
        self.eventos = []

    def atualizar(self, evento, **dados):
        self.eventos.append((evento, dados))


    def imprimir_relatório(self, imprimir_detalhes : bool = False):
        print("----- Imprinindo LOG de auditoria -----")

        for index, (evento, dados) in  enumerate(self.eventos):
            detalhes = ", ".join(f"{k}={v}" for k, v in dados.items())
            print(f'Evento {index} -->  {evento}')
            if imprimir_detalhes:
                print(f'Detalhes do evento : {detalhes}') 
        print("---------------------------\n")

    def tamanho_relatorio(self):
        return len(self.eventos)
