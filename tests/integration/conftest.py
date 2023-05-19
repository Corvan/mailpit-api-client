import email
import logging
import smtplib

import logging518.config
import pytest as _pt

import mailpit.client.api as _c_api


_project_path = "/root/mailpit-api-client"


@_pt.fixture(scope="session")
def log():
    logging518.config.fileConfig(f"{_project_path}/pyproject.toml")
    return logging.getLogger("tests")


@_pt.fixture
def api():
    client_api = _c_api.API("http://mailpit:8025")
    yield client_api
    client_api.delete_messages(
        message.id for message in client_api.get_messages().messages
    )


@_pt.fixture
def smtp_server(log, api):
    log.info("connecting to smtp_server")
    server = smtplib.SMTP("mailpit", 1025)
    yield server
    log.info("closing smtp server connection")
    server.quit()


@_pt.fixture
def message(smtp_server, log):
    log.info("reading mail from file")
    with open(f"{_project_path}/tests/mail/email.eml") as fp:
        mail = email.message_from_file(fp)
        # _log.debug(f"mail: `{mail}`")
    log.info("sending message")
    smtp_server.send_message(
        mail,
        from_addr="Sender Smith <sender@example.com>",
        to_addrs="Recipient Ross <recipient@example.com>",
    )
