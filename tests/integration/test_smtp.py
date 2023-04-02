import unittest
import smtplib

import mailpit.api


class TestMessages(unittest.TestCase):
    def setUp(self) -> None:
        self.api_endpoint = "http://mailpit:8025"
        self.smtp_server = smtplib.SMTP("mailpit", 1025)
        self.api = mailpit.api.API(self.api_endpoint)

    def tearDown(self) -> None:
        self.smtp_server.quit()
        self.smtp_server.close()

    def test_smtp__connect(self):

        response = self.smtp_server.connect("mailpit", 1025)
        self.assertEqual(220, response[0])
        self.assertRegex(response[1].decode("UTF-8"), "Mailpit ESMTP Service")
        self.assertEqual("AF_INET", self.smtp_server.sock.family.name)
        self.assertFalse(self.smtp_server.does_esmtp)

    def test_smtp__helo(self):
        response = self.smtp_server.helo("integration")
        self.assertEqual(250, response[0])
        self.assertRegex(
            response[1].decode("UTF-8"), r"[a-zA-Z0-9]{0,12} greets integration"
        )

    def test_ehlo(self):
        response = self.smtp_server.ehlo("integration")
        self.assertEqual(250, response[0])
        self.assertRegex(
            response[1].decode("UTF-8"), r"[a-zA-Z0-9]{0,12} greets integration"
        )

    def test_sendmail(self):
        response = self.smtp_server.sendmail(
            from_addr="test@example.com",
            to_addrs="receipient@example.com",
            msg="""
 From: Me@my.org
 Subject: testin'

This is a test """,
        )
        self.assertDictEqual({}, response)
