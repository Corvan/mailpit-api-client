import logging
import unittest
import smtplib


import logging518.config


class TestSMTPConnect(unittest.TestCase):
    @unittest.skip("This leads to python socket complaining about an unclosed socket")
    def test_smtp__connect(self):
        logger = logging.getLogger(
            "tests.integration.TestSMTPConnect.test_smtp__connect"
        )
        logger.info("connecting to smtp_server")
        smtp_server = smtplib.SMTP("mailpit", 1025)
        response = smtp_server.connect("mailpit", 1025)
        logger.debug(f"response: {response}")

        self.assertEqual(220, response[0])
        self.assertRegex(response[1].decode("UTF-8"), "Mailpit ESMTP Service")
        self.assertFalse(smtp_server.does_esmtp)

        logger.info("closing connection to smtp_server")
        smtp_server.close()


class TestSMTP(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.project_path = "/root/mailpit-api-client"
        logging518.config.fileConfig(f"{self.project_path}/pyproject.toml")
        logger = logging.getLogger("tests.integration.TestSMTP.setUp")
        logger.info("connecting to smtp_server")
        self.smtp_server = smtplib.SMTP("mailpit", 1025)

    def tearDown(self) -> None:
        logger = logging.getLogger("tests.integration.TestSMTP.tearDown")
        logger.info("closing smtp server connection")
        self.smtp_server.quit()
        self.smtp_server.close()

    def test_smtp__helo(self):
        logger = logging.getLogger("tests.integration.TestSMTP.test_helo")
        logger.info("sending HELO to SMTP-server")
        response = self.smtp_server.helo("integration")
        logger.debug(f"response: {response}")
        self.assertEqual(250, response[0])
        self.assertRegex(
            response[1].decode("UTF-8"), r"[a-zA-Z0-9]{0,12} greets integration"
        )

    def test_ehlo(self):
        logger = logging.getLogger("tests.integration.TestSMTP.test_ehlo")
        logger.info("sending EHLO to SMTP-server")
        response = self.smtp_server.ehlo("integration")
        logger.debug(f"response: {response}")
        self.assertEqual(250, response[0])
        self.assertRegex(
            response[1].decode("UTF-8"), r"[a-zA-Z0-9]{0,12} greets integration"
        )

    def test_sendmail(self):
        logger = logging.getLogger("tests.integration.TestSMTP.test_sendmail")
        logger.info("sending mail to SMTP-server")
        response = self.smtp_server.sendmail(
            from_addr="test@example.com",
            to_addrs="receipient@example.com",
            msg="""
 From: Me@my.org
 Subject: testin'

This is a test """,
        )
        logger.debug(f"response: {response}")
        self.assertDictEqual({}, response)
