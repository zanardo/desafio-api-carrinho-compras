"""
Testes de unidade do projeto.
"""

import unittest
from datetime import datetime, timedelta

from api_carrinho.models.carrinho import Carrinho


class TestModelsCarrinho(unittest.TestCase):
    def test_new(self):
        "Teste de criação de um novo carrinho"
        carrinho = Carrinho(cliente=None)
        self.assertIsNone(carrinho.cliente)
        self.assertListEqual(carrinho.produtos, [])
        self.assertEqual(len(carrinho.codigo), 36)
        self.assertRegex(
            carrinho.codigo,
            r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        )
        self.assertEqual((datetime.now() - carrinho.data_alteracao).days, 0)


if __name__ == "__main__":
    unittest.main()
