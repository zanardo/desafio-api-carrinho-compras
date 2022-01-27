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
