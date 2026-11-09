import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class TestCLI(unittest.TestCase):
    def run_cli(self, value):
        return subprocess.run(
            [sys.executable, str(ROOT / "app.py"), value],
            capture_output=True, text=True, timeout=10, cwd=ROOT,
        )

    def test_cli_at_threshold(self):
        result = self.run_cli("50000")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "500")
        self.assertEqual(result.stderr, "")

    def test_cli_cap_boundary(self):
        # Teks "500000" diparse menjadi int; 1% = 5.000 tepat di cap, exit status 0.
        result = self.run_cli("500000")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "5000")
        self.assertEqual(result.stderr, "")

    def test_cli_negative(self):
        result = self.run_cli("-1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("integer nonnegatif", result.stderr)

    def test_cli_non_numeric(self):
        result = self.run_cli("abc")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.strip())


if __name__ == "__main__":
    unittest.main()
