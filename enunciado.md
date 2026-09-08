# Projeto Final — Robô Coletor de Celulares

- **Prazo:** 12/09/2026, 8h59.
- **Entrega:** link do repositório enviado por Google Classroom
- **Formato:** individual.

## Objetivo

Construir um **robô coletor de celulares**: recebe um pedido de coleta (lista de
dispositivos, por codinome e posição), navega pela grade de um laboratório de testes, usa
um sistema de sucção pra pegar cada item, deposita tudo numa bandeja de saída, e notifica a
equipe da bancada de testes quando a bandeja está pronta pra ser retirada. É uma
continuação direta do código ao final do curso — mesma classe `Robo`, mesmo modelo de features, mesma suíte `pytest`, aplicados a um cenário novo.

## 0) Regras gerais

- Python 3.x, PEP 8, f-strings, identificadores de domínio em português.
- Sem dependências externas obrigatórias além de `pytest`, o projeto inteiro roda com
  biblioteca padrão. Não usar bibliotecas externas de FSM pro _State pattern_. A ideia é vocês mesmos construírem o mecanismo à mão.
- Cada mecanismo abaixo corresponde a um conteúdo específico já visto no curso, é aceitável
  (e esperado) seguir a mesma estrutura, adaptando pro domínio novo.
- **Entrega:** repositório Git próprio do aluno (não o repo de aulas), com histórico de commits.

## 1) Domínio e cenário

Um laboratório de testes de dispositivos móveis, testando protótipos ainda não lançados, 
é representado como uma **grade** (igual à do curso, `LADO_GRADE` configurável). 
Prateleiras com os dispositivos (identificados por **codinome interno**) ocupam posições fixas na grade. Algumas áreas podem ter obstáculos 
(equipamento bloqueando passagem, ou a área de quarentena isolada onde ficam as unidades 
com defeito). O `RoboColetor` recebe um **pedido de coleta**, que consiste de uma lista de 
dispositivos (codinome, posição, quantidade — e outros campos por item
detalhados na Seção 2.4), e com base no pedido, navega até cada
posição, usa o **sistema de sucção** pra pegar o item, e ao final deposita tudo numa
**bandeja**. Quando a bandeja está completa, o robô notifica a equipe da bancada de testes
(_Observer_): sinal de que o lote está pronto pra ser retirado. A bandeja está completa
quando todos os itens do pedido foram coletados nas quantidades solicitadas. Só depois da
equipe aprovar o lote o robô pode começar um pedido novo.


## 2) Escopo obrigatório — `RoboColetor`

### 2.1 Fundamentos de OO e descriptors

- `Robo` já vem pronto em `robo_base.py` (`starter`, Seção 3) — posição (`x`, `y`) via
  descriptor `Coordenada` incluída, não precisa reescrever. `RoboColetor(Robo)`
  reaproveita isso por herança.
- Um descriptor de quantidade novo (`QuantidadeValida` ou similar, mesmo protocolo de
  `Percentual`/`Coordenada`) validando que a quantidade coletada de um item nunca é
  negativa nem passa do pedido.
- Métodos especiais onde fizer sentido (`__str__`/`__repr__` pro robô, `__len__` pra
  bandeja — quantos itens já foram coletados, e assim por diante).
  (`Bandeja` pode ser uma classe própria, com seu próprio `__len__`, ou um
  atributo interno de `RoboColetor` — ex. um `dict` codinome→quantidade
  coletada. A escolha é livre; documente no README qual foi adotada.)

### 2.2 Metaprogramação

- `RoboColetor` já sai registrado em `Robo._registro` assim que herda de `Robo`. 
  O `__init_subclass__` vem pronto em `robo_base.py`, não precisa reescrever. Mesmo com um
  tipo só no escopo obrigatório, é esse registro que a extensão (Seção 7) vai aproveitar sem
  editar nada.
- `ComandoColeta`, `EquipeDeTestes`/`RegistroAuditoria` e `ModoColetando`/
  `ModoAguardandoVerificacao` herdam direto de `Comando`/`Observador`/`ModoOperacao`
  (`comandos_base.py`/`observadores_base.py`/`modos_base.py`) — o `__init_subclass__` de lá
  já registra suas classes junto com os exemplos genéricos do curso.
- **Exceção — Strategy:** aqui o mecanismo é escrito por você numa segunda hierarquia, em vez
  de herdar de `Estrategia`: uma base `RotaColeta` com `__init_subclass__` próprio
  registrando `RotaDireta`/`RotaComDuplaConferencia` num `_registro_rotas` —
  `ESTRATEGIAS_VALIDAS = set(_registro_rotas)` deriva do registro, não é digitado à mão
  (mesmo raciocínio de `TIPOS_VALIDOS`, já usado pro robô). Motivo de ser diferente:
  `ESTRATEGIAS_VALIDAS` precisa conter só as duas rotas de coleta — herdar de `Estrategia`
  contaminaria o conjunto com `EstrategiaPadrao`/`Esquiva`/`EstrategiaZigzag` (movimentação).

### 2.3 Design patterns — exercitar os cinco

- **Strategy** — pelo menos duas rotas de coleta: `RotaDireta` (vai direto até cada
  prateleira) e `RotaComDuplaConferencia` (revalida cada item antes de depositar na
  bandeja — mais lenta, mais segura pra aparelhos frágeis). Trocável em
  `robo.estrategia`, igual `EstrategiaPadrao`/`EstrategiaEsquiva`.
- **Command** — cada item do pedido vira um `ComandoColeta(Comando)`
  (`codinome, posicao, quantidade`), com `.executar(robo)` **e `.desfazer(robo)`** (remove o
  item da bandeja, decrementa a contagem coletada) — o _undo_ que o _Command_ do curso ainda
  não tinha explorado. O pedido inteiro é uma lista de comandos executada em sequência,
  guardada em histórico (igual `_historico_comandos`).
- **Factory** — `criar_robo_coletor(tipo_nome, ...)` a partir de `_registro`, igual
  `criar_robo` do curso.
  `criar_robo_configurado` é a função pública que valida a config (via
  `validar_configuracao`, Seção 2.4) e então chama `criar_robo_coletor` —
  a CLI deve usar sempre `criar_robo_configurado`; `criar_robo_coletor` é
  o nível mais baixo, direto no registro, chamado internamente.
- **Observer** — pelo menos dois observadores, ambos `Observador`: `EquipeDeTestes` (reage a
  `"bandeja_pronta"`) e `RegistroAuditoria` (loga **todo** evento — coleta, bandeja pronta,
  pedido rejeitado — igual `RegistroEventos`, mas pensando em trilha de auditoria, não só
  depuração).
- **State** — pelo menos dois modos, ambos `ModoOperacao`: `ModoColetando` (delega pra
  `self.estrategia`, igual `ModoExplorando`) e `ModoAguardandoVerificacao` (recusa iniciar
  nova coleta até a bandeja ser aprovada, igual `ModoCarregando` recusando `mover()`). A
  transição de `ModoColetando` pra `ModoAguardandoVerificacao` acontece **via Observer**,
  quando a bandeja fica completa — mesmo mecanismo de `MonitorBateria` trocando pra
  `ModoCarregando`, quando Observer e State foram conectados no curso.
  Se a equipe **rejeitar** a bandeja, o robô retorna a `ModoColetando` para
  o mesmo pedido — os itens já coletados permanecem na bandeja (não é
  necessário reprocessar). A rejeição em si é registrada via
  `RegistroAuditoria`, não como reprocessamento automático.

### 2.4 Modelo de features / LPS

- Pelo menos duas dimensões alternativas: tipo de robô (`RoboColetor`, mesmo com um tipo
  só no MVP) e estratégia de rota (Seção 2.3).
- Uma terceira dimensão, **tipo de área** (mesmo mecanismo de "tipo de grade" do capstone
  do curso): pelo menos `"centro_padrao"` e `"area_quarentena"`, cada uma resultando num
  `robo.obstaculos` diferente — não é só um rótulo usado na validação (Seção 2.4/2.5).
  - `"centro_padrao"`: `robo.obstaculos` vazio, sem barreiras.
  - `"area_quarentena"`: `robo.obstaculos` com pelo menos uma posição bloqueada — o
    corredor isolado onde ficam as unidades com defeito, de fato intransponível pro
    sensor/`avancar()` do robô, não só uma barreira decorativa.
- Uma quarta dimensão, **urgência do item** (campo `urgente` no pedido, ao lado de
  `fragil`): `urgente=True` exige `RotaDireta` — testes urgentes não esperam a segunda
  validação.
- **`requires`**: um item marcado como `fragil=True` no pedido exige que o robô esteja
  configurado com `RotaComDuplaConferencia` — o sistema de sucção não pega um protótipo
  frágil na rota rápida.
- **`excludes`**: a área `"area_quarentena"` exclui `RotaDireta` — corredor isolado não
  permite trajeto sem revalidação.
- **Conflito item a item:** `fragil=True` e `urgente=True` no mesmo item é contraditório
  (exige `RotaComDuplaConferencia` e `RotaDireta` ao mesmo tempo). Decida e documente no
  README qual exceção recusa isso — `PedidoInvalido` (problema no item) ou
  `ConfiguracaoInvalida` (problema na combinação) são ambas defensáveis; o que importa é
  ser consistente e ter um teste cobrindo a escolha (Seção 2.7).
- **Conflito entre itens do mesmo pedido:** se o pedido tiver ao menos um
  item `urgente=True` e ao menos um item `fragil=True` (mesmo que não seja
  o mesmo item), a estratégia configurada no robô não consegue satisfazer
  os dois ao mesmo tempo — `robo.estrategia` é única por robô. Decida e
  documente no README como tratar isso (recusar o pedido inteiro com
  `PedidoInvalido` antes de processar qualquer item é a opção mais simples,
  mas alternativas são aceitáveis desde que consistentes e testadas). Essa
  checagem acontece ao carregar/validar o **pedido**, não em
  `validar_configuracao` — que só enxerga o JSON de config do robô, sem
  visibilidade dos itens do pedido.
- `ConfiguracaoInvalida` recusando a combinação antes de qualquer robô ser instanciado —
  mesmo padrão de `validar_configuracao`/`criar_robo_configurado` já visto no curso.

### 2.5 Exceções com hierarquia (mencionado desde a D1, aprofundado aqui)

- `ErroColeta(Exception)` como base.
- `ConfiguracaoInvalida(ErroColeta)` — problema na configuração do robô/rota/área (igual
  Seção 2.4).
- `PedidoInvalido(ErroColeta)` — problema no **conteúdo** do pedido em si: codinome não
  encontrado no lote, quantidade pedida maior que o disponível, pedido vazio. Uma
  hierarquia de duas exceções deixa quem chama decidir se quer tratar os dois casos juntos
  (`except ErroColeta`) ou separado.
- **De onde vem "o lote" pra validar contra:** o JSON do pedido (Seção 2.6) só traz o
  *nome* do lote (`"lote": "Lote de Testes #482"`) — a relação codinome→quantidade
  disponível não é fornecida, você decide e documenta no README como representá-la (ex.:
  um `dict` no módulo que faz a validação, ou um arquivo próprio em `dados/`). Não é uma
  peça faltando no esqueleto: `dados/` vem vazia de propósito, os JSONs de exemplo são
  parte da sua entrega (Seção 5).
- **Pedido com itens mistos:** se um pedido tiver vários itens e só **um** for inválido
  (ex.: codinome inexistente), decida e documente no README — rejeita o pedido inteiro, ou
  processa os itens válidos e pula o inválido (registrando o motivo, ex. via
  `RegistroAuditoria`)? As duas são defensáveis; o que importa é ser consistente e ter um
  teste cobrindo a escolha.

### 2.6 Configuração e persistência

- O pedido de coleta é um registro JSON:
  ```json
  {
    "lote": "Lote de Testes #482",
    "itens": [
      {"codinome": "Projeto Aurora", "quantidade": 2, "posicao": [3, 4],
       "fragil": false, "urgente": true},
      {"codinome": "Projeto Vesper", "quantidade": 1, "posicao": [7, 2],
       "fragil": true, "urgente": false}
    ]
  }
  ```
  E o config do robô, `config_robo_exemplo.json`:
  ```json
  {
    "tipo_nome": "RoboColetor",
    "nome": "Coletor-1",
    "estrategia_nome": "direta",
    "area_nome": "centro_padrao"
  }
  ```
- `montar_robo_de_config(config)` e `montar_pedido_de_json(caminho)` — mesmo par de
  funções do curso (`montar_robo_de_config`/`montar_frota_de_json`), adaptado:
  um arquivo configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.
  (Note a assimetria intencional: `montar_robo_de_config` recebe um `dict`
  já carregado, `montar_pedido_de_json` recebe um caminho de arquivo — mesmo
  padrão usado no par equivalente do curso. Não é inconsistência.)

### 2.7 Testes (`pytest`)

- **Fornecido pelo professor** em `tests/test_00_fornecido.py`, já dentro da estrutura de
  código inicial (Seção 3) — **não editar**: uma fixture (`robo_padrao`) e **2 testes já escritos**,
  um caminho feliz e um `pytest.raises(ConfiguracaoInvalida)` cobrindo a regra de
  `excludes` de `"area_quarentena"` (Seção 2.4). Rodando `pytest -v` assim que vocês recebem o
  esqueleto, os dois **quebram** — as funções ainda não existem. É o esperado, não um bug
  nem um problema de setup (o `pyproject.toml` do starter já resolve o import do pacote);
  eles ficam verdes conforme o projeto é construído (ver Seção 8, item 5).
- **Criados por você, além dos 2 fornecidos:** pelo menos 4 testes novos, cobrindo:
  - `pytest.raises(PedidoInvalido)` pra um pedido com codinome inexistente;
  - `@pytest.mark.parametrize` cobrindo pelo menos 3 combinações de
    estratégia×área, no mesmo espírito de `test_contrato_criar_ou_recusar` (ver exercício
    avançado da Aula 16 do seu repositório de exercícios, que confere o contrato inteiro —
    não só válido/inválido, mas que o robô resultante tem exatamente o tipo/estratégia
    esperados);
  - um teste confirmando que a transição `ModoColetando`→`ModoAguardandoVerificacao`
    acontece sozinha quando a bandeja completa (Observer disparando State) — dica: não
    precisa simular uma coleta de verdade até a bandeja encher; notifique o evento
    direto (`robo.notificar("bandeja_pronta", ...)`, mesma técnica do exercício de
    Observer com injeção de evento) e confira a reação;
  - um quarto teste à sua escolha cobrindo alguma regra de negócio do domínio (candidatos
    naturais: o conflito `fragil`+`urgente` de Seção 2.4, ou confirmar que um robô criado
    com `area_nome="area_quarentena"` tem pelo menos uma posição em `robo.obstaculos`).

## 3) Estrutura de projeto

Vocês recebem esta estrutura pronta (pasta `celular_robo/` do material de starter) — copie
ela inteira como raiz do seu repositório. Cada arquivo em `src/celular_robo/` só tem um
comentário `# TODO`, sem nenhuma lógica implementada; a divisão de classes por arquivo é a sugerida abaixo, mas caso prefira reorganizar, justifique no README.

```
celular_robo/
├── README.md                  # setup, como rodar, mapeamento pra aulas da disciplina
├── requirements.txt           # só pytest
├── dados/
│   ├── pedido_coleta_exemplo.json
│   └── config_robo_exemplo.json
└── src/
    └── celular_robo/
        ├── __init__.py
        ├── robo_base.py         # Robo, já fornecido — não editar
        ├── estrategias_base.py  # Strategy genérico do curso, fornecido — não editar
        ├── comandos_base.py     # Command genérico do curso, fornecido — não editar
        ├── observadores_base.py # Observer genérico do curso, fornecido — não editar
        ├── modos_base.py        # State genérico do curso, fornecido — não editar
        ├── fabrica_base.py      # criar_robo, fornecido — não editar (reutilizável)
        ├── robo.py             # RoboColetor, QuantidadeValida
        ├── estrategias.py      # RotaColeta (base, com __init_subclass__ próprio),
                                 # RotaDireta, RotaComDuplaConferencia
        ├── modos.py            # ModoColetando, ModoAguardandoVerificacao
        ├── comandos.py         # ComandoColeta
        ├── observadores.py     # EquipeDeTestes, RegistroAuditoria
        ├── excecoes.py         # ErroColeta, ConfiguracaoInvalida, PedidoInvalido
        ├── modelo_features.py  # TIPOS_VALIDOS, REQUER, EXCLUI, validar_configuracao
        ├── fabrica.py          # criar_robo_coletor, criar_robo_configurado
        ├── persistencia.py     # montar_robo_de_config, montar_pedido_de_json
        └── cli.py              # menu ou argparse
└── tests/
    ├── conftest.py
    ├── test_00_fornecido.py       # 2 testes prontos do professor (Seção 2.7) — não editar
    ├── test_configuracao.py
    ├── test_pedido.py
    └── test_fluxo_completo.py
```

## 4) CLI

Menu interativo simples:
listar pedido carregado, processar pedido, ver estado da bandeja, aprovar/rejeitar
retirada da equipe de testes. `argparse` é aceito como alternativa pra quem preferir.

## 5) Entregáveis

1. Código-fonte organizado (estrutura de Seção 3 ou equivalente justificada no `README`).
2. `README.md` — como rodar, decisões de projeto, e uma seção curta mapeando **cada**
   mecanismo da disciplina pro arquivo/classe correspondente (facilita a correção).
3. `requirements.txt`.
4. `dados/pedido_coleta_exemplo.json` + `dados/config_robo_exemplo.json`.
5. Suíte `pytest` (Seção 2.7) — `pytest -v` precisa rodar limpo a partir da raiz do projeto.
6. Opcional: vídeo curto (≤ 3 min) demonstrando o fluxo completo.

## 6) Rubrica (100 pts)

| Critério | Pontos |
|---|---|
| OO fundamentals + descriptors (validação de posição/quantidade) | 10 |
| Metaprogramação (`__init_subclass__`/registro automático — robôs **e** rotas) | 15 |
| Design patterns — Strategy, Command, Factory, Observer, State | 30 |
| Modelo de features / LPS (`requires`/`excludes`, 4 dimensões, validador antes de instanciar) | 15 |
| Configuração/persistência (JSON → robô/pedido) | 10 |
| Testes `pytest` (4 seus além dos 2 fornecidos ficarem verdes) | 10 |
| Qualidade & CLI (tipagem, docstrings, hierarquia de exceções, CLI funcional) | 10 |
| **Total** | **100** |

## 7) Extensão opcional — `RoboTransportador` (+10 pts, bônus)

Um segundo tipo de robô, registrado no mesmo `_registro` sem precisar tocar no código do
`RoboColetor` (prova de que a metaprogramação de Seção 2.2 realmente generaliza). Quando a
equipe de testes aprova a bandeja, um Observer dispara a criação/notificação de um
`RoboTransportador`, que leva os itens aprovados até o ponto de retirada do carrinho
robótico (o carrinho em si continua fora de escopo). Pontos extra por:

- reaproveitar `TIPOS_VALIDOS = set(_registro)` sem editar nada à mão (mesmo mecanismo já
  visto no curso);
- uma restrição nova de `requires`/`excludes` envolvendo o `RoboTransportador` (ex.:
  transportador exclui `"area_quarentena"` — não entra na área de unidades com defeito);
- testes cobrindo o handoff coletor→transportador.

## 8) Passo a passo para iniciar

0. Antes de escrever qualquer código: rode `pytest -v` no esqueleto fornecido e veja os 2
   testes de `test_00_fornecido.py` falharem (import/atributo faltando) — é o ponto de
   partida do projeto.
1. `RoboColetor` mínimo: posição com descriptor, `avancar()`/`girar()` reaproveitando a
   grade do curso.
2. Uma estratégia (`RotaDireta`) e `ComandoColeta.executar()` funcionando pra **um** item.
3. `EquipeDeTestes` (Observer) recebendo uma notificação de bandeja pronta, mesmo que
   "pronta" comece como "coletei 1 item" (ajuste o critério depois).
4. `ModoColetando`/`ModoAguardandoVerificacao`, com a transição disparada pelo Observer.
5. Modelo de features com as duas primeiras dimensões (tipo, estratégia) e o validador —
   os 2 testes fornecidos devem ficar verdes por volta daqui.
6. Segunda estratégia, `ComandoColeta.desfazer()`, área com obstáculos, quarta dimensão
   (`urgente`), `requires`/`excludes`, `PedidoInvalido`, JSON, CLI.
7. Seus 4 testes próprios (Seção 2.7) — pode escrever em paralelo com o passo 6, não só no
   fim.