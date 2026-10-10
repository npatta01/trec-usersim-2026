"""Synthetic, offline checks for evidence loss and accidental credential copying."""
import json
from pathlib import Path
import tempfile
import unittest

from tools.evidence.archive import archive, scan_for_secrets, verify


class EvidenceArchiveTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "receipt.json").write_text('{"synthetic":true}\n')
        self.dest = self.root / "archive"

    def create(self):
        return archive({"synthetic-run": self.source}, self.dest)

    def test_snapshot_checks_originals_and_hashes(self):
        result = self.create()
        self.assertEqual(result["files"], 1)
        self.assertTrue(result["original_sources_checked"])
        self.assertEqual(verify(self.dest)["manifest_sha256"], result["manifest_sha256"])
        private = json.loads((self.dest / "manifest.json").read_text())
        self.assertIn("sources", private)
        self.assertNotIn("sources", result)
        self.assertEqual((self.dest / "synthetic-run/receipt.json").read_bytes(),
                         (self.source / "receipt.json").read_bytes())

    def test_missing_changed_or_extra_archive_files_fail(self):
        self.create()
        saved = self.dest / "synthetic-run/receipt.json"
        data = saved.read_bytes()
        saved.write_text("changed")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            verify(self.dest)
        saved.write_bytes(data)
        extra = self.dest / "extra.txt"
        extra.write_text("extra")
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify(self.dest)
        extra.unlink()
        saved.unlink()
        with self.assertRaisesRegex(ValueError, "inventory"):
            verify(self.dest)

    def test_sources_can_disappear_after_snapshot_but_changes_are_detected(self):
        self.create()
        (self.source / "receipt.json").write_text("new")
        verify(self.dest)
        with self.assertRaisesRegex(ValueError, "Original source changed"):
            verify(self.dest, check_sources=True)

    def test_existing_and_recursive_destinations_are_refused(self):
        self.create()
        with self.assertRaisesRegex(ValueError, "exists"):
            self.create()
        with self.assertRaisesRegex(ValueError, "inside a source"):
            archive({"synthetic-run": self.source}, self.source / "nested")

    def test_credential_files_caches_and_symlinks_are_excluded(self):
        (self.source / "organizer.key").write_text("synthetic-secret")
        (self.source / ".env").write_text("synthetic-secret")
        cache = self.source / ".venv"
        cache.mkdir()
        (cache / "cached.txt").write_text("cache")
        (self.source / "linked.json").symlink_to(self.source / "receipt.json")
        result = self.create()
        self.assertEqual(result["files"], 1)
        self.assertGreaterEqual(result["excluded_files"], 4)

    def test_credential_content_is_refused_without_echoing_value(self):
        synthetic = "sk-or-v1-" + "x" * 40
        (self.source / "receipt.json").write_text(json.dumps({"Authorization": synthetic}))
        with self.assertRaises(ValueError) as error:
            self.create()
        self.assertNotIn(synthetic, str(error.exception))
        self.assertFalse(self.dest.exists())

    def test_only_opaque_encrypted_reasoning_is_exempt_from_text_scan(self):
        synthetic = "sk-or-v1-" + "x" * 40
        data = {"type": "reasoning.encrypted", "data": synthetic}
        self.assertEqual(scan_for_secrets(json.dumps(data).encode()), 1)
        data["text"] = synthetic
        with self.assertRaises(ValueError):
            scan_for_secrets(json.dumps(data).encode())
        with self.assertRaises(ValueError):
            scan_for_secrets(json.dumps({"type": "reasoning.text", "data": synthetic}).encode())


if __name__ == "__main__":
    unittest.main()
