from flask import Flask

from api_carrinho import __VERSION__
from api_carrinho.log import log

app = Flask(__name__)


if __name__ == "__main__":
    log.info("iniciando api-carrinho versão %s", __VERSION__)
    app.run(host="127.0.0.1", port=5000, debug=True)
