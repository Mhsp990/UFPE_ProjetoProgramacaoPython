# TODO: seus testes de pedido — enunciado, Seção 2.7 (pytest.raises(PedidoInvalido),
# conflito fragil+urgente de Seção 2.4).


import pytest
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.persistencia import CarregadorArquivos


@pytest.fixture
def carregador():
    return CarregadorArquivos()

CASOS_TESTE_PEDIDOS = [
    # Lote 0 (Normal):
    # Robô RotaDireta processa 2 dos 3 items.
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDireto", "estrategia_nome": "RotaDireta", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote0_normal.json",
        2, 3
    ),
    # Mesma ideia do anterior, mas com outra estratégia para area aberta
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDupla", "estrategia_nome": "RotaComDuplaConferencia", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote0_normal.json",
        2, 3
    ),


    # Lote 1 (Frágil):
    # Robô RotaDireta recusa item frágil, processando apenas 1 dos 2 items (pois o item invalido com nossa conf é ignorado)
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDireto", "estrategia_nome": "RotaDireta", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote1_fragil.json",
        1, 2
    ),
    # 
    ( #Desta vez, a estratégia é dupla conferência
        {"tipo_nome": "RoboColetor", "nome": "RoboDupla", "estrategia_nome": "RotaComDuplaConferencia", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote1_fragil.json",
        2, 2 
    ),

    # Lote 2 (Urgente):
    # Robô RotaDireta processa todos os pedidos.
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDireto", "estrategia_nome": "RotaDireta", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote2_urgente.json",
        2, 2
    ),

    # Entretanto, para estrategia de dupla conferência, recusa um dos pedidos urgentes.
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDupla", "estrategia_nome": "RotaComDuplaConferencia", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote2_urgente.json",
        1, 2
    ),

    # Lote 3 (Negativo): Testando o descriptor quantidade valida.
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDireto", "estrategia_nome": "RotaDireta", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote3_negativo.json",
        1, 2
    ),

    # Lote 4 (Conflito Config, Item com fragil e urgente simultâneos):
    (
        {"tipo_nome": "RoboColetor", "nome": "RoboDireto", "estrategia_nome": "RotaDireta", "area_nome": "centro_padrao"},
        "dados/pedidos_json/lote4_conflitoConf.json",
        2, 3
    ),
]




@pytest.mark.parametrize("config_robo, caminho_lote, sucessos_esperados, total_esperado", CASOS_TESTE_PEDIDOS)
def test_processamento_lote_pedidos(carregador, config_robo, caminho_lote, sucessos_esperados, total_esperado):
    robo = criar_robo_configurado(
        tipo_nome=config_robo["tipo_nome"],
        nome_robo=config_robo["nome"],
        estrategia_nome=config_robo["estrategia_nome"],
        area_nome=config_robo["area_nome"]
    )

    itens_json = carregador.montarPedidosJson(caminho_lote)
    comandos = carregador.criarComandos(itens_json)

    sucessos, total = robo.processarComandosColeta(comandos)

    assert total == total_esperado
    assert sucessos == sucessos_esperados