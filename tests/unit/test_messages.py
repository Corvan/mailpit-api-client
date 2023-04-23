import httpx
import pytest
import respx

import mailpit.client.messages as _c_messages
import mailpit.client.models as _c_models
import mailpit.client.api as _c_api


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
              "Created": "2022-10-03T21:35:32.228605299+13:00",
              "Size": 6144,
              "Attachments": 0
            }
        ]
    }"""

    @pytest.fixture(scope="class")
    def messages(self, response) -> _c_messages.Messages:
        yield _c_messages.Messages.from_json(response)

    @pytest.fixture(scope="class")
    def message(self, messages) -> _c_messages.Message:
        yield messages.messages[0]

    def test_messages(self, messages):
        assert isinstance(messages, _c_messages.Messages)

        assert 500 == messages.total
        assert 500 == messages.unread
        assert 50 == messages.count
        assert 0 == messages.start

    def test_message(self, message):
        assert isinstance(message, _c_messages.Message)
        assert "1c575821-70ba-466f-8cee-2e1cf0fcdd0f" == message.id
        assert message.read is False
        assert "Message subject" == message.subject
        assert "2022-10-03T21:35:32.228605299+13:00" == message.created
        assert 6144 == message.size
        assert 0 == message.attachments

    def test_message_from(self, message):
        assert isinstance(message.from_, _c_models.Contact)
        assert "John Doe" == message.from_.name
        assert "john@example.com" == message.from_.address

    def test_message_to(self, message):
        assert isinstance(message.to[0], _c_models.Contact)
        assert "Jane Smith" == message.to[0].name
        assert "jane@example.com" == message.to[0].address

    def test_message_cc(self, message):
        assert isinstance(message.cc[0], _c_models.Contact)
        assert "Accounts" == message.cc[0].name
        assert "accounts@example.com" == message.cc[0].address

    def test_message_bcc(self, message):
        assert [] == message.bcc


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
                    "Created": "2022-10-03T21:35:32.228605299+13:00",
                    "Size": 6144,
                    "Attachments": 0,
                }
            ],
        }

    @pytest.fixture
    def api(self) -> _c_api.API:
        yield _c_api.API("https://example.com")

    @respx.mock
    def test_messages_get(self, api, response):
        route = respx.get("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json=response))

        messages = api.get_messages()

        assert isinstance(messages, _c_messages.Messages)
        assert route.called is True
        assert 200 == api.last_response.status_code

    @respx.mock
    def test_messages_delete(self, api):
        route = respx.delete("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        api.delete_messages(["1", "2", "3"])

        assert route.called is True
        assert 200 == api.last_response.status_code

    @respx.mock
    def test_messages_put(self, api):
        route = respx.put("https://example.com/api/v1/messages")
        route.mock(return_value=httpx.Response(200, json={"body": "ok"}))

        api.put_messages(["1", "2", "3"], "Read", True)

        assert route.called is True
        assert 200 == api.last_response.status_code

