========
vupysolr
========

``vupysolr`` allows to access Solr stored VuFind records. For more information on
VuFind, see https://vufind.org.

Installation
============

.. code-block:: bash

   pip install vupysolr

Usage Examples
==============

Command Line
~~~~~~~~~~~~

::

    $ vupysolr --id 123456789


::

    usage: vupysolr [-h] [--url URL] [--core CORE] [--id ID] [--marc [MARC]]
                    [--decode [DECODE]] [--pretty [PRETTY]]

    optional arguments:
      -h, --help         show this help message and exit
      --url URL          URL of VuFind Solr server (default:
                         http://localhost:8983/solr)
      --core CORE        Name of VuFind Solr core (default: biblio)
      --id ID            ID of record to fetch (default: None)
      --marc [MARC]      Get MARC data only (default: False)
      --decode [DECODE]  Decode MARC data (default: False)
      --pretty [PRETTY]  Pretty print output (default: False)


Interpreter
~~~~~~~~~~~

.. code-block:: python

    import vupysolr


*Create VuFind Solr index client*

.. code-block:: python

    url = "https://vufind.example.com/solr"
    core = "collection"
    index = vupysolr.index(url, core=core, marc=True)


*Retrieve VuFind Solr document from index*

.. code-block:: python

    doc_id = "123456789"
    doc = index.get(doc_id)


*Inspect fields of VuFind Solr document*

.. code-block:: python

    # print document title
    print(doc.title)
    # print timestamp of last indexation
    print(doc.last_indexed)
    # print timestamp of latest transaction (MARC)
    print(doc.marc_latest_transaction)
