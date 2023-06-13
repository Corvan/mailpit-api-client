import os
import re

import pytest as _pt


class TestSMTPConnect:
    @_pt.fixture
    def connection_response(self, log, smtp_server):
        log.info("connecting to smtp_server")
        if os.environ["HOME"] == "/root":
            response = smtp_server.connect("mailpit", 1025)
        else:
            response = smtp_server.connect("localhost", 1025)

        log.debug(f"response: {response}")
        return response

    def test_smtp_connect__response_code(self, connection_response):
        assert 220 == connection_response[0]

    def test_smtp_connect__response_message(self, connection_response):
        assert "Mailpit ESMTP Service" in connection_response[1].decode("UTF-8")

    def test_smtp_connect__check_esmtp(self, smtp_server):
        assert not smtp_server.does_esmtp


class TestSMTP:
    @_pt.fixture
    def server_helo_response(self, log, smtp_server):
        log.info("sending HELO to SMTP-server")
        response = smtp_server.helo("integration")
        log.debug(f"response: {response}")
        return response

    @_pt.fixture
    def server_ehlo_response(self, log, smtp_server):
        log.info("sending EHLO to SMTP-server")
        response = smtp_server.ehlo("integration")
        log.debug(f"response: {response}")
        return response

    def test_helo__response_code(self, server_helo_response):
        assert 250 == server_helo_response[0]

    def test_helo__response_message(self, server_helo_response):
        assert re.match(
            r"[a-zA-Z0-9]{0,12} greets integration",
            server_helo_response[1].decode("UTF-8"),
        )

    def test_ehlo__response_code(self, server_ehlo_response):
        assert 250 == server_ehlo_response[0]

    def test_ehlo__response_message(self, server_ehlo_response):
        assert re.match(
            r"[a-zA-Z0-9]{0,12} greets integration",
            server_ehlo_response[1].decode("UTF-8"),
        )

    def test_sendmail(self, log, smtp_server):
        log.info("sending mail to SMTP-server")
        response = smtp_server.sendmail(
            from_addr="test@example.com",
            to_addrs="receipient@example.com",
            msg="""
 From: Me@my.org
 Subject: testin'

This is a test """,
        )
        log.debug(f"response: {response}")
        assert {} == response
