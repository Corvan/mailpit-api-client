import unittest as _unittest

import mailpit.client.models.message as _message
import mailpit.client.api as _api


class EMailTestCase(_unittest.TestCase):
    api_url = "http://localhost:8025"
    api: _api.API = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addTypeEqualityFunc(_message.Message, self.assertMessageEqual)

    @classmethod
    def setUpClass(cls) -> None:
        cls.api: _api.API = _api.API(cls.api_url)

    def assertMessageEqual(
        self, message1: _message.Message, message2: _message.Message
    ):
        ...

    def assertMessageReceived(self, message: _message.Message):
        ...
