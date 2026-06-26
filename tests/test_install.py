from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.install import install_pack


class InstallTests(unittest.TestCase):
    def test_install_java_backend_pack_cursor_active_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"
            dest.mkdir()
            result = install_pack(ROOT, "java-backend-pack", "cursor", dest, active_only=True)
            self.assertIn("java-core-engineering", result.installed)
            self.assertIn("java-21-lts", result.installed)
            self.assertIn("java-25-lts", result.installed)
            self.assertTrue((dest / ".cursor/skills/java-core-engineering/SKILL.md").exists())
            self.assertTrue((dest / ".cursor/rules/java-core-engineering.mdc").exists())
            self.assertEqual(result.skipped_draft, [])

    def test_install_planning_mode_filter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"
            dest.mkdir()
            result = install_pack(
                ROOT,
                "java-backend-pack",
                "cursor",
                dest,
                active_only=True,
                modes={"planning"},
            )
            self.assertIn("java-migrate-any-version", result.installed)
            self.assertIn("java-security-hardening", result.installed)
            self.assertNotIn("java-core-engineering", result.installed)
            self.assertIn("java-core-engineering", result.skipped_modes)

    def test_install_unknown_pack_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "project"
            dest.mkdir()
            with self.assertRaises(ValueError):
                install_pack(ROOT, "missing-pack", "cursor", dest)


if __name__ == "__main__":
    unittest.main()
