"""Module providing helpers for :py:mod:`unittest` kind of testing against the
Mailpit-API"""

try:
    import pytest as _pytest
except ImportError:
    _pytest = None

if _pytest:
    import pathlib as _pathlib
    import os as _os
    import mailpit.client.api as _api
    import mailpit.client.models as _models

    @_pytest.fixture(scope="session")
    def mailpit_api(request):
        """fixture creating a connection to the mailpit API. This fixture is meant to be
        called parametrized, in order to pass the url for which an
        :py:class:`mailpit.client.api.API` instance is created and yielded"""
        try:
            client_api = _api.API(request.param)
        except AttributeError:
            if _pathlib.Path(_os.environ["HOME"]).is_relative_to(
                _pathlib.Path("/tmp/pytest-of-root")
            ):
                client_api = _api.API("http://mailpit:8025")
            else:
                client_api = _api.API("http://localhost:8025")

        yield client_api

        messages = client_api.get_messages()
        client_api.delete_messages([message.id for message in messages.messages])

    def assert_message_equal(first: _models.Message, second: _models.Message):
        assert first == second
