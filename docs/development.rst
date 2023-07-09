===========
Development
===========
If you want to hack on this little library clone it via git

.. code-block:: bash

    git clone https://github.com/Corvan/mailpit-api-client.git

or

.. code-block:: bash

    git clone git@github.com:Corvan/mailpit-api-client.git

Of course you can fork it first on GitHub.
Then you are easily able to open PRs, which is the preferred way of contributing code.

--------------------
Install dependencies
--------------------
It is recommended to use a virtual environment, in order to separate the dependencies
for this project from dependencies of other projects.
There are several tools out there to manage virtual environments, so please consult the
respective documentantion if you're not using ``venv`` or ``poetry``

If you want to run the tests :ref:`for all possible versions of Python <invoke-tasks>`
you have to install `Docker Engine <https://docs.docker.com/engine/install/>`_, and the
`Docker Compose plugin <https://docs.docker.com/compose/install/linux/>`_ on Linux.
Or you install `Docker Desktop <https://docs.docker.com/get-docker/>`_ on other
operating system and on Linux.

___
pip
___

in order to install the Python dependencies enter the directory of your just cloned
git repository, activate your virtual environment and type:

.. code-block:: python

    pip install -e ".[docs,test,pytest,build]"


Now you can start hacking.

______
poetry
______
If you want to use poetry as the manager for your virtual environment, install it if
necessary and run

.. code-block:: bash

    poetry update

inside the project's directory.

In order to run the :ref:`invoke-tasks` you have to prefix all commands given there with

.. code-block:: bash

    poetry run

so running the Invoke task of unittests you have to type

.. code-block:: bash

    poetry run invoke tests.unit

-----------------
Running the tests
-----------------
This project uses `pytest <https://pytest.org>`_ as testing framework.
Even the `unittest <https://docs.python.org/3/library/unittest.html>`_ parts are tested
themselves with ``pytest``.

There are two kinds of tests in this project:

================== =================================================================================================
test type          description
================== =================================================================================================
unit tests         unit tests are tests that check if a functionality works isolated from everything else
integration tests  integration tests are tests that include dependencies, and check if functionalities work together
================== =================================================================================================

You can run the tests locally, but then you have to provide a `running Mailpit by
yourself <https://github.com/axllent/mailpit/blob/develop/README.md>`_ for running the
integration tests.

.. _invoke-tasks:

____________
Invoke tasks
____________

In order to run the tests inside Docker containers, there are
`Invoke <https://www.pyinvoke.org>`_ tasks that use Docker Compose to set-up all the
necessary containers and run the checks and tests in them afterwards.
At the end things are cleaned up again.

.. code-block:: bash

    $ invoke -l

    Available tasks:

    tests.checks
    tests.integration
    tests.unit

There are some more tasks, but you can concentrate on those three.

================= ===============================================================================================
task              description
================= ===============================================================================================
tests.checks      runs code checks, like black (code formatting), ruff (linting), and mypy (static code analysis)
tests.integration runs the integration tests
tests.unit        runs the unit tests
================= ===============================================================================================

To run a task, simply type

.. code-block:: bash

    invoke <task>

It is also possible to run multiple tasks at once

.. code-block:: bash

    invoke tests.checks tests.unit tests.integration

For running the tests all the logging outputs are set to debug.
So running them will produce *a lot* of output, but you will want to know why things
go wrong.
If you want to reduce the amount, have a look at :file:`pyproject.toml`

-----------------------
Build the documentation
-----------------------

.. code-block:: bash

cd docs
    make clean
    sphinx-apidoc -d 4 -eM -f -o generated ../mailpit
    make html
