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


from celular_robo.robo_base import Robo
from celular_robo.estrategias import RotaColeta
from celular_robo.modos import *



EXCLUI = {
    "F"
}



def criar_robo_coletor(tipo_nome : str , tipo_estrategia : str, tipo_modo: str ,nome : str, **kwargs):

    #Registro retorna objetos do tipo classe.
    classe = Robo._registro.get(tipo_nome) 
    estrategia = RotaColeta._registro_rotas.get(tipo_estrategia)
    modo = ModoColetando._registro.get(tipo_modo)

    
    #Validando se os tipos (classes) existem.
    if classe is None:
        disponiveis = ", ".join(sorted(Robo._registro))
        raise ValueError(f"tipo desconhecido: {tipo_nome!r}. Disponíveis: {disponiveis}")
    

    if estrategia is None:
        disponiveis = ", ".join(sorted(RotaColeta._registro))
        raise ValueError(f"tipo desconhecido: {tipo_estrategia!r}. Disponíveis: {disponiveis}")


    if modo is None: #
        disponiveis = ", ".join(sorted(ModoOperacao._registro))
        raise ValueError(f"tipo desconhecido: {tipo_modo!r}. Disponíveis: {disponiveis}")


    #Validando se as configurações são válidas
    if validar_robo_coletor():
        return classe(nome, estrategia = estrategia, **kwargs)
    else:
        raise ValueError(f"Não foi possível criar o robo devido a configurações inválidas. Resolva-as e tente novamente.")


def validar_robo_coletor() -> bool:
    pass
