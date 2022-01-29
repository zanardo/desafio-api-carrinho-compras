"""
Este módulo faz "mock" da persistência dos cupons de desconto.
"""
from dataclasses import dataclass

from api_carrinho.models.cupom import Cupom


class CupomNaoExisteError(Exception):
    """
    Cupom não existe.
    """

    ...


@dataclass
class CupomPersisted:
    """
    Classe que define um cupom de desconto da forma como seria armazenado em um banco de
    dados.
    """

    codigo: str
    valor: float


# Insere alguns cupons de desconto de exemplo.
_CUPOMS = {
    "VALE10": Cupom(codigo="VALE10", valor=10.0),
    "BLACKFRIDAY15": Cupom(codigo="BLACKFRIDAY15", valor=15.0),
}


def db_cupom_fetch(codigo: str) -> CupomPersisted:
    """
    Coleta um cupom de desconto do banco de dados.
    """
    try:
        return _CUPOMS[codigo]
    except KeyError:
        raise CupomNaoExisteError("cupom com código {} não existe".format(codigo))
