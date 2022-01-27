from dataclasses import dataclass


@dataclass
class Produto:
    """
    Representa um produto com os dados necessários para uso no carrinho.
    """

    codigo: str
    descricao: str
    preco_de: float
    preco_por: float
    quantidade: int  # Quantidade de itens no carrinho

    def define_quantidade(self, quantidade: int) -> None:
        """
        Define a quantidade de um produto no carrinho. Levanta exceção ValueError caso
        quantidade seja negativa ou zero.
        """
        if quantidade <= 0:
            raise ValueError("quantidade do produto não pode ser negativa ou zero")
        self.quantidade = quantidade
