# Hierarquia de exceções — enunciado, Seção 2.5.
#
# TODO: implemente aqui. ErroColeta(Exception) como base;
# ConfiguracaoInvalida(ErroColeta) e PedidoInvalido(ErroColeta) como as duas
# subclasses (ver Seção 2.5 pra critério de qual usar em cada caso).

class ErroColeta(Exception):
    pass

class ConfiguracaoInvalida(ErroColeta):
    #Chamado quando a configuração do robo está incorreta. (Usado na LPS)
    pass

class PedidoInvalido(ErroColeta):
    #Ocorre quando o pedido é invalido. Exemplos:
    #   Codinome de lote invalido;
    #   Quantidade pedida maior que a existente;
    #   Valor pedido invalido : Itens com quantidade negativas ou pedidos vazios.
    pass