# Vamos persistir os carrinhos na memória, neste exercício.
from typing import Dict, Optional

from api_carrinho.models.carrinho import Carrinho

_CARRINHOS: Dict[str, Carrinho] = {}


def db_carrinho_fetch(codigo: str) -> Optional[Carrinho]:
    return _CARRINHOS.get(codigo)


def db_carrinho_save(carrinho: Carrinho) -> None:
    _CARRINHOS[carrinho.codigo] = carrinho


def db_carrinho_delete(codigo: str) -> None:
    del _CARRINHOS[codigo]
