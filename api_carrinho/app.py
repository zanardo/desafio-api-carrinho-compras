from typing import Dict, Optional

from flask import Flask, request

from api_carrinho import __VERSION__
from api_carrinho.log import log
from api_carrinho.models.carrinho import Carrinho

app = Flask(__name__)

# Vamos persistir os carrinhos na memória, neste exercício.
CARRINHOS: Dict[str, Carrinho] = {}


@app.post("/novo")
def novo():
    cliente: Optional[str] = request.form.get("cliente")
    carrinho = Carrinho(cliente=cliente)
    # A probabilidade de uma colisão de UUIDs é baixíssima, mas mesmo assim vamos nos
    # certificar que o carrinho com o mesmo código não existe.
    assert carrinho.codigo not in CARRINHOS
    CARRINHOS[carrinho.codigo] = carrinho
    return {"sucesso": "ok", "dados": {"carrinho_codigo": carrinho.codigo}}


@app.post("/produto-remove")
def produto_remove():
    carrinho_codigo = request.form["carrinho"]
    produto_codigo = request.form["produto"]
    carrinho = CARRINHOS[carrinho_codigo]
    carrinho.remove_produto(produto_codigo)
    return {"sucesso": "ok", "dados": {}}


if __name__ == "__main__":
    log.info("iniciando api-carrinho versão %s", __VERSION__)
    app.run(host="127.0.0.1", port=5000, debug=True)
