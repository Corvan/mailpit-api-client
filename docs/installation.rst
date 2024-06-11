============
Installation
============

This documentation assumes you are familiar with `pip <https://pip.pypa.io/en/stable/getting-started/>`_ and how to use it on your operating system.

Additionally consider using virtual environments, be it with `venv <https://docs.python.org/3/library/venv.html>`_, `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_, `pipx <https://pypa.github.io/pipx/>`_, `poetry <https://python-poetry.org>`_ or whatever else you'd like to use.

----
PyPI
----
You can find the Project on `PyPI <https://pypi.org>`_ under `<https://pypi.org/project/mailpit-api-client/>`_

It can simply be installed:

________
unittest
________

If you want to use it with `unittest <https://docs.python.org/3/library/unittest.html>`_
simply type

.. code-block:: bash

    pip install mailpit-api-client

______
pytest
______

If you want to install it with `pytest <https://pytest.org>`_, type

.. code-block:: bash

    pip install mailpit-api-client[pytest]

This will have pytest as additional dependency.

------
GitHub
------
You can install it from `GitHub <https://github.com/Corvan/mailpit-api-client.git>`_ directly as well

________
unittest
________
.. code-block:: bash

    pip install https://github.com/Corvan/mailpit-api-client.git

______
pytest
______
.. code-block:: bash

    pip install https://github.com/Corvan/mailpit-api-client.git[pytest]

______________________
Cloning git repository
______________________

Or if you want to clone the repository

.. code-block:: bash

    git clone https://github.com/Corvan/mailpit-api-client.git
