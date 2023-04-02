import unittest
import mailpit.api


class TestMessages(unittest.TestCase):
    def setUp(self) -> None:
        self.api = mailpit.api.API("http://mailpit:8025")

    def test_messages_endpoint__empty(self):
        messages = self.api.get_messages()
        self.assertEqual(len(messages.messages), 0)
