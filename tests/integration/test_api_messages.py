import mailpit.client.models.messages as _c_messages
import mailpit.client.models as _c_models


class TestAPIMessages:
    def test_messages_endpoint__empty(self, log, api):
        log.info("call `api.getmessages()`")
        messages = api.get_messages()
        log.debug(f"messages: {messages}")
        assert len(messages.messages) == 0

    def test_messages_endpoint__sendmessage(self, log, sent_message_id, api):
        log.info("reading mail from file")

        log.info("retrieving messages via API-endpoint")
        messages = api.get_messages()
        log.debug(f"messages: {messages}")

        log.info("checking asserts")
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