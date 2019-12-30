```python
In [1]: from calculadora_do_cidadao import CalculadoraDoCidadão

In [2]: from datetime import date

In [3]: c = CalculadoraDoCidadão()

In [4]: c(42.00, date(2010, 1, 1))
Out[4]:
  {'Data inicial': datetime.date(2010, 1, 1),
   'Data final': datetime.date(2019, 12, 1),
   'Valor nominal': 42.0,
   'Índice de correção no período': 1.8773205,
   'Valor corrigido na data final': 78.85}
```
