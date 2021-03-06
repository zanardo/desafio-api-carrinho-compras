# Desafio - API Carrinho de Compras

Este repositório possui um desafio de implementação de uma API para um carrinho de compras
de uma loja virtual.

**Para iniciar**: siga as instruções em "Como empacotar para a produção" e depois "Como
executar o projeto usando o Docker".

- [Desafio - API Carrinho de Compras](#desafio---api-carrinho-de-compras)
  - [Observações sobre a estrutura do código-fonte](#observações-sobre-a-estrutura-do-código-fonte)
  - [Observações sobre a estrutura do projeto](#observações-sobre-a-estrutura-do-projeto)
  - [Documentação das APIs](#documentação-das-apis)
    - [Observações gerais](#observações-gerais)
    - [Retornos da API](#retornos-da-api)
    - [Endpoints](#endpoints)
      - [/novo - Novo carrinho](#novo---novo-carrinho)
      - [/cliente-define - Altera cliente](#cliente-define---altera-cliente)
      - [/produto-adiciona - Novo produto no carrinho](#produto-adiciona---novo-produto-no-carrinho)
      - [/produto-remove - Remove produto no carrinho](#produto-remove---remove-produto-no-carrinho)
      - [/produto-define-quantidade - Altera quantidade de um produto no carrinho](#produto-define-quantidade---altera-quantidade-de-um-produto-no-carrinho)
      - [/limpa - Apaga produtos no carrinho](#limpa---apaga-produtos-no-carrinho)
      - [/cupom-define - Associa um cupom de desconto ao carrinho](#cupom-define---associa-um-cupom-de-desconto-ao-carrinho)
      - [/carrinho - Obtém todos os dados do carrinho](#carrinho---obtém-todos-os-dados-do-carrinho)
  - [Dependências para o projeto](#dependências-para-o-projeto)
  - [Como criar um ambiente de desenvolvimento](#como-criar-um-ambiente-de-desenvolvimento)
  - [Como rodar o projeto em ambiente de desenvolvimento](#como-rodar-o-projeto-em-ambiente-de-desenvolvimento)
  - [Como rodar a bateria de testes de unidade](#como-rodar-a-bateria-de-testes-de-unidade)
  - [Como rodar a bateria de testes de integração](#como-rodar-a-bateria-de-testes-de-integração)
  - [Como empacotar para a "produção"](#como-empacotar-para-a-produção)
  - [Como executar o projeto usando o Docker](#como-executar-o-projeto-usando-o-docker)


## Observações sobre a estrutura do código-fonte

* O código-fonte em Python foi formatado usando o **Black**, com 90 colunas, para
  padronização.

* Os _imports_ foram formatados e organizados usando o **isort**.

* Todo o código em Python passou por _linting_ via **flake8** e não possui problemas
  identificados pelos _linters_.

* Foram usados _type-hints_ o máximo possível, para anotar os tipos das variáveis e tornar
  o projeto mais fácil de entender e manter. Para validar os tipos, foi usado os linters
  do **mypy**.

* O projeto possui diversos testes de unidade para facilitar na manutenção e
  _refactorings_.

* O projeto possui testes de integração, os quais devem ser executados com o servidor web
  previamente rodando.

* O projeto usa um _virtualenv_ para salvar as dependências de forma isolada, e o
  **pip-tools** para compilar a relação das dependências diretas e transitivas com versões
  fixas, para ser reproduzível. Seu gerenciamento está automatizado no `Makefile`.

* O empacotamento do projeto para "produção" usa o Docker.

## Observações sobre a estrutura do projeto

* Todas as rotinas relacionadas à manipulação dos dados e regras de negócio ficam no
  pacote `api_carrinho.models`.

* Todos os dados de persistência são usados através de _mocks_, ficando no pacote
  `api_carrinho.persist`.

* O diretório `models` contém os seguintes módulos:

    * `carrinho`: Classe `Carrinho` representa um carrinho de compras.
    * `cupom`: Classe `Cupom` representa um cupom de desconto.
    * `produto`: Classe `Produto` representa um produto no carrinho de compras.

* O diretório `persist` contém módulos que "persistem" os dados na memória e contém
  pré-definidos alguns dados para uso neste exercício, eliminando a necessidade de bancos
  de dados separado:

    * `carrinhos`: Classe `CarrinhoPersist` e funções de salvar/coletar os carrinhos.
    * `cupons`: Classe `CupomPersist` e funções para coletar cupons de desconto.
    * `produtos`: Classe `ProdutoPersist` e funções para coletar produtos no cadastro.

* O aplicativo em si, que provê a API via HTTP fica em `api_carrinho.app`. Nele, são
  plugados os registros de _mocks_ dos dados com as regras de negócio.

* O servidor web usado é o de desenvolvimento do _Flask_ com _debug_ ativado. Isto foi
  feito somente para este exercício. Em produção, deve-se usar um servidor apropriado (ex:
  _Gunicorn_, _UWSGI_, etc)!

## Documentação das APIs

### Observações gerais

* As rotinas que criam/alteram dados são chamados pelo verbo HTTP `POST`. As rotinas que
  somente coletam dados são chamadas pelo verbo HTTP `GET`.

* A API é desenvolvida para ser chamada diretamente pelo _frontend_. Não existe
  autenticação/autorização.

* A associação do carrinho com o frontend é feita criando-se um carrinho e obtendo-se seu
  código, que é um `UUID` versão 4, que deverá ser salvo em um _cookie_ no navegador do
  usuário (ou persistido em sua conta).

### Retornos da API

* Existem dois formatos de retorno, dependendo se a API levanta uma exceção ou não:

  * Sucesso:

```json
{
    "sucesso": true,
    "dados": {
        ....
    }
}
```

  * Problema:

```json
{
    "sucesso": false,
    "dados": {
        "tipo": "... nome da exceção ...",
        "descricao": "mais detalhes do problema"
    }
}
```

* Nos dois casos, é retornado o status HTTP 200.

### Endpoints

#### /novo - Novo carrinho

* Uri: `/novo`
* Método: `POST`
* Parâmetros (POST): nenhum
* Ações: cria um novo carrinho de compras, gera um UUID e retorna.
* Exemplo de retorno:

```json
{
    "dados": {
        "carrinho_codigo": "2a707934-33a3-4e2e-9dd6-23c037be2522"
    },
    "sucesso": true
}
```

#### /cliente-define - Altera cliente

* Uri: `/cliente-define`
* Método: `POST`
* Parâmetros (POST):
    * `carrinho`: código do carrinho (texto)
    * `cliente`: código do cliente (inteiro)
* Ações: altera o cliente associado ao carrinho de compras.
* Exemplo de retorno:

```json
{
    "dados": {},
    "sucesso": true
}
```

#### /produto-adiciona - Novo produto no carrinho

* Uri: `/produto-adiciona`
* Método: `POST`
* Parâmetros (POST):
    * `carrinho`: código do carrinho (texto)
    * `produto`: código do produto (texto)
* Ações: adiciona o produto ao carrinho, com quantidade `1`. Os dados do produto são
  coletados da persistência.
* Exemplo de retorno:

```json
{
     "dados": {},
     "sucesso": true
}
```

#### /produto-remove - Remove produto no carrinho

* Uri: `/produto-remove`
* Método: `POST`
* Parâmetros (POST):
    * `carrinho`: código do carrinho (texto)
    * `produto`: código do produto (texto)
* Ações: remove completamente o produto do carrinho.
* Exemplo de retorno:

```json
{
     "dados": {},
     "sucesso": true
}
```

#### /produto-define-quantidade - Altera quantidade de um produto no carrinho

* Uri: `/produto-define-quantidade`
* Método: `POST`
* Parâmetros (POST):
    * `carrinho`: código do carrinho (texto)
    * `produto`: código do produto (texto)
    * `quantidade`: nova quantidade do produto (inteiro)
* Ações: altera a quantidade do produto no carrinho.
* Exemplo de retorno:

```json
{
     "dados": {},
     "sucesso": true
}
```
* Possíveis erros:
    * Pode retornar a exceção `ProdutoSemEstoqueError` quando não existe estoque
      suficiente do produto para a quantidade no carrinho.

#### /limpa - Apaga produtos no carrinho

* Uri: `/limpa`
* Método: `POST`
* Parâmetros (POST): nenhum
* Ações: remove todos os produtos do carrinho.
* Exemplo de retorno:

```json
{
     "dados": {},
     "sucesso": true
}
```

#### /cupom-define - Associa um cupom de desconto ao carrinho

* Uri: `/cupom-define`
* Método: `POST`
* Parâmetros (POST):
    * `carrinho`: código do carrinho (texto)
    * `cupom`: código do cupom (texto)
* Ações: associa um cupom de desconto ao carrinho, calculando o desconto no total. Os
  dados do cupom são coletados da persistência.
* Exemplo de retorno:

```json
{
     "dados": {},
     "sucesso": true
}
```

#### /carrinho - Obtém todos os dados do carrinho

* Uri: `/carrinho/<codigo>`
* Método: `GET`
* Parâmetros (URL path):
    * `codigo`: código do carrinho (texto)
* Ações: retorna todos os dados do carrinho.
* Exemplo de retorno:

```json
{
  "dados": {
    "cliente": 123456,
    "codigo": "5d05fe31-8363-426e-9de0-481dbca59e84",
    "cupom": {
      "codigo": "BLACKFRIDAY15",
      "valor": 15.0
    },
    "produtos": [
      {
        "codigo": "AB1234567",
        "descricao": "Camiseta Pólo",
        "preco_de": 170.0,
        "preco_por": 170.0,
        "quantidade": 1
      },
      {
        "codigo": "EF3567942",
        "descricao": "Sapato Social Masculino",
        "preco_de": 500.0,
        "preco_por": 450.0,
        "quantidade": 1
      }
    ],
    "totais": {
      "subtotal": 620.0,
      "total": 605.0
    }
  },
  "sucesso": true
}
```

## Dependências para o projeto

O ambiente de desenvolvimento foi testado no Arch Linux.

* Python 3.9
* make
* Docker

## Como criar um ambiente de desenvolvimento

Criar o _virtualenv_ e instalar as dependências:

```shell
make
```

## Como rodar o projeto em ambiente de desenvolvimento

```shell
make run
```

## Como rodar a bateria de testes de unidade

```shell
make tests
```

## Como rodar a bateria de testes de integração

* Em um terminal, inicie o projeto:

```shell
make run
```

* Em outro terminal, rode os testes:

```shell
make testes-integration
```

## Como empacotar para a "produção"

Para criar a imagem do Docker (`zanardo/desafio-api-carrinho`):

```shell
make docker-build
```

## Como executar o projeto usando o Docker

```shell
make docker-run
```

A API será acessível através do endereço: http://127.0.0.1:5000/
