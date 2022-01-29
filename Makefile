# Costumo usar o make para todos meus projetos, independente da linguagem. Com isto, o
# fluxo de desenvolvimento fica mais padronizado!

# Com isto, sempre sei que "make run" inicia o projeto em modo de desenvolvimento, "make
# upload" envia os artefatos preparados para distribuição (imagem do Docker, pacote de
# biblioteca sdist do Python, binário estático compilado do Go, etc).

# Sempre fixo a versão do Python!
PYTHON ?= python3.9

# Variáveis auxiliares... Não devemos ficar repetindo as coisas, correto?
VENV = .venv
VPYTHON = $(VENV)/bin/python3
VPIP = $(VENV)/bin/pip

# "make all" ou somente "make" cria o virtualenv, e instala todas as dependências diretas
# e transitivas com pining de versão, descritas em "requirements.txt", usando a mágica da
# idempotência :)
.PHONY: all
all: $(VENV)/.ok

# Cria o virtualenv e instala as ferramentas básicas. O pip-tools é minha ferramenta
# escolhida para gerenciar as dependências, de forma bastante reproduzível.
$(VENV)/bin/pip-compile:
	$(PYTHON) -m venv $(VENV)
	$(VPYTHON) -m pip install -q -U pip
	$(VPYTHON) -m pip install -q -U wheel setuptools
	$(VPYTHON) -m pip install -q pip-tools

# Certifica-se que o virtualenv está criado, com as ferramentas necessárias instaladas.
requirements.in: $(VENV)/bin/pip-compile

# Salva as dependências diretas e transitivas com versões fixas em requirements.txt a
# partir de requirements.in.
requirements.txt: requirements.in
	$(VPYTHON) -m piptools compile -q

# Sincroniza os pacotes dentro do virtualenv com o requirements.txt.
$(VENV)/.ok: requirements.txt
	$(VPYTHON) -m piptools sync -q requirements.txt
	@touch $(VENV)/.ok

# Limpa os artefatos!
.PHONY: clean
clean:
	@rm -rf $(VENV)

# Executa o projeto em modo de desenvolvimento.
.PHONY: run
run: $(VENV)/.ok
	@while :; do $(VPYTHON) -m api_carrinho.app ; sleep 1 ; done

# Executa a bateria de testes de unidade.
.PHONY: tests
tests: $(VENV)/.ok
	$(VPYTHON) -m tests

# Executa a bateria de testes de integração.
.PHONY: tests-integration
tests-integration: $(VENV)/.ok
	$(VPYTHON) -m tests_integration

# Cria a imagem do Docker.
.PHONY: docker-build
docker-build:
	docker build \
		-t zanardo/api-carrinho \
		.

# Executa o container do Docker.
.PHONY: docker-run
docker-run:
	@docker run --rm -it \
		-p 5000:5000 \
		zanardo/api-carrinho
