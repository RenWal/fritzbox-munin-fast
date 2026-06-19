import os
from unittest.mock import patch
import pytest
from test_response_mock import ResponseMock
from test_fritzconnection_mock import FritzConnectionMock

# @see https://docs.pytest.org/en/7.3.x/example/parametrize.html#indirect-parametrization


@pytest.fixture(autouse=True)
def mock_env_vars():
  """Set required environment variables for all tests."""
  with patch.dict(os.environ, {
    'fritzbox_user': 'testuser',
    'fritzbox_password': 'testpassword'
  }, clear=False):
    yield


@pytest.fixture(autouse=True)
def fixture_version(request):  # request param is fixture
  with patch('requests.request', side_effect=ResponseMock) as mock_requests:
    mock_requests.side_effect.version = request.param if hasattr(request, "param") else None
    yield


@pytest.fixture(autouse=True)
def connection(request):
  return FritzConnectionMock(version=request.param if hasattr(request, "param") else None)
