import unittest

import httpx
import respx

import mailpit.messages
import mailpit.message
import mailpit.api


class MessagesModelsTestCase(unittest.TestCase):
    RESPONSE = """{
        "total": 500,
        "unread": 500,
        "count": 50,
        "start": 0,
        "messages": [
            {
              "ID": "1c575821-70ba-466f-8cee-2e1cf0fcdd0f",
              "Read": false,
              "From": {
                "Name": "John Doe",
                "Address": "john@example.com"
              },
              "To": [
                {
                  "Name": "Jane Smith",
                  "Address": "jane@example.com"
                }
              ],
              "Cc": [
                {
                  "Name": "Accounts",
                  "Address": "accounts@example.com"
                }
              ],
              "Bcc": [],
              "Subject": "Message subject",
              "Created": "2022-10-03T21:35:32.228605299+13:00",
              "Size": 6144,
              "Attachments": 0
            }
        ]
    }"""
    messages: mailpit.messages.Messages = mailpit.messages.Messages.from_json(RESPONSE)
    message: mailpit.messages.Message = messages.messages[0]

    def test_messages(self):
        self.assertIsInstance(
            MessagesModelsTestCase.messages, mailpit.messages.Messages
        )
        self.assertEqual(500, MessagesModelsTestCase.messages.total)
        self.assertEqual(500, MessagesModelsTestCase.messages.unread)
        self.assertEqual(50, MessagesModelsTestCase.messages.count)
        self.assertEqual(0, MessagesModelsTestCase.messages.start)

    def test_message(self):
        self.assertIsInstance(MessagesModelsTestCase.message, mailpit.messages.Message)
        self.assertEqual(
            "1c575821-70ba-466f-8cee-2e1cf0fcdd0f", MessagesModelsTestCase.message.id
        )
        self.assertIs(False, MessagesModelsTestCase.message.read)
        self.assertEqual("Message subject", MessagesModelsTestCase.message.subject)
        self.assertEqual(
            "2022-10-03T21:35:32.228605299+13:00",
            MessagesModelsTestCase.message.created,
        )
        self.assertEqual(6144, MessagesModelsTestCase.message.size)
        self.assertEqual(0, MessagesModelsTestCase.message.attachments)

    def test_message_from(self):
        self.assertIsInstance(
            MessagesModelsTestCase.message.from_, mailpit.models.Contact
        )
        self.assertEqual("John Doe", MessagesModelsTestCase.message.from_.name)
        self.assertEqual(
            "john@example.com", MessagesModelsTestCase.message.from_.address
        )

    def test_message_to(self):
        self.assertIsInstance(
            MessagesModelsTestCase.message.to[0], mailpit.models.Contact
        )
        self.assertEqual("Jane Smith", MessagesModelsTestCase.message.to[0].name)
        self.assertEqual(
            "jane@example.com", MessagesModelsTestCase.message.to[0].address
        )

    def test_message_cc(self):
        self.assertIsInstance(self.message.cc[0], mailpit.models.Contact)
        self.assertEqual("Accounts", MessagesModelsTestCase.message.cc[0].name)
        self.assertEqual(
            "accounts@example.com", MessagesModelsTestCase.message.cc[0].address
        )

    def test_message_bcc(self):
        self.assertEqual([], MessagesModelsTestCase.message.bcc)


class MessagesAPITestCase(unittest.TestCase):
    RESPONSE = {
        "total": 500,
        "unread": 500,
        "count": 50,
        "start": 0,
        "messages": [
            {
                "ID": "1c575821-70ba-466f-8cee-2e1cf0fcdd0f",
                "Read": False,
                "From": {"Name": "John Doe", "Address": "john@example.com"},
                "To": [{"Name": "Jane Smith", "Address": "jane@example.com"}],
                "Cc": [{"Name": "Accounts", "Address": "accounts@example.com"}],
                "Bcc": [],
                "Subject": "Message subject",
                "Created": "2022-10-03T21:35:32.228605299+13:00",
                "Size": 6144,
                "Attachments": 0,
            }
        ],
    }

    def setUp(self) -> None:
        self.api = mailpit.api.API("https://example.com")

    @respx.mock
    def test_messages_get(self):
        route = respx.get("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json=MessagesAPITestCase.RESPONSE))

        messages = self.api.get_messages()

        self.assertIsInstance(messages, mailpit.messages.Messages)
        self.assertTrue(route.called)
        self.assertEqual(200, self.api.last_response.status_code)

    @respx.mock
    def test_messages_delete(self):
        route = respx.delete("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        self.api.delete_messages(["1", "2", "3"])

        self.assertTrue(route.called)
        self.assertEqual(200, self.api.last_response.status_code)

    @respx.mock
    def test_messages_put(self):
        route = respx.put("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        self.api.put_messages(["1", "2", "3"], "Read", True)

        self.assertTrue(route.called)
        self.assertEqual(200, self.api.last_response.status_code)


if __name__ == "__main__":
    unittest.main()
