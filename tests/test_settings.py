import os
from unittest.mock import patch

from fast_api_zero.settings import Settings


def test_settings_should_load_from_env():
    with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///test.db'}):
        settings = Settings()
        assert settings.DATABASE_URL == 'sqlite:///test.db'


def test_settings_invalid_url_type():
    with patch.dict(
        os.environ, {'DATABASE_URL': 'postgres://user:pass@localhost/db'}
    ):
        settings = Settings()
        assert 'postgres' in settings.DATABASE_URL
