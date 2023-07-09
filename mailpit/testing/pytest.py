"""Module providing helpers for :py:mod:`unittest` kind of testing against the
Mailpit-API"""

try:
    import pytest
except ImportError:
    pytest = None

if pytest:
    import pathlib as _pathlib
    import os as _os
    import mailpit.client.api as _api

    @pytest.fixture(scope="session")
    def mailpit_api(request):
        """:py:func:`pytest.fixture` creating a connection to the mailpit API.
        This fixture has got a default of ``http://localhost:8025`` but it is possible
        to be called `parametrized <https://docs.pytest.org/en/stable/example/
        parametrize.html #indirect-parametrization>`_ with the parameter
        ``indirect`` set to ``True``, in order to pass the url for which an
        :py:class:`mailpit.client.api.API` instance is created and yielded.
        The fixture has got a scope of ``session`` and it will call
        :py:meth:`API.delete_messages() <mailpit.client.api.API.delete_messages>`
        with an empty list to delete all messages, when it goes out of scope."""
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
