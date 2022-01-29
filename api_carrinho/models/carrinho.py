from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from api_carrinho.models.cupom import Cupom
from api_carrinho.models.produto import Produto


@dataclass
class CarrinhoTotais:
    subtotal: float = 0.0
    total: float = 0.0


class Carrinho:
    """
    Representa um carrinho de compras.
    """

    codigo: str  # uuid versão 4 representando um carrinho único
    data_alteracao: datetime  # data e hora de última alteração no carrinho (para expirar)
    cliente: Optional[int]  # código do cliente - None caso cliente sem logar
    produtos: Dict[str, Produto]  # produtos no carrinho - código => Produto
    cupom: Optional[Cupom]  # cupom de desconto - aceitamos somente um
    totais: CarrinhoTotais

    def _atualiza_mtime(self):
        self.data_alteracao = datetime.now()

    def _atualiza_totais(self):
        self.totais.subtotal = 0.0
        self.totais.total = 0.0
        for codigo in self.produtos:
            self.totais.subtotal += (
                self.produtos[codigo].quantidade * self.produtos[codigo].preco_por
            )
        self.totais.total = self.totais.subtotal
        if self.cupom:
            self.totais.total -= self.cupom.valor

    def __init__(self, cliente: Optional[int]) -> None:
        """
        Inicializa um carrinho de compras, definindo um código aleatório e sem produtos.
        """
        self.codigo = str(uuid4())
        self.cliente = cliente
        self._atualiza_mtime()
        self.produtos = {}
        self.cupom = None
        self.totais = CarrinhoTotais()

    def define_cliente(self, cliente: Optional[int]) -> None:
        """
        Edita o cliente do carrinho de compras. Pode ser None.
        """
        self.cliente = cliente

    def adiciona_produto(self, produto: Produto) -> None:
        """
        Adiciona um produto ao carrinho. Caso o produto já exista, apenas a quantidade é
        acrescida de 1.
        """
        if produto.codigo in self.produtos:
            self.produtos[produto.codigo].define_quantidade(
                self.produtos[produto.codigo].quantidade + 1
            )
        self.produtos[produto.codigo] = produto
        self._atualiza_totais()

    def remove_produto(self, codigo: str) -> None:
        """
        Remove um produto do carrinho, dado seu código.
        """
        if codigo in self.produtos:
            del self.produtos[codigo]
            self._atualiza_totais()

    def remove_todos_produtos(self):
        """
        Remove todos os produtos do carrinho.
        """
        self.produtos = {}
        self._atualiza_totais()

    def define_cupom_desconto(self, cupom: Optional[Cupom]) -> None:
        """
        Associa um cupom de desconto ao carrinho. No momento, aceitamos somente um cupom.
        Use cupom=None para remover.
        """
        self.cupom = cupom
        self._atualiza_totais()

    def define_produto_quantidade(self, produto_codigo: str, quantidade: int) -> None:
        """
        Define a quantidade de um produto no carrinho.
        """
        self.produtos[produto_codigo].define_quantidade(quantidade)
        self._atualiza_totais()
