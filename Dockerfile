FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN set -x ; \
	python3.9 -m venv .venv && \
	.venv/bin/python -m pip install -U pip wheel setuptools && \
	.venv/bin/python -m pip install -r requirements.txt

COPY api_carrinho /app/api_carrinho

ENV UID=12345 \
	HOST=0.0.0.0 \
	PORT=5000

CMD exec setpriv --reuid=${UID} --regid=${UID} --clear-groups \
	.venv/bin/python -m api_carrinho.app
