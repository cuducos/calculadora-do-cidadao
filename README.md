# Calculadora do Cidadão

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cuducos/calculadora-do-cidadao/Tests)](https://github.com/cuducos/calculadora-do-cidadao/actions)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/maintainability)
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/cuducos/calculadora-do-cidadao)](https://codeclimate.com/github/cuducos/calculadora-do-cidadao/test_coverage)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)
[![PyPI](https://img.shields.io/pypi/v/calculadora-do-cidadao)](https://pypi.org/project/calculadora-do-cidadao/)

Pacote em Python para correção de valores.

## Instalação

```console
$ pip install calculadora-do-cidadao
```

## Uso

### Adaptadores disponíveis

| Índice | Módulo |
|---|---|
| [__IGP-M__](https://portalibre.fgv.br/estudos-e-pesquisas/indices-de-precos/igp/) | `calculadora_do_cidadao.Igpm` |
| [__INPC__](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-indice-nacional-de-precos-ao-consumidor.html) | `calculadora_do_cidadao.Inpc` |
| [__IPCA__](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html) | `calculadora_do_cidadao.Ipca` |
| [__IPCA-15__](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9260-indice-nacional-de-precos-ao-consumidor-amplo-15.html) | `calculadora_do_cidadao.Ipca15` |
| [__IPCA-E__](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9262-indice-nacional-de-precos-ao-consumidor-amplo-especial.html) | `calculadora_do_cidadao.IpcaE` |
| [__Selic__](https://receita.economia.gov.br/orientacao/tributaria/pagamentos-e-parcelamentos/taxa-de-juros-selic) | `calculadora_do_cidadao.Selic` |

Todos os adaptadores fazem o download dos dados na hora que a classe é instanciada. Esses dados ficam no atributo `data` da instância da classe do adaptador. Ou seja, criar uma instância demora e **é recomendado que sua aplicação faça isso na inicialização, e não a cada uso**.

### Utilizando um adaptador

Todos os adaptadores tem o método `adjust` que recebe três argumentos:

| Argumento | Obrigatório | Tipo |Descrição | Valor padrão |
|---|:-:|:-:|---|:-:|
| `original_date` | ✅ | `datetime.date` | Data original do valor a ser corrigido. | |
| `value` | ❌ | `decimal.Decimal`, `float` ou `int` | Valor a ser corrigido. | `decimal.Decimal('1')` |
| `target_date` | ❌ |  `datetime.date` | Data para quando o valor tem que ser corrigido. | `datetime.date.today()` |


#### Exemplo de uso

```
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

## Desenvolvendo novos adaptadores

Todos os adaptadores herdam de `calculadora_do_cidadao.adapters.Adapter`.

### Método obrigatório

Todo adaptador precisa de um método `serialize`. Esse método sempre recebe uma linha da tabela (`NamedTuple` instanciada pela [`rows`](https://github.com/turicas/rows)) e é um gerador que devolve:

* ou `None` (caso seja uma linha inválida)
* ou uma tupla contendo um `datetime.date` e um `decimal.Decimal`

### Variáveis obrigatórias

| Variável | Descrição |
|---|---|
| `url` | URL da fonte para baixar os dados. |
| `file_type` | `"html"` ou `"xls"`, indicando o formato dos dados na fonte. |

### Variáveis opcionais

| Variável | Descrição |
|---|---|
| `COOKIES` | No caso de a URL usar o protocolo HTTP, essa variável pode ser um dicionário que será incluído como _cookies_ da sessão na requisição HTTP. |
| `SHOULD_UNZIP` | Um booleano informando se o arquivo baixado da URL precisa ser descompactado ou não (apenas `.zip` é suportado por enquanto). |
| `SHOULD_AGGREGATE` | Um booleano informando se os dados estão desagregados (por exemplo, 0,42%) ou se eles já representam o acumulado desde o início da série (1,0042, por exemplo). |
| `IMPORT_KWARGS` | Argumentos nomeados que serem passados passados para a função de leitura dos dados (`rows.import_from_html`, por exemplo).<br><br>Essa variável pode ser um dicionário e, nesse caso, a função de leitura será chamada apenas uma vez, desempacotando o dicionário como argumentos nomeados;<br><br>Ainda, essa variável pode ser uma sequência de dicionários e, nesse caso, a função de leitura será chamada várias vezes, uma vez para cada dicionário da sequência. |


### Testes

A suíte de testes roda com [`tox`](https://pypi.org/project/tox/). Se você não tiver instalado, `pip install tox` deve resolver.

```
$ tox
```

Para limpar os arquivos gerados automaticamente, existe o atalho `make clean`.
