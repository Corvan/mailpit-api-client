import unittest as _unittest

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


class TestSetUpClassWithSuper(EMailTestCase):
    api_url = "http://mailpit:8025"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_api_object(self):
        messages: _messages.Messages = self.api.get_messages()
        self.assertEqual(0, len(messages.messages))


def test_unittest_from_pytest__test_mail():
    test_loader = _unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestMail)
    test_result = _unittest.TestResult()
    test_result = test_suite.run(test_result)
    assert test_result.wasSuccessful()


def test_unittest_from_pytest__test_setup_class_without_super():
    test_loader = _unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestSetUpClassWithoutSuper)
    test_result = _unittest.TestResult()
    test_result = test_suite.run(test_result)
    assert test_result.wasSuccessful()


def test_unittest_from_pytest__test_setup_class_with_super():
    test_loader = _unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestSetUpClassWithSuper)
    test_result = _unittest.TestResult()
    test_result = test_suite.run(test_result)
    assert test_result.wasSuccessful()
