Uso
===

Todos os adaptadores podem sem iniciados sem argumento algum. Nesse caso, os adaptadores fazem o download dos dados na hora que a classe é instanciada. Ou seja, criar uma instância demora e **é recomendado que sua aplicação faça isso na inicialização, e não a cada uso**.

Como alternativa, caso você já tenha salvo esses dados localmente (ver :ref:`Exportando os dados`), é possível iniciar qualquer adaptador passando um `pathlib.Path` de onde ele deve ler os dados.

::

    from pathlib import Path

    from calculadora_do_cidadao import Ipca


    backup = Path("backup.csv")

    ipca = Ipca()  # vai fazer o download nesse momento
    ipca.to_csv(backup)

    ipca = Ipca(backup)  # não fará o download, carregará do backup

Adaptadores disponíveis
-----------------------

============================================================================================================================================ ==================================================
Índice                                                                                                                                       Módulo
============================================================================================================================================ ==================================================
`IGP-M <https://portalibre.fgv.br/estudos-e-pesquisas/indices-de-precos/igp/>`_                                                              :class:`calculadora_do_cidadao.Igpm`
`INPC <https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-indice-nacional-de-precos-ao-consumidor.html>`_                  :class:`calculadora_do_cidadao.Inpc`
`IPCA <https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html>`_            :class:`calculadora_do_cidadao.Ipca`
`IPCA-15 <https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9260-indice-nacional-de-precos-ao-consumidor-amplo-15.html>`_      :class:`calculadora_do_cidadao.Ipca15`
`IPCA-E <https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9262-indice-nacional-de-precos-ao-consumidor-amplo-especial.html>`_ :class:`calculadora_do_cidadao.IpcaE`
`Selic <https://receita.economia.gov.br/orientacao/tributaria/pagamentos-e-parcelamentos/taxa-de-juros-selic>`_                              :class:`calculadora_do_cidadao.Selic`
============================================================================================================================================ ==================================================

Uso de um adaptador
-------------------

Todos os adaptadores tem o método `adjust` (:meth:`calculadora_do_cidadao.adapters.Adapter.adjust`) que recebe três argumentos:

================ =========== =================================== =============================================== =======================
Argumento        Obrigatório Tipo                                Descrição                                       Valor padrão 
================ =========== =================================== =============================================== =======================
`original_date`  ✅          `datetime.date`                     Data original do valor a ser corrigido.  
`value`          ❌          `decimal.Decimal`, `float` ou `int` Valor a ser corrigido.                          `decimal.Decimal('1')` 
`target_date`    ❌          `datetime.date`                     Data para quando o valor tem que ser corrigido. `datetime.date.today()` 
================ =========== =================================== =============================================== =======================


Exemplo
~~~~~~~

::

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

.. _Exportando os dados:

Exportando os dados
-------------------

Todos os adaptadores tem o método `to_csv` (:meth:`calculadora_do_cidadao.adapters.Adapter.to_csv`) para exportar os dados no formato CSV. O único argumento que esse método recebe é um `pathlib.Path` que é o caminho do arquivo para onde os dados serão exportados.

Para exportar os dados de todos os índices (adaptadores) de uma vez só é só chamar o pacote pela linha de comando (será criado o arquivo `calculadora-do-cidadao.csv` com os dados):

::

    $ python -m calculadora_do_cidadao

Importando os dados
-------------------

Todos os adaptadores tem o método `from_csv` (:meth:`calculadora_do_cidadao.adapters.Adapter.from_csv`) para importar os dados de um arquivo CSV. O único argumento que esse método recebe é um `pathlib.Path` que é o caminho do arquivo onde os dados estão. O arquivo deve ter duas colunas, `date` no formato `YYYY-MM-DD`, e `value` utilizando um ponto como separador das casas decimais.
