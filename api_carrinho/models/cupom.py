from dataclasses import dataclass


@dataclass
class Cupom:
    """
    Representa um Cupom de Desconto. No momento, apenas consideramos descontos em valor.
    """

    codigo: str
    valor: float

    def valida_cupom(self) -> bool:
        """
        Valida se o cupom de desconto é verdadeiro.
        Neste exercício, apenas aceitamos qualquer cupom!
        """
        return True
