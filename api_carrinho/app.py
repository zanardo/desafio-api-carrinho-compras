from typing import Optional

from flask import Flask, request

from api_carrinho import __VERSION__
from api_carrinho.log import log
from api_carrinho.models.carrinho import Carrinho
from api_carrinho.persist.carrinhos import db_carrinho_fetch, db_carrinho_save

app = Flask(__name__)


@app.post("/novo")
def novo():
    cliente: Optional[str] = request.form.get("cliente")
    carrinho = Carrinho(cliente=cliente)
    db_carrinho_save(carrinho)
    return {"sucesso": "ok", "dados": {"carrinho_codigo": carrinho.codigo}}


@app.post("/produto-remove")
def produto_remove():
    carrinho_codigo = request.form["carrinho"]
    produto_codigo = request.form["produto"]
    carrinho = db_carrinho_fetch(carrinho_codigo)
    carrinho.remove_produto(produto_codigo)
    return {"sucesso": "ok", "dados": {}}


if __name__ == "__main__":
    log.info("iniciando api-carrinho versão %s", __VERSION__)
    app.run(host="127.0.0.1", port=5000, debug=True)
