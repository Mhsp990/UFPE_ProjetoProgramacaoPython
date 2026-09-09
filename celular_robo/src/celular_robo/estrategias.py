# Strategy — RotaDireta, RotaComDuplaConferencia — enunciado, Seção 2.3.
# (Não confundir com estrategias_base.py — genérico do curso, não editar. Ao
# contrário de Command/Observer/State, aqui você NÃO herda de `Estrategia`:
# escreva sua própria base, ver TODO abaixo — motivo em estrategias_base.py.)
#
# TODO: implemente aqui. Considere uma base comum (RotaColeta) com
# __init_subclass__ registrando cada rota, ver Seção 2.2 (metaprogramação
# aplicada a uma segunda hierarquia).

from abc import ABC, abstractmethod

class RotaColeta(ABC):
    _registro_rotas = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        RotaColeta._registro_rotas[cls.__name__] = cls


    def __init__(self):
        pass

    @abstractmethod   
    def mover(self, robo): pass
    


class RotaDireta(RotaColeta):
    #Vai direto até cada pratileira.
    #
    pass

class RotaComDuplaConferencia(RotaColeta):
    pass