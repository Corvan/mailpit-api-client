import email
import logging
import smtplib
import unittest

import mailpit.api
import mailpit.messages
import mailpit.models

import logging518.config


class TestMessages(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.project_path = "/root/mailpit-api-client"
        logging518.config.fileConfig(f"{self.project_path}/pyproject.toml")
        logger = logging.getLogger("tests.integration.setUp.TestMessages.setUp")
        self.api_endpoint = "http://mailpit:8025"
        self.api = mailpit.api.API(self.api_endpoint)
        logger.info("connecting to smtp_server")
        self.smtp_server = smtplib.SMTP("mailpit", 1025)

    def tearDown(self) -> None:
        logger = logging.getLogger("tests.integration.TestMessages.tearDown")
        logger.info("closing smtp server connection")
        self.smtp_server.quit()

    def test_messages_endpoint__empty(self):
        messages = self.api.get_messages()
        self.assertEqual(len(messages.messages), 0)

    def test_messages_endpoint__sendmessage(self):
        logger = logging.getLogger(
            "tests.integration.test_messages_endpoint__sendmessage"
        )
        logger.info("reading mail from file")
        with open(f"{self.project_path}/tests/mail/email.eml") as fp:
            mail = email.message_from_file(fp)
        logger.info("sending message")
        self.smtp_server.send_message(
            mail,
            from_addr="Sender Smith <sender@example.com>",
            to_addrs="Recipient Ross <recipient@example.com>",
        )
        logger.info("retrieving messages via API-endpoint")
        messages = self.api.get_messages()

        logger.info("closing smtp connection")

        logger.info("checking asserts")
        messages_expected = mailpit.messages.Messages(
            total=1,
            count=1,
            unread=1,
            start=0,
            messages=[
                mailpit.messages.Message(
                    # NOTE: this is on purpose,
                    # because those next 3 values cannot be predicted
                    id=messages.messages[0].id,
                    created=messages.messages[0].created,
                    size=messages.messages[0].size,
                    from_=mailpit.models.Contact(
                        name="Sender Smith", address="sender@example.com"
                    ),
                    to=[
                        mailpit.models.Contact(
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

        self.assertEqual(messages_expected, messages)
