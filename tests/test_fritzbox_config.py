import os
import pytest
from unittest.mock import patch

from fritzbox_config import FritzboxConfig


class TestFritzboxConfigValidation:
    def test_valid_credentials(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass'
        }):
            config = FritzboxConfig()
            assert config.user == 'testuser'
            assert config.password == 'testpass'

    def test_missing_user_raises_error(self):
        with patch.dict(os.environ, {
            'fritzbox_password': 'testpass'
        }, clear=True):
            with pytest.raises(ValueError, match="fritzbox_user environment variable must be set"):
                FritzboxConfig()

    def test_missing_password_raises_error(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser'
        }, clear=True):
            with pytest.raises(ValueError, match="fritzbox_password environment variable must be set"):
                FritzboxConfig()

    def test_user_literal_none_raises_error(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'None',
            'fritzbox_password': 'testpass'
        }):
            with pytest.raises(ValueError, match="fritzbox_user environment variable must be set"):
                FritzboxConfig()

    def test_password_literal_none_raises_error(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'None'
        }):
            with pytest.raises(ValueError, match="fritzbox_password environment variable must be set"):
                FritzboxConfig()

    def test_empty_string_credentials_allowed(self):
        with patch.dict(os.environ, {
            'fritzbox_user': '',
            'fritzbox_password': ''
        }):
            config = FritzboxConfig()
            assert config.user == ''
            assert config.password == ''

    def test_defaults(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass'
        }, clear=True):
            config = FritzboxConfig()
            assert config.server == 'fritz.box'
            assert config.port is None
            assert config.use_tls is True
            assert config.certificate_file is False
            assert config.timeout == 60

    def test_custom_ip(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass',
            'fritzbox_ip': '192.168.1.1'
        }):
            config = FritzboxConfig()
            assert config.server == '192.168.1.1'

    def test_custom_port(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass',
            'fritzbox_port': '8080'
        }):
            config = FritzboxConfig()
            assert config.port == 8080

    def test_tls_disabled(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass',
            'fritzbox_use_tls': 'false'
        }):
            config = FritzboxConfig()
            assert config.use_tls is False

    def test_tls_enabled(self):
        with patch.dict(os.environ, {
            'fritzbox_user': 'testuser',
            'fritzbox_password': 'testpass',
            'fritzbox_use_tls': 'true'
        }):
            config = FritzboxConfig()
            assert config.use_tls is True
