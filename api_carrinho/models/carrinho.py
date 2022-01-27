from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from api_carrinho.models.produto import Produto


class Carrinho:
    """
    Representa um carrinho de compras.
    """

    codigo: str  # uuid versão 4 representando um carrinho único
    data_alteracao: datetime  # data e hora de última alteração no carrinho (para expirar)
    cliente: Optional[int]  # código do cliente - None caso cliente sem logar
    produtos: List[Produto]

    def _atualiza_mtime(self):
        self.data_alteracao = datetime.now()

    def __init__(self, cliente: Optional[int]) -> None:
        """
        Inicializa um carrinho de compras, definindo um código aleatório e sem produtos.
        """
        self.codigo = str(uuid4())
        self.cliente = cliente
        self._atualiza_mtime()
        self.produtos = []

    def define_cliente(self, cliente: Optional[int]) -> None:
        """
        Edita o cliente do carrinho de compras. Pode ser None.
        """
        self.cliente = cliente
