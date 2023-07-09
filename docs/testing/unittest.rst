========
unittest
========
In order to provide some convenience a test-case class has been created with the name :py:class:`~mailpit.testing.unittest.EMailTestCase` deriving from :py:class:`unittest.TestCase`, which is meant to be inherited from, as you would do from :py:class:`~unittest.TestCase`:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         def test_send_message(self):
            ...

The class adds a few methods and attributes, so that you are able to assert, if your message has been sent, or if two messages are equal.

----------
Attributes
----------

_______
api_url
_______
If your Mailpit ist not running on ``localhost:8025``, you can set the classattribute :py:attr:`~mailpit.testing.unittest.EmailTestCase.api_url` to a different URL:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         api_url = "http://my.mailpit.example:8080"

         def test_send_message(self):
            ...


___
api
___

Classes inherited from :py:class:`~mailpit.testing.unittest.EMailTestCase` will connect to the Mailpit-API automatically on creation.
They will provide you with the :py:attr:`~mailpit.testing.unittest.EmailTestCase.mailpit_api` attribute, which is an instance of :py:class:`~mailpit.client.api.API`:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         def test_send_message(self):
            messages = self.api.get_messages([])
            ...

-------------------------
Assert messages are equal
-------------------------
In order to check, whether two E-Mail messages are equal you can use :py:meth:`~mailpit.testing.unittest.EmailTestCase.assertMessageEqual`

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

        def test_messages_equal(self):
            message1 = self.api.get_message("MessageID1")
            message2 = self.api.get.message("MessageID2")

            self.assertMessageEqual(message1, message2)

--------------------------------
Assert message has been received
--------------------------------
In order to check, whether an E-Mail message has been received by Mailpit, you can use
    :py:meth:~mailpit.testing.unittest.EmailTestCase.assertMessageReceived`

.. code-block:: python

    import email
    import smtplib
    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

        def test_messages_received(self):
            smtp_server = smtplib.SMTP("localhost", 1025)
            with open(f"tests/mail/email_without_attachment.eml") as fp:
                mail = email.message_from_file(fp)
            smtp_server.send_message(
                mail,
                from_addr="Sender Smith <sender@example.com>",
                to_addrs="Recipient Ross <recipient@example.com>",
            )
            self.assertMessageReceived(
            "20220727034441.7za34h6ljuzfpmj6@localhost.localhost"
        )
