=======
Testing
=======
To make testing easier there are test-helpers inside the :py:mod:`mailpit.testing` package.

--------
unittest
--------
In order to provide some convenience a test-case class has been created with the name :py:class:`~mailpit.testing.unittest.EMailTestCase` deriving from :py:class:`unittest.TestCase`, which is meant to be inherited from, as you would do from :py:class:`~unittest.TestCase`:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         def test_send_message(self):
            ...

The class adds a few methods and attributes, so that you are able to assert, if your message has been sent, or if two messages are equal.

__________
Attributes
__________

.......
api_url
.......

If your Mailpit ist not running on ``localhost:8025``, you can set the classattribute :py:attr:`~mailpit.testing.unittest.EmailTestCase.api_url` to a different URL:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         api_url = "http://my.mailpit.example:8080"

         def test_send_message(self):
            ...


...
api
...

Classes inherited from :py:class:`~mailpit.testing.unittest.EMailTestCase` will connect to the Mailpit-API automatically on creation.
They will provide you with the :py:attr:`~mailpit.testing.unittest.EmailTestCase.api` attribute, which is an instance of :py:class:`~mailpit.client.api.API`:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         api_url = "http://my.mailpit.example:8080"

         def test_send_message(self):
            messages = self.api.get_messages([])
            ...

_________________________
Assert messages are equal
_________________________
In order to check, whether to E-Mail messages are equal you can use :py:meth:`~mailpit.testing.unittest.EmailTestCase.assertMessageEqual`

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

        def test_messages_equal(self):
            message1 = self.api.get_message("MessageID1")
            message2 = self.api.get.message("MessageID2")

            self.assertMessageEqual(message1, message2)

____________________________
Assert message has been sent
____________________________


------
pytest
------
