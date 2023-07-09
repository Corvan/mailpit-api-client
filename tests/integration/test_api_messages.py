import pathlib
from typing import Callable

import mailpit.client.models as models


# noinspection PyShadowingNames
class TestAPIMessages:
    def test_messages_endpoint__empty(self, log, mailpit_api):
        log.info("call `api.getmessages()`")
        messages = mailpit_api.get_messages()
        log.debug(f"messages: {messages}")
        assert len(messages.messages) == 0

    def test_messages_endpoint__sendmessage(
        self,
        log,
        sent_message_id: Callable,
        message_without_attachment: pathlib.Path,
        mailpit_api,
    ):
        log.info("reading mail from file")
        sent_message_id(message_without_attachment)

        log.info("retrieving messages via API-endpoint")
        messages = mailpit_api.get_messages()
        log.debug(f"messages: {messages}")

        log.info("checking asserts")
        messages_expected = models.Messages(
            total=1,
            count=1,
            unread=1,
            start=0,
            messages=[
                models.MessageSummary(
                    # NOTE: this is on purpose,
                    # because those next 3 values cannot be predicted
                    id=messages.messages[0].id,
                    message_id="20220727034441.7za34h6ljuzfpmj6@localhost.localhost",
                    created=messages.messages[0].created,
                    size=messages.messages[0].size,
                    from_=models.Contact(
                        name="Sender Smith", address="sender@example.com"
                    ),
                    to=[
                        models.Contact(
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
