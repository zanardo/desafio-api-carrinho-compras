from typing import Optional

from flask import Flask, request

from api_carrinho import __VERSION__
from api_carrinho.log import log
from api_carrinho.models.carrinho import Carrinho
from api_carrinho.models.produto import Produto
from api_carrinho.persist.carrinhos import db_carrinho_fetch, db_carrinho_save
from api_carrinho.persist.cupons import db_cupom_fetch
from api_carrinho.persist.produtos import db_produto_fetch

app = Flask(__name__)


@app.post("/novo")
def novo():
    cliente: Optional[str] = request.form.get("cliente")
    carrinho = Carrinho(cliente=cliente)
    db_carrinho_save(carrinho)
    return {"sucesso": "ok", "dados": {"carrinho_codigo": carrinho.codigo}}


@app.post("/produto-adiciona")
def produto_adiciona():
    carrinho_codigo = request.form["carrinho"]
    produto_codigo = request.form["produto"]
    carrinho = db_carrinho_fetch(carrinho_codigo)
    produto_persisted = db_produto_fetch(produto_codigo)
    produto = Produto(
        codigo=produto_persisted.codigo,
        descricao=produto_persisted.descricao,
        preco_de=produto_persisted.preco_de,
        preco_por=produto_persisted.preco_por,
        quantidade=1,
    )
    carrinho.adiciona_produto(produto)
    return {"sucesso": "ok", "dados": {}}


@app.post("/produto-remove")
def produto_remove():
    carrinho_codigo = request.form["carrinho"]
    produto_codigo = request.form["produto"]
    carrinho = db_carrinho_fetch(carrinho_codigo)
    carrinho.remove_produto(produto_codigo)
    return {"sucesso": "ok", "dados": {}}


@app.post("/produto-define-quantidade")
def produto_define_quantidade():
    carrinho_codigo = request.form["carrinho"]
    produto_codigo = request.form["produto"]
    quantidade = int(request.form["quantidade"])
    carrinho = db_carrinho_fetch(carrinho_codigo)
    carrinho.produtos[produto_codigo].define_quantidade(quantidade)
    carrinho._atualiza_totais()
    return {"sucesso": "ok", "dados": {}}


@app.post("/limpa")
def limpa():
    carrinho_codigo = request.form["carrinho"]
    carrinho = db_carrinho_fetch(carrinho_codigo)
    carrinho.remove_todos_produtos()
    return {"sucesso": "ok", "dados": {}}


@app.post("/cupom-define")
def cupom_define():
    carrinho_codigo = request.form["carrinho"]
    cupom_codigo = request.form["cupom"]
    carrinho = db_carrinho_fetch(carrinho_codigo)
    cupom = db_cupom_fetch(cupom_codigo)
    carrinho.define_cupom_desconto(cupom)
    return {"sucesso": "ok", "dados": {}}


@app.get("/carrinho/<codigo>")
def carrinho(codigo: str):
    carrinho = db_carrinho_fetch(codigo)
    retorno_dados = {
        "codigo": carrinho.codigo,
        "totais": {"subtotal": carrinho.totais.subtotal, "total": carrinho.totais.total},
        "produtos": [],
        "cupom": {},
    }
    if carrinho.cupom:
        retorno_dados["cupom"] = {
            "codigo": carrinho.cupom.codigo,
            "valor": carrinho.cupom.valor,
        }
    for codigo_produto in carrinho.produtos:
        produto = carrinho.produtos[codigo_produto]
        retorno_dados["produtos"].append(
            {
                "codigo": produto.codigo,
                "descricao": produto.descricao,
                "quantidade": produto.quantidade,
                "preco_de": produto.preco_de,
                "preco_por": produto.preco_por,
            }
        )
    return {"sucesso": "ok", "dados": retorno_dados}


if __name__ == "__main__":
    log.info("iniciando api-carrinho versão %s", __VERSION__)
    app.run(host="127.0.0.1", port=5000, debug=True)
