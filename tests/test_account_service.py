"""Cached services must follow the currently loaded account implementation."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from accounts import Accounts
from account_ui import account_service


class ServiceCacheTests(unittest.TestCase):
    """Verify cached account services refresh when their implementation is reloaded."""
    def test_reloaded_implementation_does_not_reuse_stale_service(self):
        """Verifies reloaded implementation does not reuse stale service."""
        with tempfile.TemporaryDirectory() as temporary:
            url = "sqlite:///" + (Path(temporary) / "cache.db").as_posix()
            original = account_service(url, False)
            class ReloadedAccounts(Accounts):
                """Stand in for a newly loaded account-service implementation."""
                pass
            try:
                with patch("account_ui.Accounts", ReloadedAccounts):
                    refreshed = account_service(url, False)
                    try:
                        self.assertIsNot(original, refreshed)
                        self.assertIsInstance(refreshed, ReloadedAccounts)
                    finally:
                        refreshed.engine.dispose()
            finally:
                original.engine.dispose()
                account_service.clear()
