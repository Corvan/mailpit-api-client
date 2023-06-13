import email as _email
import logging as _logging
import os as _os
import pathlib as _pathlib
import smtplib as _smtplib

import logging518.config
import pytest as _pt

import mailpit.client.api as _api

if _os.environ["HOME"] == "/root":
    _project_path = _pathlib.Path("/root/mailpit-api-client")
elif _pathlib.Path(_os.environ["HOME"]).is_relative_to(_pathlib.Path("/github")):
    _project_path = _pathlib.Path(_os.environ["GITHUB_WORKSPACE"])
else:
    _project_path = _pathlib.Path(".")


@_pt.fixture(scope="session")
def log():
    logging518.config.fileConfig(f"{_project_path}/pyproject.toml")
    return _logging.getLogger("tests")


@_pt.fixture(scope="module")
def api():
    if _os.environ["HOME"] == "/root" or _pathlib.Path(
        _os.environ["HOME"]
    ).is_relative_to(_pathlib.Path("/github")):
        client_api = _api.API("http://mailpit:8025")
    else:
        client_api = _api.API("http://localhost:8025")
    yield client_api
    messages = client_api.get_messages()
    client_api.delete_messages([message.id for message in messages.messages])


# noinspection PyShadowingNames
@_pt.fixture(scope="module")
def smtp_server(log, api):
    log.info("connecting to smtp_server")
    if _os.environ["HOME"] == "/root" or _pathlib.Path(
        _os.environ["HOME"]
    ).is_relative_to(_pathlib.Path("/github")):
        server = _smtplib.SMTP("mailpit", 1025)
    else:
        server = _smtplib.SMTP("localhost", 1025)
    yield server
    log.info("closing smtp server connection")
    server.quit()


@_pt.fixture(scope="session")
def message_with_attachment():
    return _pathlib.Path("tests/mail/email_with_attachment.eml")


@_pt.fixture(scope="session")
def message_without_attachment():
    return _pathlib.Path("tests/mail/email_without_attachment.eml")


@_pt.fixture(scope="session")
def message_with_inline_attachment():
    return _pathlib.Path("tests/mail/email_with_inline_attachment.eml")


@_pt.fixture(scope="session")
def message_with_attachment_and_inline_attachment():
    return _pathlib.Path("tests/mail/email_with_attachment_and_inline_attachment.eml")


# noinspection PyShadowingNames
@_pt.fixture(scope="class")
def sent_message_id(smtp_server, api, log):
    def _sent_message_id(file: _pathlib.Path):
        with open(_project_path / file) as fp:
            mail = _email.message_from_file(fp)
            log.info("sending message")
            smtp_server.send_message(
                mail,
                from_addr="Sender Smith <sender@example.com>",
                to_addrs="Recipient Ross <recipient@example.com>",
            )
            messages = api.get_messages()
            log.debug(f"Message ID: {messages.messages[0].id}")
            return messages.messages[0].id

    yield _sent_message_id

    messages = api.get_messages()
    api.delete_messages([message.id for message in messages.messages])
