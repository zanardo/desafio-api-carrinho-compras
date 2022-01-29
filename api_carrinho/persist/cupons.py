from dataclasses import dataclass

from api_carrinho.models.cupom import Cupom


class CupomNaoExisteError(Exception):
    ...


@dataclass
class CupomPersisted:
    codigo: str
    valor: float


_CUPOMS = {
    "VALE10": Cupom(codigo="VALE10", valor=10.0),
    "BLACKFRIDAY15": Cupom(codigo="BLACKFRIDAY15", valor=15.0),
}


def db_cupom_fetch(codigo: str) -> CupomPersisted:
    try:
        return _CUPOMS[codigo]
    except KeyError:
        raise CupomNaoExisteError("cupom com código {} não existe".format(codigo))
