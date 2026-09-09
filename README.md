# UFPE_ProjectoProgramacaoPython

Para este projeto, adotou-se as seguintes arquiteturas:

ITEM PEDIDO
A classe item pedido irá representar UM pedido da lista de pedidos.
Permite implementar descriptors. Como por exemplo, o descriptor QuantidadeValida
Portanto, ao ler um arquivo externo (por exemplo) contendo a lista de pedidos,
estes serão transformados em objetos desta classe.

BANDEJA
Bandeja será uma classe que representará tudo que a bandeja está "carregando".
Portanto, o robo coletor poderá "manipular" o conteúdo de bandeja através de métodos dedicados.
Bandeja possuirá uma lista dos itens armazenados, além de que usará o descriptor "QuantidadeValida".
OBS : Estou supondo que basta adicionar o item coletado via sucção em bandeja "diretamente", sem precisar de movimentos na grade até a localização da bandeja.


ESTRATÉGIAS
Rota direta : Vai direto até uma pratileira (coordenada).
