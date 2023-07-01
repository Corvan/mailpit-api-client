===========
Development
===========

--------------------
Install dependencies
--------------------

.. code-block:: python

    pip install -e ".[docs,test,pytest,build]"

.. code-block:: bash

    make clean
    sphinx-apidoc -d 4 -eM -f -o generated ../mailpit
    make html
