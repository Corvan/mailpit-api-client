import logging
import re

import pytest


class TestSMTPConnect:
    
    def test_smtp__connect(self, log, smtp_server):
        log.info("connecting to smtp_server")
        response = smtp_server.connect("mailpit", 1025)
        log.debug(f"response: {response}")

        assert 220 == response[0]
        assert "Mailpit ESMTP Service" in response[1].decode("UTF-8") 
        assert smtp_server.does_esmtp is False

        log.info("closing connection to smtp_server")
        

class TestSMTP:
    
    def test_helo(self, log, smtp_server):
        log.info("sending HELO to SMTP-server")
        response = smtp_server.helo("integration")
        log.debug(f"response: {response}")
        assert 250 == response[0]
        assert re.match(r"[a-zA-Z0-9]{0,12} greets integration", 
                        response[1].decode("UTF-8"))

    def test_ehlo(self, log, smtp_server):
        logger = logging.getLogger("tests.integration.TestSMTP.test_ehlo")
        logger.info("sending EHLO to SMTP-server")
        response = smtp_server.ehlo("integration")
        logger.debug(f"response: {response}")
        assert 250 == response[0]
        assert re.match(r"[a-zA-Z0-9]{0,12} greets integration",
                        response[1].decode("UTF-8"))

    def test_sendmail(self, log, smtp_server: pytest.fixture):
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
