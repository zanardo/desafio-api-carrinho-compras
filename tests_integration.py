from pprint import pformat
from typing import Dict

import requests

from api_carrinho.log import log

WEBSERVICE = "http://127.0.0.1:5000"


def api_get(uri: str) -> Dict:
    "Generaliza um GET na API e retorna os dados"
    log.debug("chamando api via get em %s", uri)
    res = requests.get(url="{}/{}".format(WEBSERVICE, uri), timeout=5)
    log.debug("retorno do api:\n%s", pformat(res.json()))
    if not res.ok:
        raise ValueError(
            "erro ao carregar dados da api: %s: %s", res.status_code, res.text
        )
    return res.json()["dados"]


def api_post(uri: str, dados: Dict) -> Dict:
    "Generaliza um POST na API e retorna os dados"
    log.debug("chamando api via post em %s com dados %s", uri, pformat(dados))
    res = requests.post(url="{}/{}".format(WEBSERVICE, uri), timeout=5, data=dados)
    log.debug("retorno do api:\n%s", pformat(res.json()))
    if not res.ok:
        raise ValueError(
            "erro ao carregar dados da api: %s: %s", res.status_code, res.text
        )
    j = res.json()
    if j["sucesso"]:
        return j["dados"]
    else:
        return j["erro"]


def main():
    log.info("criando novo carrinho")
    carrinho = api_post("/novo", dados={})["carrinho_codigo"]
    log.info("altera cliente do carrinho")
    api_post("/define-cliente", dados={"carrinho": carrinho, "cliente": 123456})
    log.info("adiciona produto no carrinho")
    api_post("/produto-adiciona", dados={"carrinho": carrinho, "produto": "AB1234567"})
    log.info("adiciona outro produto no carrinho")
    api_post("/produto-adiciona", dados={"carrinho": carrinho, "produto": "CD7654321"})
    log.info("define quantidade de produto no carrinho")
    api_post(
        "/produto-define-quantidade",
        dados={"carrinho": carrinho, "produto": "CD7654321", "quantidade": 2},
    )
    log.info("remove produto do carrinho")
    api_post("/produto-remove", dados={"carrinho": carrinho, "produto": "CD7654321"})
    log.info("define a quantidade de um produto")
    api_post(
        "/produto-define-quantidade",
        dados={"carrinho": carrinho, "produto": "AB1234567", "quantidade": 3},
    )
    log.info("limpa o carrinho")
    api_post("/limpa", dados={"carrinho": carrinho})
    log.info("adiciona produto no carrinho")
    api_post("/produto-adiciona", dados={"carrinho": carrinho, "produto": "AB1234567"})
    log.info("tenta adicionar produto para estourar estoque")
    api_post("/produto-adiciona", dados={"carrinho": carrinho, "produto": "EF3567942"})
    assert (
        api_post(
            "/produto-define-quantidade",
            dados={"carrinho": carrinho, "produto": "EF3567942", "quantidade": 2},
        )["tipo"]
        == "ProdutoSemEstoqueError"
    )
    log.info("define um cupom de desconto")
    api_post("/cupom-define", dados={"carrinho": carrinho, "cupom": "BLACKFRIDAY15"})
    log.info("obtendo o carrinho completo da api")
    api_get("/carrinho/{}".format(carrinho))


if __name__ == "__main__":
    main()
