==================
mailpit-api-client
==================
-------------------------------------------------------------------
API-client for https://github.com/axllent/mailpit written in Python
-------------------------------------------------------------------

:Authors:
    Lars Liedtke <corvan@gmx.de>
:Version:
    0.10.3

----------
Motivation
----------
For work, I thought about introducing integration testing.
We are working with `Odoo <https://github.com/odoo/odoo>`_  and I wanted to test if e-mails created by Odoo really were sent.
I remembered `mailhog <https://github.com/mailhog/MailHog>`_, which I discovered to be abandoned.
Searching for an alternative, I found Mailpit - for which I decided to write an API-client in my free time.

-----
Usage
-----

this library - as is Mailpit - is mostly meant for testing. Giving the url of Mailpit to a tool to send e-mail messages to and then use this client to check on the API if the mail was sent.

------
Client
------

The client itself consists of the class ``API`` in `mailpit/client/api.py <mailpit/client/api.py>`_, that offers methods, which query the API-Endpoints and are named respectively.
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

messages will be an instance of ``mailpit.client.models.Messages`` , which you can find in link:mailpit/client/models/messages.py[mailpit/client/models.py]. +
The model-classes' attributes are named the same as Mailpit's responses, as documented in the API's `README.md <https://github.com/axllent/mailpit/blob/develop/docs/apiv1/README.md>`_, but as is convention in Python in Snakecase.

For examples have a look at the link:tests[tests]

== Testing

To make testing easier I plan to provide testhelpers like TestCase-classes of ``unittest`` and ``pytest``-fixtures.

=== unittest
tbd

=== pytest
tbd

.. [1] If you have it running differently, you have to adjust the URL you pass.
