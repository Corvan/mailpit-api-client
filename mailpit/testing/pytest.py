"""Module providing helpers for :py:module:`unittest` kind of testing against the
Mailpit-API"""

try:
    import pytest as _pytest
except ImportError:
    _pytest = None

if _pytest:
    import mailpit.client.api as _api
    import mailpit.client.models as _models

    @_pytest.fixture(scope="session")
    def mailpit_api(request):
        """fixture creating a connection to the mailpit API. This fixture is meant to be
        called parametrized, in order to pass the url for which an
        :py:class:`mailpit.client.api.API` instance is created and yielded"""
        client_api = _api.API(request.param)

        yield client_api

        messages = client_api.get_messages()
        client_api.delete_messages([message.id for message in messages.messages])

    def assert_message_equal(first: _models.Message, second: _models.Message):
        assert first == second
