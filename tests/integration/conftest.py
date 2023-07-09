import email
import logging
import os as os
import pathlib
import smtplib

import logging518.config
import pytest

import mailpit.client.api as api

if os.environ["HOME"] == "/root":
    _project_path = pathlib.Path("/root/mailpit-api-client")
elif pathlib.Path(os.environ["HOME"]).is_relative_to(pathlib.Path("/github")):
    _project_path = pathlib.Path(os.environ["GITHUB_WORKSPACE"])
else:
    _project_path = pathlib.Path(".")


@pytest.fixture(scope="session")
def log():
    logging518.config.fileConfig(f"{_project_path}/pyproject.toml")
    return logging.getLogger("tests")


@pytest.fixture(scope="module")
def mailpit_api():
    if os.environ["HOME"] == "/root" or pathlib.Path(os.environ["HOME"]).is_relative_to(
        pathlib.Path("/github")
    ):
        client_api = api.API("http://mailpit:8025")
    else:
        client_api = api.API("http://localhost:8025")
    yield client_api
    messages = client_api.get_messages()
    client_api.delete_messages([message.id for message in messages.messages])


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def smtp_server(log, mailpit_api):
    log.info("connecting to smtp_server")
    if os.environ["HOME"] == "/root" or pathlib.Path(os.environ["HOME"]).is_relative_to(
        pathlib.Path("/github")
    ):
        server = smtplib.SMTP("mailpit", 1025)
    else:
        server = smtplib.SMTP("localhost", 1025)
    yield server
    log.info("closing smtp server connection")
    server.quit()


@pytest.fixture(scope="session")
def message_with_attachment():
    return pathlib.Path("tests/mail/email_with_attachment.eml")


@pytest.fixture(scope="session")
def message_without_attachment():
    return pathlib.Path("tests/mail/email_without_attachment.eml")


@pytest.fixture(scope="session")
def message_with_inline_attachment():
    return pathlib.Path("tests/mail/email_with_inline_attachment.eml")


@pytest.fixture(scope="session")
def message_with_attachment_and_inline_attachment():
    return pathlib.Path("tests/mail/email_with_attachment_and_inline_attachment.eml")


# noinspection PyShadowingNames
@pytest.fixture(scope="class")
def sent_message_id(smtp_server, mailpit_api, log):
    def _sent_message_id(file: pathlib.Path):
        with open(_project_path / file) as fp:
            mail = email.message_from_file(fp)
            log.info("sending message")
            smtp_server.send_message(
                mail,
                from_addr="Sender Smith <sender@example.com>",
                to_addrs="Recipient Ross <recipient@example.com>",
            )
            messages = mailpit_api.get_messages()
            log.debug(f"Message ID: {messages.messages[0].id}")
            return messages.messages[0].id

    yield _sent_message_id

    messages = mailpit_api.get_messages()
    mailpit_api.delete_messages([message.id for message in messages.messages])
