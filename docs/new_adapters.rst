Desenvolvendo novos adaptadores
===============================

Todos os adaptadores herdam de :class:`calculadora_do_cidadao.adapters.Adapter`.

Método obrigatório
------------------

Todo adaptador precisa de um método `serialize`. Esse método sempre recebe uma linha da tabela (`NamedTuple` instanciada pela `rows <https://github.com/turicas/rows>`_ e é um **gerador** que devolve:

* ou `None` (caso seja uma linha inválida)
* ou uma tupla contendo um `datetime.date` e um `decimal.Decimal`

Variáveis obrigatórias
----------------------

=========== ============================================================
Variável    Descrição
=========== ============================================================
`url`       URL da fonte para baixar os dados.
`file_type` `"html"` ou `"xls"`, indicando o formato dos dados na fonte.
=========== ============================================================

Métodos opcionais
-----------------

`post_processing`
~~~~~~~~~~~~~~~~~

Um método estático (``staticmethod``) ou função que recebe `bytes` como seu único argumento e também retorna `bytes`. Utilizado quando o documento a ser baixado está corrimpido na fonte, por exemplo. Essa função é executada antes de salvar o arquivo, dando a chance de corrigi-lo caso necessário.

Variáveis opcionais
-------------------

`HEADERS`
~~~~~~~~~

No caso de a URL usar o protocolo HTTP, essa variável pode ser um dicionário que será incluído como _headers_ em cada requisição HTTP.

`COOKIES`
~~~~~~~~~

No caso de a URL usar o protocolo HTTP, essa variável pode ser um dicionário que será incluído como _cookies_ da sessão na requisição HTTP.

`SHOULD_UNZIP`
~~~~~~~~~~~~~~

Um booleano informando se o arquivo baixado da URL precisa ser descompactado ou não (apenas `.zip` é suportado por enquanto).

`SHOULD_AGGREGATE`
~~~~~~~~~~~~~~~~~~

Um booleano informando se os dados estão desagregados (por exemplo, 0,42%) ou se eles já representam o acumulado desde o início da série (1,0042, por exemplo).

`IMPORT_KWARGS`
~~~~~~~~~~~~~~~

Argumentos nomeados que serem passados passados para a função de leitura dos dados (`rows.import_from_html`, por exemplo).

Essa variável pode ser um dicionário e, nesse caso, a função de leitura será chamada apenas uma vez, desempacotando o dicionário como argumentos nomeados.

Ainda, essa variável pode ser uma sequência de dicionários e, nesse caso, a função de leitura será chamada várias vezes, uma vez para cada dicionário da sequência.

`POST_DATA`
~~~~~~~~~~~

Dicionário com valores que serão passados via HTTP POST para a URL especificada nesse adaptdor. A requisição HTTP será do tipo GET caso essa variável não seja criada.

Ainda, essa variável pode ser uma sequência de dicionários e, nesse caso, serão feitas várias requisições, uma com cada conunto de dados dessa sequência.
