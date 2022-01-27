from dataclasses import dataclass


@dataclass
class Cupom:
    """
    Representa um Cupom de Desconto. No momento, apenas consideramos descontos em valor.
    """

    codigo: str
    valor: float
