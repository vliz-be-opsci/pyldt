pyldt
===================================

python implementation of LinkedData Templates support to produce triples out of various datasources

Started on 2021-08-18

Setup
-----
Start using this project in a virtual environment

.. code-block:: bash

    $ virtualenv venv
    $ source venv/Scripts/activate
    $ pip install -r requirements.txt

Initialize to grab dependencies

.. code-block:: bash

    $ make init

Build Docs

.. code-block:: bash

    $ make docu

Run Tests

.. code-block:: bash

    $ make test

Developers
----------
``requirements.txt`` could be generated with command below, but maintaining by hand makes more sense

.. code-block:: bash

    $ pip freeze --local > requirements.txt

The initial structure for the Sphinx documentation is in the folder ``docs/``
It gets build by running

.. code-block:: bash

    $ sphinx-quickstart -p prjname -a 'First Last' -v v0.0.0 -r v0.0.0 -M docs/



