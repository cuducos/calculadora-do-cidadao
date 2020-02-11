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

In [4]: ipca.adjust(date(2014, 7, 8), 7)
Out[4]: Decimal('9.407523138792336916983267321')

In [5]: ipca.adjust(date(1998, 7, 12), 3, date(2006, 7, 1))
Out[5]: Decimal('5.279855889296777979447848574')
```

[![asciicast](https://asciinema.org/a/295920.svg)](https://asciinema.org/a/295920)

## Mini-guia de contribuição

### Testes

A suíte de testes roda com diversas versões do Python via [`tox`](https://pypi.org/project/tox/). Se você não tiver instalado, `pip install tox` deve resolver.

```console
$ tox
```

Se quiser rodar os testes mais rapidamente apenas para a versão em uso, é possível utilizar o [`pytest`](https://docs.pytest.org/), mas é necessário instalar alguns pacotes extras:

```console
$ pip install pytest pytest-black pytest-cov pytest-mock pytest-mypy
```

#### Escrevendo testes de novos adaptadores

Quando criar m novo adaptador, escreva ao menos três casos de teste para o método `adjust`:

1. Utilizando apenas um argumento (data original)
1. Utilizando dois argumentos (data original mais valor personalizado)
1. Utilizando três argumentos (data original, valor personalizado e data final)

### Documentação

Para visualizar alterações na documentação, é preciso instalar alguns pacotes e utilizar a o [Sphinx](https://www.sphinx-doc.org/en/):

```console
$ pip install -e .
$ pip install -r docs/requirements.txt
$ sphinx-build docs docs/_build
```

Depois, é só acessar `docs/_build/index.html`.

### Limpeza de arquivos gerados automaticamente

Para limpar os arquivos gerados automaticamente, existe o atalho `make clean`.
