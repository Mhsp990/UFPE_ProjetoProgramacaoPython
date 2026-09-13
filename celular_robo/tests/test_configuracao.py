# TODO: seus testes de configuração/LPS — enunciado, Seção 2.7 (pytest.raises,
# @pytest.mark.parametrize cobrindo estratégia×área).

#Os testes abaixo testam a configuração do robo.


import pytest
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.excecoes import ConfiguracaoInvalida

CASOS_CONFIG_VALIDAS = [
    ("RoboColetor", "Coletor-padrao", "RotaDireta", "centro_padrao"),
    ("RoboColetor", "Coletor dupla conferencia", "RotaComDuplaConferencia", "area_quarentena"),
    ("RoboColetor", "Coletor dupla conferencia em area aberta", "RotaComDuplaConferencia", "centro_padrao"),
]

# Casos inválidos: espera-se a exceção ConfiguracaoInvalida
CASOS_CONFIG_INVALIDAS = [
    ("RoboColetor", "Coletor incompativel", "RotaDireta", "area_quarentena"),
    ("NaoExiste", "Coletor-padrao", "RotaDireta", "centro_padrao"),
    ("RoboColetor", "Coletor-EstrategiaInexistente", "Inexistente", "centro_padrao"),
    ("RoboColetor", "Coletor-areaInexistente", "RotaDireta", "areaInexistente"),
]



@pytest.mark.parametrize("tipo_nome, nome, estrategia_nome, area_nome", CASOS_CONFIG_VALIDAS)
def test_criar_robo_configuracao_valida(tipo_nome, nome, estrategia_nome, area_nome):
    robo = criar_robo_configurado(
        tipo_nome=tipo_nome,
        nome_robo=nome,
        estrategia_nome=estrategia_nome,
        area_nome=area_nome
    )
    assert robo.nome == nome
    assert robo.estrategia.__class__.__name__ == estrategia_nome
    assert robo.area_nome == area_nome


@pytest.mark.parametrize("tipo_nome, nome, estrategia_nome, area_nome", CASOS_CONFIG_INVALIDAS)
def test_criar_robo_configuracao_invalida(tipo_nome, nome, estrategia_nome, area_nome):
    with pytest.raises(ConfiguracaoInvalida):
        criar_robo_configurado(
            tipo_nome=tipo_nome,
            nome_robo=nome,
            estrategia_nome=estrategia_nome,
            area_nome=area_nome
        )