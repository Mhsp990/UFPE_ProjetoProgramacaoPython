# UFPE_ProjectoProgramacaoPython


#O fluxo do algoritmo
O algoritmo funcionará, basicamente, seguindo o seguinte fluxo:
1- Lê um dado persistente (Json), que contém um conjunto de pedidos a serem coletados.
2- "Converter" cada elemento(item) em um ComandoColeta, que contém a lógica para executar a coleta. Desta forma, possuiremos uma LISTA de ComandoColeta no qual iremos iterar sob ela.
    2.1 - ComandoColeta possui as informações :
            Codinome do item, Localização para coletar e a quantidade.
3- ComandoColeta.executar() irá gatilhar o Modo, que decide o comportamento.
4- No modo coleta, isto implica em gatilhar a ESTRATÉGIA.
5- Estratégia recebe, além da referência a instância do robo, informações do item.
6- Considerando a estratégia RotaDireta : Tenta chegar nas coordenadas alvo.
    -No caso de obstáculos, ele tenta se esquivar. Possui um limite de tentativas totais.
7- Ao chegar no local, retorna True. (False caso não). A execução do algoritmo retorna a "ComandoColeta.executar()".
8- Confirmada a chegada, ComandoColeta ativa a coleta do item em Robo.
9- Robo Adiciona a bandeja, que é um objeto Bandeja (que TENTA adicionar).
10- Caso a bandeja esteja cheia, emite o sinal para a equipe analisar.




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
Para as estrategias funcionarem, decidi que elas precisam receber, por padrão, a localização que devem alcançar.
Rota direta : Vai direto até uma pratileira (coordenada).
