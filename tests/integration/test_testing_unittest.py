import datetime as _datetime
import email as _email
import logging as _logging
import os as _os
import smtplib as _smtplib
import unittest as _unittest

import logging518.config

from mailpit.testing.unittest import EMailTestCase
import mailpit.client.models as _models

if _os.environ["HOME"] == "/root":
    PROJECT_PATH = "/root/mailpit-api-client"
else:
    PROJECT_PATH = "."

logging518.config.fileConfig(f"{PROJECT_PATH}/pyproject.toml")
_log = _logging.getLogger("tests")


class TestMail(EMailTestCase):
    _log.debug(f"HOME={_os.environ['HOME']}")
    if _os.environ["HOME"] == "/root":
        api_url = "http://mailpit:8025"
    else:
        api_url = "http://localhost:8025"

    def test_api_object(self):
        messages: _models.Messages = self.api.get_messages()
        self.assertEqual(0, len(messages.messages))

    def test_assert_messages_equal__equal(self):
        first = _models.Message(
            id="d7a5543b-96dd-478b-9b60-2b465c9884de",
            message_id="20220727034441.7za34h6ljuzfpmj6@localhost.localhost",
            read=True,
            subject="Message subject",
            date=_datetime.datetime(
                year=2016,
                month=9,
                day=7,
                hour=16,
                minute=46,
                second=00,
                tzinfo=_datetime.timezone(_datetime.timedelta(hours=13)),
            ),
            text="Plain text MIME part of the email",
            html="HTML MIME part (if exists)",
            size=79499,
            from_=_models.Contact(name="John Doe", address="john@example.com"),
            to=[_models.Contact(name="Jane Smith", address="jane@example.com")],
            cc=[],
            bcc=[],
            inline=[
                _models.Attachment(
                    part_id="1.2",
                    file_name="filename.gif",
                    content_type="image/gif",
                    content_id="919564503@07092006-1525",
                    size=7760,
                )
            ],
            attachments=[
                _models.Attachment(
                    part_id="2",
                    file_name="filename.doc",
                    content_type="application/msword",
                    content_id="",
                    size=43520,
                )
            ],
        )
        second = _models.Message(
            id="d7a5543b-96dd-478b-9b60-2b465c9884de",
            message_id="20220727034441.7za34h6ljuzfpmj6@localhost.localhost",
            read=True,
            subject="Message subject",
            date=_datetime.datetime(
                year=2016,
                month=9,
                day=7,
                hour=16,
                minute=46,
                second=00,
                tzinfo=_datetime.timezone(_datetime.timedelta(hours=13)),
            ),
            text="Plain text MIME part of the email",
            html="HTML MIME part (if exists)",
            size=79499,
            from_=_models.Contact(name="John Doe", address="john@example.com"),
            to=[_models.Contact(name="Jane Smith", address="jane@example.com")],
            cc=[],
            bcc=[],
            inline=[
                _models.Attachment(
                    part_id="1.2",
                    file_name="filename.gif",
                    content_type="image/gif",
                    content_id="919564503@07092006-1525",
                    size=7760,
                )
            ],
            attachments=[
                _models.Attachment(
                    part_id="2",
                    file_name="filename.doc",
                    content_type="application/msword",
                    content_id="",
                    size=43520,
                )
            ],
        )
        self.assertMessageEqual(first, second)

    def test_assert_messages_equal__not_equal(self):
        first = _models.Message(
            id="d7a5543b-96dd-478b-9b60-2b465c9884de",
            message_id="20220727034441.7za34h6ljuzfpmj6@localhost.localhost",
            read=True,
            subject="Message subject",
            date=_datetime.datetime(
                year=2016,
                month=9,
                day=7,
                hour=16,
                minute=46,
                second=00,
                tzinfo=_datetime.timezone(_datetime.timedelta(hours=13)),
            ),
            text="Plain text MIME part of the email",
            html="HTML MIME part (if exists)",
            size=79499,
            from_=_models.Contact(name="John Doe", address="john@example.com"),
            to=[_models.Contact(name="Jane Smith", address="jane@example.com")],
            cc=[],
            bcc=[],
            inline=[
                _models.Attachment(
                    part_id="1.2",
                    file_name="filename.gif",
                    content_type="image/gif",
                    content_id="919564503@07092006-1525",
                    size=7760,
                )
            ],
            attachments=[
                _models.Attachment(
                    part_id="2",
                    file_name="filename.doc",
                    content_type="application/msword",
                    content_id="",
                    size=43520,
                )
            ],
        )
        second = _models.Message(
            id="d7a5543b-96dd-478b-9b60-2b465c9884de",
            message_id="inequal",
            read=True,
            subject="Message subject",
            date=_datetime.datetime(
                year=2016,
                month=9,
                day=7,
                hour=16,
                minute=46,
                second=00,
                tzinfo=_datetime.timezone(_datetime.timedelta(hours=13)),
            ),
            text="Plain text MIME part of the email",
            html="HTML MIME part (if exists)",
            size=79499,
            from_=_models.Contact(name="John Doe", address="john@example.com"),
            to=[_models.Contact(name="Jane Smith", address="jane@example.com")],
            cc=[],
            bcc=[],
            inline=[
                _models.Attachment(
                    part_id="1.2",
                    file_name="filename.gif",
                    content_type="image/gif",
                    content_id="919564503@07092006-1525",
                    size=7760,
                )
            ],
            attachments=[
                _models.Attachment(
                    part_id="2",
                    file_name="filename.doc",
                    content_type="application/msword",
                    content_id="",
                    size=43520,
                )
            ],
        )
        with self.assertRaises(AssertionError) as ae:
            self.assertMessageEqual(first, second)


class TestMailSend(EMailTestCase):
    if _os.environ["HOME"] == "/root":
        api_url = "http://mailpit:8025"
        project_path = "/root/mailpit-api-client"
    else:
        api_url = "http://localhost:8025"
        project_path = "."

    def setUp(self) -> None:
        if _os.environ["HOME"] == "/root":
            self.smtp_server = _smtplib.SMTP("mailpit", 1025)
        else:
            self.smtp_server = _smtplib.SMTP("localhost", 1025)
        with open(f"{self.project_path}/tests/mail/email_without_attachment.eml") as fp:
            mail = _email.message_from_file(fp)
        self.smtp_server.send_message(
            mail,
            from_addr="Sender Smith <sender@example.com>",
            to_addrs="Recipient Ross <recipient@example.com>",
        )

    def tearDown(self) -> None:
        self.smtp_server.quit()
        self.api.delete_messages([])

    def test_assert_message_received__received(self):
        self.assertMessageReceived(
            "20220727034441.7za34h6ljuzfpmj6@localhost.localhost"
        )

    def test_assert_message_received__not_received(self):
        with self.assertRaises(AssertionError) as ae:
            self.assertMessageReceived("test@testing.org")
        self.assertRegex(
            str(ae.exception), "Message not found, so it has not been received"
        )


class TestSetUpClassWithSuper(EMailTestCase):
    if _os.environ["HOME"] == "/root":
        api_url = "http://mailpit:8025"
    else:
        api_url = "http://localhost:8025"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_api_object(self):
        messages: _models.Messages = self.api.get_messages()
        self.assertEqual(0, len(messages.messages))


class TestSetUpClassWithoutSuper(EMailTestCase):
    if _os.environ["HOME"] == "/root":
        api_url = "http://mailpit:8025"
    else:
        api_url = "http://localhost:8025"

    @classmethod
    def setUpClass(cls):
        pass

    def test_api_object(self):
        with self.assertRaises(AttributeError) as ae:
            messages: _models.Messages = self.api.get_messages()
        self.assertEqual(
            "'NoneType' object has no attribute 'get_messages'", str(ae.exception)
        )


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


def test_unittest_from_pytest__test_mail():
    test_loader = _unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestMail)
    test_result = _unittest.TestResult()
    test_result = test_suite.run(test_result)
    assert test_result.wasSuccessful()


def test_unittest_from_pytest__test_mail_received():
    test_loader = _unittest.TestLoader()
    test_suite = test_loader.loadTestsFromTestCase(TestMailSend)
    test_result = _unittest.TestResult()
    test_result = test_suite.run(test_result)
    assert test_result.wasSuccessful()