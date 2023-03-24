import unittest

import httpx
import respx

import mailpit.api
import mailpit.message


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
        self.assertIsInstance(message, mailpit.message.Message)
        self.assertEqual(200, self.api.last_response.status_code)
