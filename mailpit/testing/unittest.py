"""Module providing helpers for :py:module:`unittest` kind of testing against the
Mailpit-API"""
from typing import Optional
import unittest as _unittest

import mailpit.client.models as _models
import mailpit.client.api as _api


class EMailTestCase(_unittest.TestCase):
    """:py:class:`unittest.TestCase` derived class with added test-helper methods and
    attributes, in order to test against the Mailpit-API. Simply derive from this class,
    as you would from :py:class:`unittest.TestCase` and write your tests as you are used
    to.


    e.g.::

        class ExampleTestCase(EMailTestCase):

            def test_api_object(self):
            messages: mailpit.client.models.Messages = self.api.get_messages()
            self.assertEqual(0, len(messages.messages))
    """

    api_url: str = "http://localhost:8025"
    """URL pointing to the Mailpit-API to test, if you need to use another url,
    override this attribute in your derived class"""
    api: Optional[_api.API] = None
    """API object created on class setup for testing against Mailpit's API, access this
    object if you need to communicate directly with the API in your tests. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addTypeEqualityFunc(_models.Message, self.assertMessageEqual)

    @classmethod
    def setUpClass(cls) -> None:
        """Creates the class attribute object for the API, on creation of this class and
        classes derived from it. Remember to call :py:func:`super().setUpClass()` while
        subclassing and overriding this method"""
        super().setUpClass()
        cls.api = _api.API(cls.api_url)

    def assertMessageEqual(
        self, first: _models.Message, second: _models.Message, msg: Optional[str] = None
    ):
        """Fail if two instances of :py:class:`Message` are not equal as determined
        by the '==' operator

        e.g.::

            import mailpit.client.models

            class ExampleTestCase(EMailTestCase):

                def test_example(self):
                    message1 = mailpit.client.models.Message(...)
                    message2 = mailpit.client.models.Message(...)
                    self.assertMessageEqual(message1, message2)
        """
        if first != second:
            raise self.failureException(
                self._formatMessage(msg, f"{first} != {second}")
            )

    def assertMessageReceived(
        self,
        message_id: str,
        msg: Optional[str] = None,
    ):
        """Fail if the passed message has not been sent to Mailpit"""
        if self.api is None:
            raise self.failureException(
                self._formatMessage(msg, "self.api may not be None")
            )
        messages: _models.Messages = self.api.get_messages()
        if message_id not in [message.message_id for message in messages.messages]:
            raise self.failureException(
                self._formatMessage(
                    msg, "Message not found, so it has not been received"
                )
            )
