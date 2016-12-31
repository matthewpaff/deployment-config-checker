from copy import deepcopy
from pathlib import Path
import unittest

from deployment_lab.core import validate_deployment
from deployment_lab.fixture_check import check


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.data = {"service": "example", "replicas": 2, "resources": {"cpu_millis": 250, "memory_mb": 128},
                     "health": {"path": "/ready", "interval_seconds": 10, "timeout_seconds": 2, "failure_threshold": 3}}

    def test_totals_and_input_preservation(self):
        original = deepcopy(self.data)
        self.assertEqual(validate_deployment(self.data), {"service": "example", "replicas": 2,
            "total_cpu_millis": 500, "total_memory_mb": 256, "health_path": "/ready", "configured_failure_window_seconds": 30})
        self.assertEqual(self.data, original)

    def test_timeout_must_be_shorter_than_interval(self):
        self.data["health"]["timeout_seconds"] = 10
        with self.assertRaisesRegex(ValueError, "shorter"):
            validate_deployment(self.data)

    def test_aggregate_budget_and_boolean_fields(self):
        self.data["replicas"] = 50
        self.data["resources"]["cpu_millis"] = 16000
        with self.assertRaisesRegex(ValueError, "budget"):
            validate_deployment(self.data)
        self.data["replicas"] = True
        with self.assertRaises(ValueError):
            validate_deployment(self.data)

    def test_unknown_settings_and_nonlocal_probe_shapes(self):
        for path in ("https://example.com", "//remote", "/ready?secret=1", "/ready\n"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.data["health"]["path"] = path
                validate_deployment(self.data)
        self.data["health"]["path"] = "/ready"
        self.data["extra"] = 1
        with self.assertRaises(ValueError):
            validate_deployment(self.data)

    def test_complete_fixture_corpus(self):
        self.assertGreaterEqual(check(Path(__file__).resolve().parents[1] / "fixtures/cases.jsonl", validate_deployment), 350)


if __name__ == "__main__":
    unittest.main()
