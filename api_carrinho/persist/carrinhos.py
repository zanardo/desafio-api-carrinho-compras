"""
Este módulo faz "mock" da persistência dos carrinhos de compras.
"""
from typing import Dict

from api_carrinho.models.carrinho import Carrinho

_CARRINHOS: Dict[str, Carrinho] = {}


class CarrinhoNaoExisteError(Exception):
    """
    Carrinho não existe.
    """

    ...


def db_carrinho_fetch(codigo: str) -> Carrinho:
    """
    Obtém um carrinho da persistência.
    """
    try:
        return _CARRINHOS[codigo]
    except KeyError:
        raise CarrinhoNaoExisteError("carrinho com código {} não existe".format(codigo))


def db_carrinho_save(carrinho: Carrinho) -> None:
    """
    Salva um carrinho na persistência.
    """
    _CARRINHOS[carrinho.codigo] = carrinho


def db_carrinho_delete(codigo: str) -> None:
    """
    Remove um carrinho da persistência.
    """
    try:
        del _CARRINHOS[codigo]
    except KeyError:
        raise CarrinhoNaoExisteError("carrinho com código {} não existe".format(codigo))
