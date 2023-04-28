import email
import logging
import smtplib

import logging518.config
import pytest as _pt

import mailpit.client.api as _c_api
import mailpit.client.messages as _c_messages
import mailpit.client.models as _c_models


_log = logging.getLogger("tests")
_project_path = "/root/mailpit-api-client"
logging518.config.fileConfig(f"{_project_path}/pyproject.toml")


class TestMessages:

    @_pt.fixture
    def api(self):
        return _c_api.API("http://mailpit:8025")

    @_pt.fixture
    def smtp_server(self):
        _log.info("connecting to smtp_server")
        smtp_server = smtplib.SMTP("mailpit", 1025)
        yield smtp_server
        _log.info("closing smtp server connection")
        smtp_server.quit()

    def test_messages_endpoint__empty(self, api):
        _log.info("call `api.getmessages()`")
        messages = api.get_messages()
        _log.debug(f"messages: {messages}")
        assert len(messages.messages) == 0

    def test_messages_endpoint__sendmessage(self, smtp_server, api):
        _log = logging.getLogger("tests")
        _log.info("reading mail from file")
        with open(f"{_project_path}/tests/mail/email.eml") as fp:
            mail = email.message_from_file(fp)
            _log.debug(f"mail: `{mail}`")
        _log.info("sending message")
        smtp_server.send_message(
            mail,
            from_addr="Sender Smith <sender@example.com>",
            to_addrs="Recipient Ross <recipient@example.com>",
        )
        _log.info("retrieving messages via API-endpoint")
        messages = api.get_messages()
        _log.debug(f"messages: {messages}")

        _log.info("checking asserts")
        messages_expected = _c_messages.Messages(
            total=1,
            count=1,
            unread=1,
            start=0,
            messages=[
                _c_messages.Message(
                    # NOTE: this is on purpose,
                    # because those next 3 values cannot be predicted
                    id=messages.messages[0].id,
                    created=messages.messages[0].created,
                    size=messages.messages[0].size,
                    from_=_c_models.Contact(
                        name="Sender Smith", address="sender@example.com"
                    ),
                    to=[
                        _c_models.Contact(
                            name="Recipient Ross", address="recipient@example.com"
                        )
                    ],
                    cc=[],
                    bcc=[],
                    read=False,
                    subject="Plain text message",
                    attachments=0,
                )
            ],
        )

        assert messages == messages_expected
