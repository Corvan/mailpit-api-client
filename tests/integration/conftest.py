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


@_pt.fixture(scope="module")
def api():
    client_api = _c_api.API("http://mailpit:8025")
    yield client_api
    messages = client_api.get_messages()
    client_api.delete_messages([message.id for message in messages.messages])


# noinspection PyShadowingNames
@_pt.fixture(scope="module")
def smtp_server(log, api):
    log.info("connecting to smtp_server")
    server = smtplib.SMTP("mailpit", 1025)
    yield server
    log.info("closing smtp server connection")
    server.quit()


# noinspection PyShadowingNames
@_pt.fixture(scope="class")
def sent_message_id_without_attachment(smtp_server, api, log):
    log.info("reading mail from file")
    with open(f"{_project_path}/tests/mail/email_without_attachment.eml") as fp:
        mail = email.message_from_file(fp)
    log.info("sending message")
    smtp_server.send_message(
        mail,
        from_addr="Sender Smith <sender@example.com>",
        to_addrs="Recipient Ross <recipient@example.com>",
    )
    messages = api.get_messages()
    log.debug(f"Message ID: {messages.messages[0].id}")
    yield messages.messages[0].id
    api.delete_messages([message.id for message in messages.messages])


# noinspection PyShadowingNames
@_pt.fixture(scope="class")
def sent_message_id_with_attachment(smtp_server, api, log):
    log.info("reading mail from file")
    with open(f"{_project_path}/tests/mail/email_without_attachment.eml") as fp:
        mail = email.message_from_file(fp)
    log.info("sending message")
    smtp_server.send_message(
        mail,
        from_addr="Sender Smith <sender@example.com>",
        to_addrs="Recipient Ross <recipient@example.com>",
    )
    messages = api.get_messages()
    log.debug(f"Message ID: {messages.messages[0].id}")
    yield messages.messages[0].id
    api.delete_messages([message.id for message in messages.messages])
