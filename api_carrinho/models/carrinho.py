from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from api_carrinho.models.produto import Produto


@dataclass
class Carrinho:
    """
    Representa um carrinho de compras.
    """

    codigo: str  # uuid versão 4 representando um carrinho único
    data_alteracao: datetime  # data e hora de última alteração no carrinho (para expirar)
    cliente: Optional[int]  # código do cliente - None caso cliente sem logar
    produtos: List[Produto]
