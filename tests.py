"""
Testes de unidade do projeto.
"""

import unittest
from datetime import datetime

from api_carrinho.models.carrinho import Carrinho
from api_carrinho.models.produto import Produto


class TestModelsCarrinho(unittest.TestCase):
    def test_new(self):
        "Teste de criação de um novo carrinho"
        carrinho = Carrinho(cliente=None)
        self.assertIsNone(carrinho.cliente)
        self.assertEqual(carrinho.produtos, {})
        self.assertEqual(len(carrinho.codigo), 36)
        self.assertRegex(
            carrinho.codigo,
            r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
        )
        self.assertEqual((datetime.now() - carrinho.data_alteracao).days, 0)

    def test_adiciona_produto(self):
        "Teste de adição de produto ao carrinho"
        carrinho = Carrinho(cliente=None)
        produto = Produto(
            codigo="AB1234567",
            descricao="Descrição",
            preco_de=100.0,
            preco_por=90.0,
            quantidade=1,
        )
        carrinho.adiciona_produto(produto)
        self.assertTrue(len(carrinho.produtos), 1)

    def test_adiciona_produto_existente(self):
        "Teste de adição de produto já existente ao carrinho"
        carrinho = Carrinho(cliente=None)
        produto = Produto(
            codigo="AB1234567",
            descricao="Descrição",
            preco_de=100.0,
            preco_por=90.0,
            quantidade=1,
        )
        carrinho.adiciona_produto(produto)
        self.assertEqual(len(carrinho.produtos), 1)
        self.assertEqual(carrinho.produtos[produto.codigo].quantidade, 1)
        carrinho.adiciona_produto(produto)
        self.assertEqual(len(carrinho.produtos), 1)
        self.assertEqual(carrinho.produtos[produto.codigo].quantidade, 2)


if __name__ == "__main__":
    unittest.main()
