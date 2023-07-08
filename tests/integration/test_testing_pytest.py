def test_pytest_helpers(pytester):
    pytester.makeconftest("""pytest_plugins = ["mailpit.testing.pytest"]""")
    pytester.makepyfile(
        """import pytest as _pytest
import os as _os
import pathlib as _pathlib

if _pathlib.Path(_os.environ["HOME"]).is_relative_to(_pathlib.Path("/tmp/pytest-of-root")):
    api_url = "http://mailpit:8025"
else:
    api_url = "http://localhost:8025"

@_pytest.mark.parametrize("mailpit_api", [api_url], indirect=True)
def test_api(mailpit_api):
    assert len(mailpit_api.get_messages().messages) == 0
"""
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_pytest_helpers_default_api_url(pytester):
    pytester.makeconftest("""pytest_plugins = ["mailpit.testing.pytest"]""")
    pytester.makepyfile(
        """import pytest as _pytest
import os as _os
import pathlib as _pathlib

def test_api(mailpit_api):
    if _pathlib.Path(_os.environ["HOME"]).is_relative_to(_pathlib.Path("/tmp/pytest-of-root")):
        assert mailpit_api.mailpit_url == "http://mailpit:8025"
    else:
        assert mailpit_api.mailpit_url == "http://localhost:8025"
"""
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
