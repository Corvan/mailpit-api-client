==================
mailpit-api-client
==================
-------------------------------------------------------------------
API-client for https://github.com/axllent/mailpit written in Python
-------------------------------------------------------------------

:Authors:
    Lars Liedtke <corvan@gmx.de>
:Version:
    1.0.0
:Documentation:
    `<https://corvan.github.io/mailpit-api-client/>`_
:PyPI:
    `<https://pypi.org/project/mailpit-api-client/>`_


----------
Motivation
----------
For work, I thought about introducing integration testing.
We are working with `Odoo <https://github.com/odoo/odoo>`_  and I wanted to test if e-mails created by Odoo really were sent.
I remembered `mailhog <https://github.com/mailhog/MailHog>`_, which I discovered to be abandoned.
Searching for an alternative, I found Mailpit - for which I decided to write an API-client in my free time.

-------
Install
-------
If you want to use the library with ``unittest``:

.. code-block:: bash

    pip install mailpit-api-client

If you want to use the library with ``pytest``:

.. code-block:: bash

    pip install mailpit-api-client[pytest]

-----
Usage
-----

this library - as is Mailpit - is mostly meant for testing. Giving the url of Mailpit to a tool to send e-mail messages to and then use this client to check on the API if the mail was sent.

------
Client
------

The client itself consists of the class ``API`` in `<mailpit/client/api.py>`_, that offers methods, which query the API-Endpoints and are named respectively.
To use this class, simply try something like this.
You have to have Mailpit running on localhost for this [1]_ .

.. code-block:: python

    import mailpit.client.api
    api = mailpit.client.api.API("localhost:8025")
    messages = api.get_messages()

Additionally, there are some model-classes that wrap the API's responses.
For example with

.. code-block:: python

    messages = api.get_messages()

messages will be an instance of ``mailpit.client.models.Messages`` , which you can find in `<mailpit/client/models.py>`_.

The model-classes' attributes are named the same as Mailpit's responses, as documented in the API's `README.md <https://github.com/axllent/mailpit/blob/develop/docs/apiv1/README.md>`_, but as is convention in Python in Snakecase.

For examples have a look at the `<tests>`_

-------
Testing
-------

To make testing easier there are test-helpers inside the ``mailpit.testing`` package.

________
unittest
________

In order to provide some convenience a test-case class has been created with the name ``EMailTestCase`` deriving from ``unittest.TestCase``, which is meant to be inherited from, as you would do from ``TestCase``:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         def test_sending_email():
            ...

The class adds a few methods and attributes, so that you are able to assert, if your message has been sent, or if two messages are equal.

______
pytest
______

In order to provide some convenience a :py:func:`pytest.fixtures <pytest.fixture>` has
been created.


Mailpit-API fixture
^^^^^^^^^^^^^^^^^^^

``mailpit.testing.pytest.mailpit_api`` is a ``pytest`` `fixture <https://docs.pytest.org/en/stable/reference/reference.html#fixtures>`_, that sets up an API connection and returns it as ``mailpit.client.api.API`` object.

The fixture has got a scope of ``session`` and it will call ``API.delete_messages()`` with an empty list to delete all messages, when it goes out of scope.

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


.. [1] If you have it running differently, you have to adjust the URL you pass.
