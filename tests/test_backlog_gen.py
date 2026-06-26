from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from skillforge.backlog_gen import generate_backlog_entries, load_taxonomy, merge_backlog_entries, load_skill_folder_statuses


class BacklogGenTests(unittest.TestCase):
    def test_generate_backlog_entries_meets_scale_target(self) -> None:
        taxonomy = load_taxonomy(ROOT)
        entries = generate_backlog_entries(taxonomy)
        self.assertGreaterEqual(len(entries), 50)
        ids = [entry["id"] for entry in entries]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("java-spring-boot-service", ids)
        self.assertIn("react-component-engineering", ids)
        self.assertIn("system-architecture-review", ids)

    def test_merge_backlog_entries_syncs_folder_status(self) -> None:
        generated = [{"id": "java-core-engineering", "status": "proposed", "display_name": "X"}]
        existing = [{"id": "java-core-engineering", "status": "draft", "display_name": "X"}]
        merged = merge_backlog_entries(generated, existing, {"java-core-engineering": "active"})
        self.assertEqual(merged[0]["status"], "active")


if __name__ == "__main__":
    unittest.main()
