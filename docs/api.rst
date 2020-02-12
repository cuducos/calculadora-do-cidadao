API
===

Adaptador Base
--------------

.. autoclass:: calculadora_do_cidadao.adapters.Adapter
   :members:

.. autoexception:: calculadora_do_cidadao.adapters.AdapterNoImportMethod
    :members:

.. autoexception:: calculadora_do_cidadao.adapters.AdapterDateNotAvailableError
    :members:

Adaptadores
-----------

CpiAllUrbanCityAverage (FED's Consumer Price Index for All Urban Consumers: All Items (CpiAllUrbanCityAverage))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. CpiAllUrbanCityAverage:
.. autoclass:: calculadora_do_cidadao.CpiAllUrbanCityAverage
   :members:

IGP-M
~~~~~

.. igpm:
.. autoclass:: calculadora_do_cidadao.Igpm
   :members:

Família IPCA & INPC
~~~~~~~~~~~~~~~~~~~

.. autoclass:: calculadora_do_cidadao.adapters.ibge.IbgeAdapter
   :members:

.. autoclass:: calculadora_do_cidadao.Inpc
   :members:

.. autoclass:: calculadora_do_cidadao.Ipca
   :members:

.. autoclass:: calculadora_do_cidadao.Ipca15
   :members:

.. autoclass:: calculadora_do_cidadao.IpcaE
   :members:

SELIC
~~~~~

.. autoclass:: calculadora_do_cidadao.Selic
   :members:

Download
--------

.. autoclass:: calculadora_do_cidadao.download.Download
   :members:

.. autoexception:: calculadora_do_cidadao.download.DownloadMethodNotImplementedError
   :members:

Campos
------

.. autoclass:: calculadora_do_cidadao.fields.DateField
   :members:

.. autoclass:: calculadora_do_cidadao.fields.PercentField
   :members:
