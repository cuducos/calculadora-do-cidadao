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
`DIEESE Cesta Básica: média de todas as cidades disponíveis <https://www.dieese.org.br/cesta/>`_                                             :class:`calculadora_do_cidadao.CestaBasica`
`DIEESE Cesta Básica: média das capitais da Região Centro-Oeste <https://www.dieese.org.br/cesta/>`_                                         :class:`calculadora_do_cidadao.CestaBasicaCentroOeste`
`DIEESE Cesta Básica: média das capitais da Região Nordeste <https://www.dieese.org.br/cesta/>`_                                             :class:`calculadora_do_cidadao.CestaBasicaNordeste`
`DIEESE Cesta Básica: média das capitais da Região Norte <https://www.dieese.org.br/cesta/>`_                                                :class:`calculadora_do_cidadao.CestaBasicaNorte`
`DIEESE Cesta Básica: média das capitais da Região Sudeste <https://www.dieese.org.br/cesta/>`_                                              :class:`calculadora_do_cidadao.CestaBasicaSudeste`
`DIEESE Cesta Básica: média das capitais da Região Sul <https://www.dieese.org.br/cesta/>`_                                                  :class:`calculadora_do_cidadao.CestaBasicaSul`
`DIEESE Cesta Básica: Aracaju <https://www.dieese.org.br/cesta/>`_                                                                           :class:`calculadora_do_cidadao.CestaBasicaAracaju`
`DIEESE Cesta Básica: Belém  <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaBelem`
`DIEESE Cesta Básica: Belo Horizonte <https://www.dieese.org.br/cesta/>`_                                                                    :class:`calculadora_do_cidadao.CestaBasicaBeloHorizonte`
`DIEESE Cesta Básica: Boa Vista <https://www.dieese.org.br/cesta/>`_                                                                         :class:`calculadora_do_cidadao.CestaBasicaBoaVista`
`DIEESE Cesta Básica: Brasília <https://www.dieese.org.br/cesta/>`_                                                                          :class:`calculadora_do_cidadao.CestaBasicaBrasilia`
`DIEESE Cesta Básica: Campo Grande <https://www.dieese.org.br/cesta/>`_                                                                      :class:`calculadora_do_cidadao.CestaBasicaCampoGrande`
`DIEESE Cesta Básica: Cuiaba <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaCuiaba`
`DIEESE Cesta Básica: Curitiba <https://www.dieese.org.br/cesta/>`_                                                                          :class:`calculadora_do_cidadao.CestaBasicaCuritiba`
`DIEESE Cesta Básica: Florianópolis <https://www.dieese.org.br/cesta/>`_                                                                     :class:`calculadora_do_cidadao.CestaBasicaFlorianopolis`
`DIEESE Cesta Básica: Fortaleza <https://www.dieese.org.br/cesta/>`_                                                                         :class:`calculadora_do_cidadao.CestaBasicaFortaleza`
`DIEESE Cesta Básica: Goiânia <https://www.dieese.org.br/cesta/>`_                                                                           :class:`calculadora_do_cidadao.CestaBasicaGoiania`
`DIEESE Cesta Básica: João Pessoa <https://www.dieese.org.br/cesta/>`_                                                                       :class:`calculadora_do_cidadao.CestaBasicaJoaoPessoa`
`DIEESE Cesta Básica: Macaé <https://www.dieese.org.br/cesta/>`_                                                                             :class:`calculadora_do_cidadao.CestaBasicaMacae`
`DIEESE Cesta Básica: Macapá <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaMacapa`
`DIEESE Cesta Básica: Maceió <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaMaceio`
`DIEESE Cesta Básica: Manaus <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaManaus`
`DIEESE Cesta Básica: Natal <https://www.dieese.org.br/cesta/>`_                                                                             :class:`calculadora_do_cidadao.CestaBasicaNatal`
`DIEESE Cesta Básica: Palmas <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaPalmas`
`DIEESE Cesta Básica: Porto Alegre <https://www.dieese.org.br/cesta/>`_                                                                      :class:`calculadora_do_cidadao.CestaBasicaPortoAlegre`
`DIEESE Cesta Básica: Porto Velho <https://www.dieese.org.br/cesta/>`_                                                                       :class:`calculadora_do_cidadao.CestaBasicaPortoVelho`
`DIEESE Cesta Básica: Recife <https://www.dieese.org.br/cesta/>`_                                                                            :class:`calculadora_do_cidadao.CestaBasicaRecife`
`DIEESE Cesta Básica: Rio Branco <https://www.dieese.org.br/cesta/>`_                                                                        :class:`calculadora_do_cidadao.CestaBasicaRioBranco`
`DIEESE Cesta Básica: Rio de Janeiro <https://www.dieese.org.br/cesta/>`_                                                                    :class:`calculadora_do_cidadao.CestaBasicaRioDeJaneiro`
`DIEESE Cesta Básica: Salvador <https://www.dieese.org.br/cesta/>`_                                                                          :class:`calculadora_do_cidadao.CestaBasicaSalvador`
`DIEESE Cesta Básica: São Luís <https://www.dieese.org.br/cesta/>`_                                                                          :class:`calculadora_do_cidadao.CestaBasicaSaoLuis`
`DIEESE Cesta Básica: São Paulo <https://www.dieese.org.br/cesta/>`_                                                                         :class:`calculadora_do_cidadao.CestaBasicaSaoPaulo`
`DIEESE Cesta Básica: Teresina <https://www.dieese.org.br/cesta/>`_                                                                          :class:`calculadora_do_cidadao.CestaBasicaTeresina`
`DIEESE Cesta Básica: Vitória <https://www.dieese.org.br/cesta/>`_                                                                           :class:`calculadora_do_cidadao.CestaBasicaVitoria`
`FED's Consumer Price Index for All Urban Consumers: All Items <https://fred.stlouisfed.org/series/CPIAUCSL>`_                               :class:`calculadora_do_cidadao.AllUrbanCityAverage`
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

================ =========== ============================================================= =============================================== =======================
Argumento        Obrigatório Tipo                                                          Descrição                                       Valor padrão
================ =========== ============================================================= =============================================== =======================
`original_date`  ✅          `datetime.date`, `datetime.datetime`, `str`, `int` ou `float` Data original do valor a ser corrigido.
`value`          ❌          `decimal.Decimal`, `float` ou `int`                           Valor a ser corrigido.                          `decimal.Decimal('1')`
`target_date`    ❌          `datetime.date`, `datetime.datetime`, `str`, `int` ou `float` Data para quando o valor tem que ser corrigido. `datetime.date.today()`
================ =========== ============================================================= =============================================== =======================


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

.. _Formatos dos campos de data:

Formatos dos campos de data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Os adaptadores aceitam diversos formatos de data, como descrevem os exemplos a seguir:

========================================= =================== ===========================
Entrada                                   Tipo                Saída
========================================= =================== ===========================
`datetime.date(2018, 7, 6)`               `datetime.date`     `datetime.date(2018, 7, 6)`
`datetime.datetime(2018, 7, 6, 21, 0, 0)` `datetime.datetime` `datetime.date(2018, 7, 6)`
`"2018-07-06T21:00:00"`                   `str`               `datetime.date(2018, 7, 6)`
`"2018-07-06 21:00:00"`                   `str`               `datetime.date(2018, 7, 6)`
`"2018-07-06"`                            `str`               `datetime.date(2018, 7, 6)`
`"06/07/2018"`                            `str`               `datetime.date(2018, 7, 6)`
`"2018-07"`                               `str`               `datetime.date(2018, 7, 1)`
`"Jul/2018"`                              `str`               `datetime.date(2018, 7, 1)`
`"Jul-2018"`                              `str`               `datetime.date(2018, 7, 1)`
`"Jul 2018"`                              `str`               `datetime.date(2018, 7, 1)`
`"07/2018"``                              `str`               `datetime.date(2018, 7, 1)`
`"2018"`                                  `str`               `datetime.date(2018, 1, 1)`
`1530925200`                              `int` (timestamp)   `datetime.date(2018, 7, 6)`
`1530925200.0`                            `float` (timestamp) `datetime.date(2018, 7, 6)`
========================================= =================== ===========================

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
