from dataclasses import dataclass
from typing import Optional

from api_carrinho.models.cupom import Cupom


@dataclass
class CupomPersisted:
    codigo: str
    valor: float


_CUPOMS = {
    "VALE10": Cupom(codigo="VALE10", valor=10.0),
    "BLACKFRIDAY15": Cupom(codigo="BLACKFRIDAY15", valor=15.0),
}


def db_cupom_fetch(codigo: str) -> Optional[CupomPersisted]:
    if codigo not in _CUPOMS:
        return None
    return _CUPOMS[codigo]
