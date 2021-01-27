# Mini-guia de Contribuição

O pacote utiliza o padrão `pyproject.toml` e o [Poetry](https://python-poetry.org/). Para instalar as dependências:

```console
$ poetry install --extras "docs"
```

## Testes

Para rodar os testes apenas com a versão atual do Python:

```console
$ poetry run pytest
```

Para rodar com todas as versões de Python:

```console
$ poetry run tox
```

### Escrevendo testes de novos adaptadores

Quando criar m novo adaptador, escreva ao menos três casos de teste para o método `adjust`:

1. Utilizando apenas um argumento (data original)
1. Utilizando dois argumentos (data original mais valor personalizado)
1. Utilizando três argumentos (data original, valor personalizado e data final)

## Documentação

Para a documentação, é preciso utilizar o [Sphinx](https://www.sphinx-doc.org/en/):

```console
$ poetry run sphinx-build docs docs/_build
```

Depois, é só acessar `docs/_build/index.html`.

## Limpeza de arquivos gerados automaticamente

Para limpar os arquivos gerados automaticamente, existe o atalho `make clean`.
