import importlib
import os
import unittest
from unittest.mock import patch

import settings


class SettingsTests(unittest.TestCase):
    def test_is_truthy_accepts_expected_values(self) -> None:
        for value in ["1", "true", "TRUE", " yes ", "on"]:
            with self.subTest(value=value):
                self.assertTrue(settings.is_truthy(value))

    def test_is_truthy_rejects_other_values(self) -> None:
        for value in ["0", "false", "off", "", "nope", None]:
            with self.subTest(value=value):
                self.assertFalse(settings.is_truthy(value))

    def test_reload_reads_env_values(self) -> None:
        env = {
            "DEBUG": "yes",
            "VERIFY_SSL": "false",
            "REQUEST_TIMEOUT_SECONDS": "25",
            "GROQ_MODEL": "test-model",
        }

        with patch.dict(os.environ, env, clear=False):
            module = importlib.reload(settings)

        self.assertTrue(module.DEBUG)
        self.assertFalse(module.VERIFY_SSL)
        self.assertEqual(module.REQUEST_TIMEOUT_SECONDS, 25)
        self.assertEqual(module.GROQ_MODEL, "test-model")

        importlib.reload(settings)

    def test_disable_warnings_called_when_ssl_verification_off(self) -> None:
        with patch.dict(os.environ, {"VERIFY_SSL": "false"}, clear=False):
            with patch("urllib3.disable_warnings") as mock_disable_warnings:
                importlib.reload(settings)
                mock_disable_warnings.assert_called_once()

        importlib.reload(settings)


if __name__ == "__main__":
    unittest.main()
