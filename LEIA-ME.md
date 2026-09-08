# Starter — Projeto Final

Copie a pasta `celular_robo/` inteira pra ser a raiz do seu repositório do
projeto (ver estrutura sugerida no enunciado, Seção 3).

## O que já vem pronto

- **Estrutura de pastas** (`src/celular_robo/`, `tests/`, `dados/`) e um
  arquivo por módulo. A divisão de classes por arquivo é a sugestão do
  enunciado; se preferir organizar diferente, é só justificar no README (ele
  já vem com essa seção).
- Seis arquivos `*_base.py` — **não editar**: o `Robo` do curso inteiro, já
  pronto e testado, separado nos mesmos "papéis" que o resto do projeto usa
  pros seus próprios patterns (um arquivo por pattern, não tudo empilhado):
  - `robo_base.py` — a classe `Robo` (descriptors, `Direcao`, Sensor/Radio,
    `__init_subclass__`/`_registro`, `avancar`/`girar`). `RoboColetor` (em
    `robo.py`) herda daqui.
  - `estrategias_base.py`, `comandos_base.py`, `observadores_base.py`,
    `modos_base.py` — os Strategy/Command/Observer/State **genéricos** do
    curso (movimentação livre, bateria). Não têm relação com o domínio de
    coleta — só existem porque `Robo` usa um deles (`EstrategiaPadrao`,
    `ModoExplorando`) como valor padrão. Os seus próprios
    Strategy/Command/Observer/State vão nos arquivos **sem** `_base`
    (`estrategias.py`, `comandos.py`, `observadores.py`, `modos.py`).
  - `fabrica_base.py` — o Factory genérico, `criar_robo(tipo_nome, nome,
    **kwargs)`. Diferente dos quatro acima, este **é** diretamente útil pro
    domínio: `criar_robo("RoboColetor", nome, **kwargs)` já funciona (já que
    `Robo._registro` só tem `RoboColetor`). Pode chamar direto de dentro do
    seu `criar_robo_coletor` (em fabrica.py), ou reimplementar — os dois são
    aceitos.

  As quatro bases de Strategy/Command/Observer/State (`Estrategia`,
  `Comando`, `Observador`, `ModoOperacao`) são todas `ABC` +
  `@abstractmethod`, cada uma com seu próprio `_registro` populado via
  `__init_subclass__` — mesmo mecanismo de `Robo._registro`. São 4 exemplos
  prontos do idioma pra estudar antes de escrever o seu (a base
  `RotaColeta`, enunciado, Seção 2.2).

  Todo mundo da turma parte da mesma base. As três subclasses de exemplo 
  (`RoboVeloz`/`RoboExplorador`/ `RoboBlindado`) foram removidas de propósito, 
  pra não poluir `Robo._registro` com tipos que não são deste projeto.
- Todos os outros arquivos de `src/celular_robo/` (sem `_base` no nome) têm
  só um comentário `# TODO` apontando pra seção do enunciado — **sem
  nenhuma lógica implementada**, essa parte é sua.
- `pyproject.toml` com `pythonpath = ["src"]` — sem isso, `pytest` não acha o
  pacote `celular_robo` (ele mora em `src/`, não na raiz). Não precisa
  instalar nada, só rodar `pytest -v` na raiz do projeto.
- `requirements.txt` com `pytest`.
- `tests/test_00_fornecido.py` — **não editar**: 2 testes já escritos (uma
  fixture + um caminho feliz + um `pytest.raises(ConfiguracaoInvalida)`),
  ver "Testes" no enunciado (Seção 2.7). Os outros quatro arquivos em `tests/`
  (`conftest.py`, `test_configuracao.py`, `test_pedido.py`,
  `test_fluxo_completo.py`) são só stubs com `# TODO` — os testes (e
  fixtures próprias) ali são seus.

## Sobre `__init__.py` e imports

Isso é novo em relação às aulas: lá, cada arquivo era carregado avulso
(`importlib`/execução direta). Aqui, `celular_robo/` é um **pacote** Python
de verdade, e é isso que permite escrever `from celular_robo.fabrica import
criar_robo_configurado` (como em `test_00_fornecido.py`) em vez de apontar
pro caminho do arquivo.

`__init__.py` é o arquivo que marca uma pasta como pacote — sem ele,
`src/celular_robo/` seria só uma pasta comum, e o import acima não
funcionaria. Ele já vem **vazio** no starter, e pode continuar vazio: você
não precisa escrever nada nele pra este projeto, só deixar ele existir onde
está.

## Antes de escrever qualquer código

Rode `pytest -v` na raiz. Os 2 testes de `test_00_fornecido.py` vão falhar
com `ImportError: cannot import name 'criar_robo_configurado'`. Isto é o
esperado (a função ainda não existe), não um problema de setup. Eles ficam
verdes conforme você implementa o projeto.
