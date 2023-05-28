from mailpit.testing.unittest import EMailTestCase
import mailpit.client.models.messages as _messages


class TestMail(EMailTestCase):
    api_url = "http://mailpit:8025"

    def test_api_object(self):
        messages: _messages.Messages = self.api.get_messages()
        self.assertEqual(0, len(messages.messages))


class TestSetUpClassWithoutSuper(EMailTestCase):
    api_url = "http://mailpit:8025"

    @classmethod
    def setUpClass(cls):
        pass

    def test_api_object(self):
        with self.assertRaises(AttributeError) as ae:
            messages: _messages.Messages = self.api.get_messages()
        self.assertEqual(
            "'NoneType' object has no attribute 'get_messages'", str(ae.exception)
        )


class TestSetUpClassWithtSuper(EMailTestCase):
    api_url = "http://mailpit:8025"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_api_object(self):
        messages: _messages.Messages = self.api.get_messages()
        self.assertEqual(0, len(messages.messages))
