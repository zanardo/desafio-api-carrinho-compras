from dataclasses import dataclass
from typing import Optional


@dataclass
class ProdutoPersisted:
    codigo: str
    descricao: str
    preco_de: float
    preco_por: float
    estoque: int


_PRODUTOS = {
    "AB1234567": ProdutoPersisted(
        codigo="AB1234567",
        descricao="Camiseta Pólo",
        preco_de=170.0,
        preco_por=170.0,
        estoque=10,
    ),
    "CD7654321": ProdutoPersisted(
        codigo="CD7654321",
        descricao="Calça Jeans",
        preco_de=280.0,
        preco_por=250.0,
        estoque=5,
    ),
    "EF3567942": ProdutoPersisted(
        codigo="EF3567942",
        descricao="Sapato Social Masculino",
        preco_de=500.0,
        preco_por=450.0,
        estoque=1,
    ),
}


def db_produto_fetch(codigo: str) -> Optional[ProdutoPersisted]:
    if codigo not in _PRODUTOS:
        return None
    return _PRODUTOS[codigo]
