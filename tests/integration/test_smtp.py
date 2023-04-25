import logging
import smtplib
import re

import logging518.config
import pytest


@pytest.fixture
def smtp_server():
    smtp_server = smtplib.SMTP("mailpit", 1025)

    yield smtp_server

    smtp_server.close()


class TestSMTPConnect:
    
    def test_smtp__connect(self, smtp_server):
        logger = logging.getLogger(
            "tests.integration.TestSMTPConnect.test_smtp__connect"
        )
        logger.info("connecting to smtp_server")
        response = smtp_server.connect("mailpit", 1025)
        logger.debug(f"response: {response}")

        assert 220 == response[0]
        assert "Mailpit ESMTP Service" in response[1].decode("UTF-8") 
        assert smtp_server.does_esmtp is False

        logger.info("closing connection to smtp_server")
        

class TestSMTP:
    
    @pytest.fixture
    def project_path(self) -> str:
        return "/root/mailpit-api-client"
    
    @pytest.fixture
    def log(self, project_path):
        logging518.config.fileConfig(f"{project_path}/pyproject.toml")
    
    def test_helo(self, smtp_server, log):
        logger = logging.getLogger("tests.integration.TestSMTP.test_helo")
        logger.info("sending HELO to SMTP-server")
        response = smtp_server.helo("integration")
        logger.debug(f"response: {response}")
        assert 250 == response[0]
        assert re.match(r"[a-zA-Z0-9]{0,12} greets integration", 
                        response[1].decode("UTF-8"))

    def test_ehlo(self, smtp_server, log):
        logger = logging.getLogger("tests.integration.TestSMTP.test_ehlo")
        logger.info("sending EHLO to SMTP-server")
        response = smtp_server.ehlo("integration")
        logger.debug(f"response: {response}")
        assert 250 == response[0]
        assert re.match(r"[a-zA-Z0-9]{0,12} greets integration",
                        response[1].decode("UTF-8"))

    def test_sendmail(self, smtp_server: pytest.fixture, log: pytest.fixture):
        logger = logging.getLogger("tests.integration.TestSMTP.test_sendmail")
        logger.info("sending mail to SMTP-server")
        response = smtp_server.sendmail(
            from_addr="test@example.com",
            to_addrs="receipient@example.com",
            msg="""
 From: Me@my.org
 Subject: testin'

This is a test """,
        )
        logger.debug(f"response: {response}")
        assert {} == response
