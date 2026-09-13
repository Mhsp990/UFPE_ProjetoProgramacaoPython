# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.

import pytest
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoColetando, ModoAguardandoAnalise
from celular_robo.persistencia import CarregadorArquivos


@pytest.fixture
def robo_coletor():
    robo = criar_robo_configurado(
        tipo_nome="RoboColetor",
        nome_robo="RoboTestModos",
        estrategia_nome="RotaDireta",
        area_nome="centro_padrao"
    )
    # Garante que o robô inicia em ModoColetando
    robo.modo = ModoColetando()
    return robo


def test_estado_inicial_robo(robo_coletor):
    assert isinstance(robo_coletor.modo, ModoColetando)


def test_bloqueio_acoes_em_modo_aguardando_analise(robo_coletor):

    robo_coletor.modo = ModoAguardandoAnalise()

    assert robo_coletor.modo.mover(robo_coletor) is False
    assert robo_coletor.modo.coletar(robo_coletor) is False


def test_modo_apos_processar_pedido_normal(robo_coletor):
    """
    Testa se, após processar um lote, entra no estado de analise.
    """
    carregador = CarregadorArquivos()
    
    itens_json = carregador.montarPedidosJson("dados/pedidos_json/lote0_normal.json")
    comandos = carregador.criarComandos(itens_json)
    
    robo_coletor.processarComandosColeta(comandos)

    assert isinstance(robo_coletor.modo, ModoColetando)
    assert len(robo_coletor.bandeja) < robo_coletor.bandeja.QUANTIDADE_MAXIMA


def test_fluxo_aprovacao_bandeja_e_limpeza(robo_coletor):
    """
    Testa a transicao apos um pedido bem sucedido e aprovado.
    """
    carregador = CarregadorArquivos()
    
    itens_json = carregador.montarPedidosJson("dados/pedidos_json/lote0_normal.json")
    comandos = carregador.criarComandos(itens_json)
    robo_coletor.processarComandosColeta(comandos)

    assert len(robo_coletor.bandeja) > 0

    robo_coletor.aprovarBandeja()

    assert len(robo_coletor.bandeja) == 0
    assert isinstance(robo_coletor.modo, ModoColetando)


def test_fluxo_rejeicao_bandeja_mantem_itens(robo_coletor):
    carregador = CarregadorArquivos()
    
    itens_json = carregador.montarPedidosJson("dados/pedidos_json/lote0_normal.json")
    comandos = carregador.criarComandos(itens_json)
    robo_coletor.processarComandosColeta(comandos)
    
    quantidade_antes_rejeitar = len(robo_coletor.bandeja)
    assert quantidade_antes_rejeitar > 0

    robo_coletor.rejeitarBandeja()

    assert len(robo_coletor.bandeja) == quantidade_antes_rejeitar
    assert isinstance(robo_coletor.modo, ModoColetando)