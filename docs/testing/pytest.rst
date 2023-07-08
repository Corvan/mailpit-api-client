======
pytest
======
In order to provide some convenience a :py:func:`pytest.fixtures <pytest.fixture>` has
been created.

-------------------
Mailpit-API fixture
-------------------
:py:func:`~mailpit.testing.pytest.mailpit_api` is a :py:mod:`pytest` :py:func:`fixture <pytest.fixture>`, that sets up an API connection and returns it as :py:class:`~mailpit.client.api.API` object.

The fixture has got a scope of ``session`` and it will call :py:meth:`API.delete_messages() <mailpit.client.api.API.delete_messages>` with an empty list to delete all messages, when it goes out of scope.

As with other pytest plugins you have to enable this library in your ``conftest.py``:

.. code-block:: python

    pytest_plugins = ["mailpit.testing.pytest"]


Now it is possible to use the fixture:

.. code-block:: python

    def test_example(mailpit_api):
        mailpit_api.get_messages([])


The fixture has got a default of ``http://localhost:8025``.
In order to pass the api url to this fixture, you have to parametrize your test function with the ``indirect`` parameter set to ``True``.

.. code-block:: python

    import pytest

    api_url = "localhost:8025"

    @pytest.mark.parametrize("mailpit_api", [api_url], indirect=True)
    def test_example(mailpit_api):
        mailpit_api.get_messages([])



