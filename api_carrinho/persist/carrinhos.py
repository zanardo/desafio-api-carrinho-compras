# Vamos persistir os carrinhos na memória, neste exercício.
from typing import Dict, Optional

from api_carrinho.models.carrinho import Carrinho

_CARRINHOS: Dict[str, Carrinho] = {}


class CarrinhoNaoExisteError(Exception):
    ...


def db_carrinho_fetch(codigo: str) -> Carrinho:
    try:
        return _CARRINHOS[codigo]
    except KeyError:
        raise CarrinhoNaoExisteError("carrinho com código {} não existe".format(codigo))


def db_carrinho_save(carrinho: Carrinho) -> None:
    _CARRINHOS[carrinho.codigo] = carrinho


def db_carrinho_delete(codigo: str) -> None:
    try:
        del _CARRINHOS[codigo]
    except KeyError:
        raise CarrinhoNaoExisteError("carrinho com código {} não existe".format(codigo))
