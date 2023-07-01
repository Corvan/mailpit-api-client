=======
Testing
=======
To make testing easier there are test-helpers inside the :py:mod:`mailpit.testing` package.

--------
unittest
--------
In order to provide some convenience a test-case class has been created with the name :py:class:`EMailTestCase` deriving from :py:class:`unittest.TestCase`, which is meant to be inherited from, as you would do from :py:class:`TestCase`:

.. code-block:: python

    from mailpit.testing.unittest import EMailTestCase

    class MyTest(EMailTestCase):

         def test_sending_email():
            ...

The class adds a few methods and attributes, so that you are able to assert, if your message has been sent, or if two messages are equal.