from pprint import pformat
from typing import Dict

import requests

from api_carrinho.log import log

WEBSERVICE = "http://127.0.0.1:5000"


def api_post(uri: str, dados: Dict) -> Dict:
    "Generaliza um POST na API e retorna os dados"
    log.debug("chamando api via post em %s com dados %s", uri, pformat(dados))
    res = requests.post(url="{}/{}".format(WEBSERVICE, uri), timeout=5, data=dados)
    log.debug("retorno do api:\n%s", pformat(res.json()))
    if not res.ok:
        raise ValueError(
            "erro ao carregar dados da api: %s: %s", res.status_code, res.text
        )
    return res.json()["dados"]


def main():
    log.info("criando novo carrinho")
    carrinho = api_post("/novo", dados={})["carrinho_codigo"]
    log.info("adicionando produto no carrinho")
    api_post("/produto-adiciona", dados={"carrinho": carrinho, "produto": "AB1234567"})


if __name__ == "__main__":
    main()
