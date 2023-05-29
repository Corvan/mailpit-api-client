import datetime

import httpx
import pytest
import respx

import mailpit.client.models.messages as _messages
import mailpit.client.models as _models
import mailpit.client.api as _api


class TestMessagesModels:
    @pytest.fixture(scope="class")
    def response(self) -> str:
        yield """{
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
              "Created": "2022-10-03T21:35:32.228605+13:00",
              "Size": 6144,
              "Attachments": 0
            }
        ]
    }"""

    @pytest.fixture(scope="class")
    def messages(self, response) -> _messages.Messages:
        yield _messages.Messages.from_json(response)

    @pytest.fixture(scope="class")
    def message(self, messages) -> _messages.Message:
        yield messages.messages[0]

    def test_messages(self, messages):
        assert isinstance(messages, _messages.Messages)

        assert messages.total == 500
        assert messages.unread == 500
        assert messages.count == 50
        assert messages.start == 0

    def test_message(self, message):
        assert isinstance(message, _messages.Message)
        assert "1c575821-70ba-466f-8cee-2e1cf0fcdd0f" == message.id
        assert message.read is False
        assert message.subject == "Message subject"
        assert message.created == datetime.datetime(
            year=2022,
            month=10,
            day=3,
            hour=21,
            minute=35,
            second=32,
            microsecond=228605,
            tzinfo=datetime.timezone(datetime.timedelta(hours=13)),
        )
        assert 6144 == message.size
        assert 0 == message.attachments

    def test_message_from(self, message):
        assert isinstance(message.from_, _models.Contact)
        assert message.from_.name == "John Doe"
        assert message.from_.address == "john@example.com"

    def test_message_to(self, message):
        assert isinstance(message.to[0], _models.Contact)
        assert message.to[0].name == "Jane Smith"
        assert message.to[0].address == "jane@example.com"

    def test_message_cc(self, message):
        assert isinstance(message.cc[0], _models.Contact)
        assert message.cc[0].name == "Accounts"
        assert message.cc[0].address == "accounts@example.com"

    def test_message_bcc(self, message):
        assert message.bcc == []


class TestMessagesAPI:
    @pytest.fixture(scope="class")
    def response(self) -> str:
        yield {
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
                    "Created": "2022-10-03T21:35:32.228605+13:00",
                    "Size": 6144,
                    "Attachments": 0,
                }
            ],
        }

    @pytest.fixture
    def api(self) -> _api.API:
        yield _api.API("https://example.com")

    @respx.mock
    def test_messages_get(self, api, response):
        route = respx.get("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json=response))

        messages = api.get_messages()

        assert isinstance(messages, _messages.Messages)
        assert route.called is True
        assert api.last_response.status_code == 200

    @respx.mock
    def test_messages_delete(self, api):
        route = respx.delete("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        api.delete_messages(["1", "2", "3"])

        assert route.called is True
        assert api.last_response.status_code == 200

    @respx.mock
    def test_messages_put(self, api):
        route = respx.put("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        api.put_messages(["1", "2", "3"], "Read", True)

        assert route.called is True
        assert api.last_response.status_code == 200
