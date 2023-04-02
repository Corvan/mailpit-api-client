import unittest
import smtplib

import mailpit.api
import logging518.config


class MailpitClientIntegrationCase(unittest.TestCase):

    PROJECT_PATH = "/root/mailpit-api-client"

    def setUp(self) -> None:
        logging518.config.fileConfig(f"{self.PROJECT_PATH}/pyproject.toml")
        self.api_endpoint = "http://mailpit:8025"
        self.api = mailpit.api.API(self.api_endpoint)


class MailpitClientIntegrationSMTPCase(MailpitClientIntegrationCase):
    def setUp(self) -> None:
        self.smtp_server = smtplib.SMTP("mailpit", 1025)

    def tearDown(self) -> None:
        self.smtp_server.quit()
        self.smtp_server.close()
