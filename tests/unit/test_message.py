import unittest

import httpx
import respx

import mailpit.api
import mailpit.message as m
import mailpit.models


class MessageModelTestCase(unittest.TestCase):
    RESPONSE = """{
        "ID": "d7a5543b-96dd-478b-9b60-2b465c9884de",
        "Read": true,
        "From": {"Name": "John Doe", "Address": "john@example.com"},
        "To": [{"Name": "Jane Smith", "Address": "jane@example.com"}],
        "Cc": [],
        "Bcc": [],
        "Subject": "Message subject",
        "Date": "2016-09-07T16:46:00+13:00",
        "Text": "Plain text MIME part of the email",
        "HTML": "HTML MIME part (if exists)",
        "Size": 79499,
        "Inline": [
            {
                "PartID": "1.2",
                "FileName": "filename.gif",
                "ContentType": "image/gif",
                "ContentID": "919564503@07092006-1525",
                "Size": 7760
            }
        ],
        "Attachments": [
            {
                "PartID": "2",
                "FileName": "filename.doc",
                "ContentType": "application/msword",
                "ContentID": "",
                "Size": 43520
            }
        ]
    }"""

    message: m.Message = m.Message.from_json(RESPONSE)

    def test_message(self):
        self.assertIsInstance(MessageModelTestCase.message, m.Message)
        self.assertEqual("d7a5543b-96dd-478b-9b60-2b465c9884de", self.message.id)
        self.assertEqual(True, MessageModelTestCase.message.read)
        self.assertEqual("Message subject", self.message.subject)
        self.assertEqual("2016-09-07T16:46:00+13:00", self.message.date)
        self.assertEqual("Plain text MIME part of the email", self.message.text)
        self.assertEqual("HTML MIME part (if exists)", self.message.html)
        self.assertEqual(79499, self.message.size)

    def test_message_from(self):
        self.assertIsInstance(self.message.from_, mailpit.models.Contact)
        self.assertEqual("John Doe", self.message.from_.name)
        self.assertEqual("john@example.com", self.message.from_.address)

    def test_message_to(self):
        self.assertEqual(1, len(self.message.to))
        self.assertIsInstance(self.message.to[0], mailpit.models.Contact)
        self.assertEqual("Jane Smith", self.message.to[0].name)
        self.assertEqual("jane@example.com", self.message.to[0].address)

    def test_message_cc(self):
        self.assertEqual([], self.message.cc)

    def test_message_bcc(self):
        self.assertEqual([], self.message.bcc)


class MessageAPITestCase(unittest.TestCase):
    RESPONSE = {
        "ID": "d7a5543b-96dd-478b-9b60-2b465c9884de",
        "Read": True,
        "From": {"Name": "John Doe", "Address": "john@example.com"},
        "To": [{"Name": "Jane Smith", "Address": "jane@example.com"}],
        "Cc": [],
        "Bcc": [],
        "Subject": "Message subject",
        "Date": "2016-09-07T16:46:00+13:00",
        "Text": "Plain text MIME part of the email",
        "HTML": "HTML MIME part (if exists)",
        "Size": 79499,
        "Inline": [
            {
                "PartID": "1.2",
                "FileName": "filename.gif",
                "ContentType": "image/gif",
                "ContentID": "919564503@07092006-1525",
                "Size": 7760,
            }
        ],
        "Attachments": [
            {
                "PartID": "2",
                "FileName": "filename.doc",
                "ContentType": "application/msword",
                "ContentID": "",
                "Size": 43520,
            }
        ],
    }

    def setUp(self) -> None:
        self.api = mailpit.api.API("https://example.com")

    @respx.mock
    def test_message_get(self):
        route = respx.get(
            "https://example.com/api/v1/message/d7a5543b-96dd-478b-9b60-2b465c9884de",
        )
        route.mock(return_value=httpx.Response(200, json=MessageAPITestCase.RESPONSE))
        message = self.api.get_message("d7a5543b-96dd-478b-9b60-2b465c9884de")
        self.assertIsInstance(message, m.Message)
        self.assertEqual(200, self.api.last_response.status_code)
