from __future__ import annotations

import unittest
from pathlib import Path

from skillctl_runner import run_skillctl

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_help_works(self) -> None:
        result = run_skillctl("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Cross-agent skill library tooling", result.stdout)

    def test_list_skills(self) -> None:
        result = run_skillctl("list", "--skills")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("java-core-engineering", result.stdout)


if __name__ == "__main__":
    unittest.main()
