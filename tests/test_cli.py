from __future__ import annotations

import subprocess
import sys
import unittest
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_help_works(self) -> None:
        command = [str(ROOT / "tools" / "skillctl"), "--help"]
        if os.name == "nt":
            command = ["cmd", "/c", str(ROOT / "tools" / "skillctl.cmd"), "--help"]
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Cross-agent skill library tooling", result.stdout)

    def test_list_skills(self) -> None:
        command = [str(ROOT / "tools" / "skillctl"), "list", "--skills"]
        if os.name == "nt":
            command = ["cmd", "/c", str(ROOT / "tools" / "skillctl.cmd"), "list", "--skills"]
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("java-core-engineering", result.stdout)


if __name__ == "__main__":
    unittest.main()
