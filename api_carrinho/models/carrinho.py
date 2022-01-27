from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from api_carrinho.models.produto import Produto


class Carrinho:
    """
    Representa um carrinho de compras.
    """

    codigo: str  # uuid versão 4 representando um carrinho único
    data_alteracao: datetime  # data e hora de última alteração no carrinho (para expirar)
    cliente: Optional[int]  # código do cliente - None caso cliente sem logar
    produtos: Dict[str, Produto]  # produtos no carrinho - código => Produto

    def _atualiza_mtime(self):
        self.data_alteracao = datetime.now()

    def __init__(self, cliente: Optional[int]) -> None:
        """
        Inicializa um carrinho de compras, definindo um código aleatório e sem produtos.
        """
        self.codigo = str(uuid4())
        self.cliente = cliente
        self._atualiza_mtime()
        self.produtos = {}

    def define_cliente(self, cliente: Optional[int]) -> None:
        """
        Edita o cliente do carrinho de compras. Pode ser None.
        """
        self.cliente = cliente

    def adiciona_produto(self, produto: Produto) -> None:
        """
        Adiciona um produto ao carrinho. Caso o produto já exista, o processo é ignorado.
        Para alterar a quantidade, use a rotina define_quantidade!
        """
        if produto.codigo in self.produtos:
            return
        self.produtos[produto.codigo] = produto
