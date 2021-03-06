"""
Testes de unidade do projeto.
"""

import unittest
from datetime import datetime

from api_carrinho.models.carrinho import Carrinho
from api_carrinho.models.cupom import Cupom
from api_carrinho.models.produto import Produto


class TestModelsProduto(unittest.TestCase):
    def _new(self) -> Produto:
        return Produto(
            codigo="B33F0123456",
            descricao="Produto Teste",
            preco_de=10.0,
            preco_por=10.00,
            quantidade=3,
        )

    def test_new(self):
        "Teste de criação de um produto"
        _ = self._new()

    def test_define_quantidade(self):
        "Teste de definição de quantidade de um produto"
        produto = self._new()
        self.assertEqual(produto.quantidade, 3)
        produto.define_quantidade(100)
        self.assertEqual(produto.quantidade, 100)
        with self.assertRaises(ValueError):
            produto.define_quantidade(0)
        with self.assertRaises(ValueError):
            produto.define_quantidade(-1)


class TestModelsCupom(unittest.TestCase):
    def _new(self):
        return Cupom(codigo="NOVO15", valor=15.0)

    def test_new(self):
        "Teste de criação de um novo cupom de desconto"
        _ = self._new()

    def test_valida(self):
        "Teste de validação do cupom"
        cupom = self._new()
        self.assertTrue(cupom.valida_cupom())


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

    def test_cliente(self):
        "Teste de alteração de cliente"
        carrinho = Carrinho(cliente=None)
        self.assertIsNone(carrinho.cliente)
        carrinho.define_cliente(123456)
        self.assertEqual(carrinho.cliente, 123456)
        carrinho.define_cliente(None)
        self.assertIsNone(carrinho.cliente)

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

    def test_remove_produto(self):
        "Teste de remoção de produto do carrinho"
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
        carrinho.remove_produto(produto.codigo)
        self.assertEqual(len(carrinho.produtos), 0)

    def test_remove_produtos(self):
        "Teste de remoção de todos os produtos do carrinho"
        carrinho = Carrinho(cliente=None)
        carrinho.adiciona_produto(
            Produto(
                codigo="AB1234567",
                descricao="Descrição",
                preco_de=100.0,
                preco_por=90.0,
                quantidade=1,
            )
        )
        self.assertEqual(len(carrinho.produtos), 1)
        carrinho.adiciona_produto(
            Produto(
                codigo="CD1234567",
                descricao="Descrição 2",
                preco_de=100.0,
                preco_por=100.0,
                quantidade=3,
            )
        )
        self.assertEqual(len(carrinho.produtos), 2)
        carrinho.remove_todos_produtos()
        self.assertEqual(len(carrinho.produtos), 0)

    def test_produto_define_quantidade(self):
        "Testa definição da quantidade de um produto no carrinho"
        carrinho = Carrinho(cliente=None)
        carrinho.adiciona_produto(
            Produto(
                codigo="AB1234567",
                descricao="Descrição",
                preco_de=100.0,
                preco_por=90.0,
                quantidade=1,
            )
        )
        self.assertEqual(carrinho.produtos["AB1234567"].quantidade, 1)
        carrinho.define_produto_quantidade("AB1234567", 2)
        self.assertEqual(carrinho.produtos["AB1234567"].quantidade, 2)

    def test_define_cupom(self):
        "Testa associação de cupom de desconto ao carrinho"
        carrinho = Carrinho(cliente=None)
        cupom = Cupom(codigo="VALE15", valor=15.0)
        carrinho.define_cupom_desconto(cupom)
        self.assertEqual(carrinho.cupom.codigo, "VALE15")

    def test_totais(self):
        "Testa cálculo de totalizadores do carrinho"
        carrinho = Carrinho(cliente=None)
        self.assertEqual(carrinho.totais.subtotal, 0.0)
        self.assertEqual(carrinho.totais.total, 0.0)
        carrinho.adiciona_produto(
            Produto(
                codigo="CD1234567",
                descricao="Descrição 2",
                preco_de=90.0,
                preco_por=100.0,
                quantidade=3,
            )
        )
        self.assertEqual(carrinho.totais.subtotal, 300.0)
        self.assertEqual(carrinho.totais.total, 300.0)
        carrinho.adiciona_produto(
            Produto(
                codigo="FG1234567",
                descricao="Descrição 3",
                preco_de=30.0,
                preco_por=25.5,
                quantidade=1,
            )
        )
        self.assertEqual(carrinho.totais.subtotal, 325.5)
        self.assertEqual(carrinho.totais.total, 325.5)
        carrinho.define_cupom_desconto(Cupom(codigo="AX10", valor=10.0))
        self.assertEqual(carrinho.totais.subtotal, 325.5)
        self.assertEqual(carrinho.totais.total, 315.5)
        carrinho.remove_produto("FG1234567")
        self.assertEqual(carrinho.totais.subtotal, 300.0)
        self.assertEqual(carrinho.totais.total, 290.0)
        carrinho.remove_todos_produtos()
        self.assertEqual(carrinho.totais.subtotal, 0.0)
        self.assertEqual(carrinho.totais.total, -10.0)
        carrinho.define_cupom_desconto(None)
        self.assertEqual(carrinho.totais.subtotal, 0.0)
        self.assertEqual(carrinho.totais.total, 0.0)


if __name__ == "__main__":
    unittest.main()
