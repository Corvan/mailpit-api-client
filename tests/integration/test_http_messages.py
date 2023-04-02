import email
import logging
import smtplib

import tests.integration


class TestMessages(tests.integration.MailpitClientIntegrationCase):
    def test_messages_endpoint__empty(self):
        messages = self.api.get_messages()
        self.assertEqual(len(messages.messages), 0)

    def test_messages_endpoint__sendmessage(self):
        logger = logging.getLogger(
            "tests.integration.test_messages_endpoint__sendmessage"
        )
        logger.info("connecting to smtp_server")
        self.smtp_server = smtplib.SMTP("mailpit", 1025)
        logger.info("reading mail from file")
        with open(f"{self.PROJECT_PATH}/tests/mail/email.eml") as fp:
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
        self.smtp_server.quit()
        self.smtp_server.close()

        logger.info("checking asserts")
        self.assertEqual(1, messages.count)
        self.assertEqual(1, len(messages.messages))
