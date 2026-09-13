# Factory — criar_robo_coletor, criar_robo_configurado — enunciado, Seção 2.3.
# (Ver fabrica_base.py — genérico do curso, não editar: criar_robo("RoboColetor",
# ...) já funciona, pode chamar direto ou usar como modelo.)
#
# TODO: implemente aqui. criar_robo_coletor(tipo_nome, ...) a partir do
# _registro (Seção 2.2); criar_robo_configurado combina isso com a validação do
# modelo de features (Seção 2.4).
#
# Contrato mínimo exigido por tests/test_00_fornecido.py (não altere a
# assinatura abaixo sem também atualizar aquele arquivo):
#
#   criar_robo_configurado(tipo_nome, nome, estrategia_nome=..., area_nome=...)


from celular_robo.robo import Robo
from celular_robo.estrategias import RotaColeta
from celular_robo.modos import *

from celular_robo.excecoes import *




def criar_robo(tipo_nome, nome, **kwargs):
    classe = Robo._registro.get(tipo_nome)
    if classe is None:
        disponiveis = ", ".join(sorted(Robo._registro))
        raise ValueError(f"tipo desconhecido: {tipo_nome!r}. Disponíveis: {disponiveis}")
    return classe(nome, **kwargs)



TIPOS_AREA = {
    "centro_padrao": set(),                     
    "area_quarentena": {(0, 5), (1, 5), (2, 5), (3, 5), (4, 5)}
}


ESTRATEGIAS_VALIDAS = set(RotaColeta._registro_rotas.keys())
AREAS_VALIDAS = set(TIPOS_AREA.keys())



#Pedido urgente excluir Dupla conferencia. Area quarentena exclui rota direta.
EXCLUDES = {
    "area_quarentena": {"RotaDireta"}
}

EXCLUDES_PEDIDOS = {
    "urgente": {"RotaComDuplaConferencia"},
    "fragil": {"RotaDireta"}
}




def validar_compatibilidade_robo_pedido(robo, comando_unico):
    #Verifica se o robo EXISTENTE é compatível com os pedidos que serão executados.
    #Para isto, recebe apenas UM comando.
    #Por decisão de arquitetura, executa-se esta validação para cada item do pedido, a fim de verificar quais são possíveis executar.
    e_fragil = getattr(comando_unico, 'fragil', False)
    e_urgente = getattr(comando_unico, 'urgente', False)

    if e_fragil and e_urgente:
        print(f" '{comando_unico.codinome}' possui fragil=True e urgente=True ao mesmo tempo, mas isto é incompatível.")
        return False

    nome_estrategia = robo.estrategia.__class__.__name__

    if e_urgente and nome_estrategia in EXCLUDES_PEDIDOS["urgente"]:
        print(f" '{comando_unico.codinome}' é urgente e exige 'RotaDireta', mas o robô está com a estratégia '{nome_estrategia}'.")
        return False

    if e_fragil and nome_estrategia in EXCLUDES_PEDIDOS["fragil"]:
        print(f" '{comando_unico.codinome}' é frágil e exige 'RotaComDuplaConferencia', mas o robô está com '{nome_estrategia}'.")
        return False

    return True

    



def validar_configuracao(tipo_nome : str, estrategia_nome : str, area_nome : str):
    if tipo_nome not in Robo._registro:
        disponiveis = ", ".join(sorted(Robo._registro))
        raise ConfiguracaoInvalida(f"tipo desconhecido: {tipo_nome!r}. Disponíveis: {disponiveis}")

    if estrategia_nome not in ESTRATEGIAS_VALIDAS:
        disponiveis = ", ".join(sorted(RotaColeta._registro_rotas))
        raise ConfiguracaoInvalida(f"tipo desconhecido: {estrategia_nome!r}. Disponíveis: {disponiveis}")

    if area_nome not in AREAS_VALIDAS:
        raise ConfiguracaoInvalida(f"Tipo de área desconhecido: {area_nome!r}")


    #Agora, validar se não há conflitos de configurações.
    if estrategia_nome in EXCLUDES.get(area_nome,set()):
        #raise ConfiguracaoIncompativel(f"A estrategia {estrategia_nome} é incompatível com area {area_nome}")
        raise ConfiguracaoInvalida(f"A estrategia {estrategia_nome} é incompatível com area {area_nome}") #Devido ao pytest, que espera isso.
    

    
def criar_robo_coletor(tipo_nome: str, nome: str, **kwargs):
    classe = Robo._registro.get(tipo_nome)
    if classe is None:
        disponiveis = ", ".join(sorted(Robo._registro))
        raise ConfiguracaoInvalida(f"tipo desconhecido: {tipo_nome!r}. Disponíveis: {disponiveis}")
    return classe(nome, **kwargs)


def criar_robo_configurado(tipo_nome : str, nome_robo: str, 
                           estrategia_nome : str = "RotaDireta", area_nome : str = "centro_padrao", **kwargs):

    validar_configuracao(tipo_nome, estrategia_nome, area_nome)
    #robo : Robo = criar_robo(tipo_nome= tipo_nome, nome= nome_robo, **kwargs)
    robo : Robo = criar_robo_coletor(tipo_nome= tipo_nome, nome= nome_robo, **kwargs)
    robo.estrategia = RotaColeta._registro_rotas[estrategia_nome]()
    robo.obstaculos = set(TIPOS_AREA[area_nome])
    robo.modo = ModoColetando()
    robo.area_nome = area_nome #Necessario para verificar se as configurações atuais são compatíveis com pedidos requisitados.
    return robo
    

    
