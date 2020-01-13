# Calculadora do Cidadão

Pacote em Python para correção de valores.

## Instalação

```console
$ pip install calculadora-do-cidadao
```

## Uso

Os adaptadores disponíveis são:

* [`calcladora_do_cidadao.Ipca`](https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html)

Todos os adaptadores (ver listagem a seguir) fazem o download dos dados na hora que a classe é instanciada. Esses dados ficam no atributo `data` da instância da classe do adaptador.

Ou seja, criar uma instância de demora e **é recomendado que sua aplicação faça isso na inicialização, e não a cada uso**.

Todos os adaptadores tem o método `adjust` que recebe três argumentos:

| Argumento | Obrigatório | Tipo |Descrição | Valor padrão |
|---|:-:|:-:|---|:-:|
| `original_date` | ✅ | `datetime.date` | Data original do valor a ser corrigido. | |
| `value` | ❌ | `decimal.Decimal`, `float` ou `int` | Valor a ser corrigido. | `decimal.Decimal('1')` |
| `target_date` | ❌ |  `datetime.date` | Data para quando o valor tem que ser corrigido. | `datetime.date.today()` |


### Exemplo de uso

```
In [1]: from datetime import date
   ...: from decimal import Decimal
   ...: from calculadora_do_cidadao import Ipca

In [4]: ipca = Ipca()

In [5]: ipca.adjust(date(2018, 7, 6))
Out[5]: Decimal('1.051202206630561280035407253')

In [6]: ipca.adjust(date(2014, 7, 8), 7)
Out[6]: Decimal('9.407523138792336916983267321')

In [7]: ipca.adjust(date(1998, 7, 12), 3, date(2006, 7, 1))
Out [7]: Decimal('5.279855889296777979447848574')
```

## Testes

```
$ python setup.py test
```