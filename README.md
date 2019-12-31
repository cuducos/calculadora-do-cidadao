# Calculadora do Cidadão

Pacote em Python para uso da [Calculadora do Cidadão](https://www3.bcb.gov.br/CALCIDADAO/publico/exibirFormCorrecaoValores.do?method=exibirFormCorrecaoValores) do Banco Central do Brasil.

## Instalação

```console
$ pip install git+https://github.com/cuducos/calculadora-do-cidadao.git
```

Ou, se você quiser usar a versão assíncrona:


```console
$ pip install git+https://github.com/cuducos/calculadora-do-cidadao.git[aio]
```

## Uso


```python
In [1]: from calculadora_do_cidadao import CalculadoraDoCidadão

In [2]: from datetime import date

In [3]: calculadora = CalculadoraDoCidadão()

In [4]: calculadora date(2010, 1, 1))
Out[4]:
  {'Data inicial': datetime.date(2010, 1, 1),
   'Data final': datetime.date(2019, 12, 1),
   'Valor nominal': 42.0,
   'Índice de correção no período': 1.8773205,
   'Valor corrigido na data final': 78.85}
```

Ou, para a versão assíncrona:

```python
In [1]: from asyncio import run

In [2]: from datetime import date

In [3]: from aiohttp import ClientSession

In [4]: from calculadora_do_cidadao import CalculadoraDoCidadãoAsyncio

In [5]: calculadora = CalculadoraDoCidadãoAsyncio()

In [6]: async def main():
   ...:     async with ClientSession() as sessão:
   ...:         return await calculadora(sessão, 42.00, date(2010, 1, 1))
   ...:

 In [7]: run(main())
 Out[7]:
 {'Data inicial': datetime.date(2010, 1, 1),
  'Data final': datetime.date(2019, 12, 1),
  'Valor nominal': 42.0,
  'Índice de correção no período': 1.8773205,
  'Valor corrigido na data final': 78.85}
```
