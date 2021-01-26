# Calculadora do Cidadão

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cuducos/calculadora-do-cidadao/Tests)](https://github.com/cuducos/calculadora-do-cidadao/actions)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/maintainability)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/test_coverage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)
[![PyPI](https://img.shields.io/pypi/v/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)
[![](https://img.shields.io/readthedocs/calculadora-do-cidadao)](https://calculadora-do-cidadao.readthedocs.io/)

Pacote em Python para correção de valores. Confira a [documentação](https://calculadora-do-cidadao.readthedocs.io/) para mais detalhes!

## Exemplo de uso

```python
In [1]: from datetime import date
   ...: from decimal import Decimal
   ...: from calculadora_do_cidadao import Ipca

In [2]: ipca = Ipca()

In [3]: ipca.adjust(date(2018, 7, 6))
Out[3]: Decimal('1.051202206630561280035407253')

In [4]: ipca.adjust("2014-07-08", 7)
Out[4]: Decimal('9.407523138792336916983267321')

In [5]: ipca.adjust("12/07/1998", 3, "01/07/2006")
Out[5]: Decimal('5.279855889296777979447848574')
```

[![asciicast](https://asciinema.org/a/295920.svg)](https://asciinema.org/a/295920)

## Mini-guia de contribuição

O pacote utiliza o padrão `pyproject.toml` e o [Poetry](https://python-poetry.org/). Para instalar as dependências:

```console
$ poetry install --extras "docs"
```

### Testes

Para rodar os testes apenas com a versão atual do Python:

```console
$ poetry run pytest
```

Para rodar com todas as versões de Python:

```console
$ poetry run tox
```

#### Escrevendo testes de novos adaptadores

Quando criar m novo adaptador, escreva ao menos três casos de teste para o método `adjust`:

1. Utilizando apenas um argumento (data original)
1. Utilizando dois argumentos (data original mais valor personalizado)
1. Utilizando três argumentos (data original, valor personalizado e data final)

### Documentação

Para a documentação, é preciso utilizar o [Sphinx](https://www.sphinx-doc.org/en/):

```console
$ poetry run sphinx-build docs docs/_build
```

Depois, é só acessar `docs/_build/index.html`.

### Limpeza de arquivos gerados automaticamente

Para limpar os arquivos gerados automaticamente, existe o atalho `make clean`.
