# Robô Coletor de Celulares

## Setup

Além do que já feito pronto no projeto base, não foi necessário instalar nenhuma dependência além do pytest.
Além disso, não utilizei bibliotecas externas.
OBS: Usei o venv + install do pytest.


## Como rodar

TODO: como rodar a CLI e como rodar `pytest -v`.
Para rodar o cli, acesse o arquivo cli.py e rode o script presente nele.

Os arquivos de persistencia, que são usados para criar o robo ou o pedido, estão na pasta 'dados'.
Cada arquivo (exemplo lote0_conflitoConf.json) representa um lote completo de pedido. O pós fixo do nome do arquivo indica o tipo de caso que se espera para aquele arquivo. Por exemplo, no lote0_conflitoConf.json, espera-se que ocorra um conflito, pois haverão pedidos frágeis e urgentes simultaneamente.

Neste caso, quando o CLI pedir o seu input, basta digitar o numero que está no nome do arquivo.
exemplo : lote2_exagerado.json ---> inserir 2
          lote1.json           ---> inserir 1

mesma ideia para configuração do robo.


Para a fabrica, os nomes das classes são traduzidos de forma "direta".
Portanto, caso o robo desejado use a estratégia rota direta, deve-se inserir:
RotaDireta
ou, similarmente
RotaComDuplaConferencia

Motivo : É assim que o init subclass está trabalhando. Desta forma, torna-se desnecessário inserir os nomes esperados manualmente.

IMPORTANTE : Devido aos testes pre prontos, necessitei alterar as strings passadas.



Ademais, em certos momentos, será esperado o prompt do usuário para aceitar o rejeitar a bandeja. Neste caso, basta seguir a legenda do CLI.


## Decisões de projeto

TODO: decisões de design tomadas — em especial onde havia mais de um jeito
razoável de resolver (ex.: qual exceção recusa o conflito `fragil`+`urgente`,
Seção 2.4 do enunciado).

OBS : Para outros detalhes, recomendo ver o read-me mais "externo", na pasta base do projeto.
Lá, eu explico o fluxo do algoritmo, algumas classes e outras informações que considero importante para facilitar o entendimento do algoritmo.


Para lidar com quantidades invalidas no pedido, criou-se a excessão PedidoInvalido.
Para lidar com configurações invalidas ao tentar fabricar um robo, usa-se a excessão ConfiguracaoInvalida.
Entretanto, caso a configuração seja válida (Classe e estratégia escolhida existem), mas há incompatibilidade com outros fatores, tal como estratégias que não podem ser usadas em certas áreas ou pedidos, usa-se a excessão ConfiguracaoIncompativel.


Sobre lidar com fragil e urgente, eu pensei em duas soluções:
    1 - Trocar a estratégia, para dar "match" no tipo de pedido. Desta forma, para cada tipo de pedido, usaria-se a estratégia adequada, caso a ÁREA (e outros fatores) em questão permitisse.
    2 - Levantar o raise, caso algum item presente no pedido seja incompativel. Desta forma, ao receber um pedido, basta comparar as configurações do robo atual com o tipo de pedido.

Optei pela opção 2, pois simplifica o código, já que torna-se desnecessário armazenar o tipo de área escolhida para comparar e, também, evita outras checagens extras para evitar que uma estratégia indesejada seja adotada.
Ademais, exigira algumas mudanças na arquitetura para que fique mais "eficiente". Por exemplo: Consideraria que existe N configurações a serem utilizadas e, ao receber um pedido (um pedido do lote de pedidos), o algoritmo verificaria qual configuração é adequada.







## Mapeamento pra aulas da disciplina

TODO: uma tabela curta ligando cada mecanismo (descriptors, `__init_subclass__`,
os 5 design patterns, LPS, exceções, persistência, testes) ao arquivo/classe
correspondente — facilita a correção.


EXCEÇÕES
As exceções criadas podem ser encontradas principalmente em:
    -Excecoes.py


DESCRIPTORS
Os descriptors podem ser encontrados principalmente em:
    -Coordenadas : Já vem do robo base.
    -QuantidadeValida : Implementado em robo.py e utilizado na classes "ItemLotePedido" e "Bandeja" para impedir quantidades inválidas.


### __init_subclass__
Além dos que já foram implementados no projeto base, temos:
    - Na classe estratégia, para registrar automaticamente todas as estratégias criadas.



PATTERNS
Obs : Em caso de dúvida de COMO foi implementado, a relação entre os patterns foi explicada no read-me mais externo (na pasta base do projeto). Ademais, há comentários no código de cada classe.

Comando pattern
    - Comando de coleta --> class CommandColeta

Estrategy pattern
    - No arquivo estrategias.py

Observadores
    -No arquivo observadores.py. Seu uso pode ser encontrado, principalmente, em robo.py.

State
    -No arquivo modos.py. Seu uso é encontrado principalmente nos execute do Command pattern + observador

Fabrica
    -No arquivo fabrica.py. Uso encontrado principalmente na classe CLI, para usar o input do usuário para criar o robo.



LPS
Tudo relacionado a LPS, tal como o algoritmo para criar e as regras (exceções, requer, area, etc) podem ser encontrados no arquivo factory.py


TESTES
Todos os arquivos de testes estarão na pasta tests.