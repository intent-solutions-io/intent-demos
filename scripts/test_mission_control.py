#!/usr/bin/env python3
"""Hermetic regression tests for source clocks, truthful output, and atomic recovery."""

import datetime as dt
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import mission_control as mc

NOW = dt.datetime(2026, 9, 17, 20, tzinfo=dt.timezone.utc)


def fixture():
    return {"schema_version": 1, "published_at": mc.stamp(NOW), "max_age_seconds": mc.MAX_AGE,
            "publisher_revision": "b" * 40,
            "source": {"revision": "a" * 40, "observed_at": mc.stamp(NOW), "commit_at": mc.stamp(NOW),
                       "fetch_status": "ok", "components": [{"name": "Founder view", "state": "present"}]},
            "services": [{"name": "Tons of Skills", "url": "https://tonsofskills.com/healthz", "state": "reachable", "observed_at": mc.stamp(NOW)}], "reports": []}


class SnapshotTests(unittest.TestCase):
    def test_july_snapshot_is_stale_despite_http_200(self):
        data = fixture()
        data["published_at"] = "2026-07-11T15:49:17Z"
        self.assertIn("publication timestamp stale or invalid", mc.freshness_errors(data, NOW))

    def test_missing_future_and_naive_clocks_refused(self):
        for value in [None, "tomorrow", "2026-09-17T20:10:00Z", "2026-09-17T20:00:00"]:
            with self.subTest(value=value):
                data = fixture()
                data["source"]["observed_at"] = value
                self.assertTrue(mc.freshness_errors(data, NOW))

    def test_success_and_exact_freshness_boundary(self):
        self.assertEqual(mc.freshness_errors(fixture(), NOW), [])
        self.assertEqual(mc.freshness_errors(fixture(), NOW + dt.timedelta(seconds=mc.MAX_AGE)), [])
        self.assertTrue(mc.freshness_errors(fixture(), NOW + dt.timedelta(seconds=mc.MAX_AGE + 1)))

    def test_schema_and_revision_required(self):
        data = fixture()
        data.pop("schema_version")
        data["source"]["revision"] = None
        self.assertEqual(len(mc.freshness_errors(data, NOW)), 2)

    def test_legacy_and_malformed_manifest_fail_closed_without_crash(self):
        for data in [{"generated": "2026-07-11"}, [], {"source": []}, {"source": {"revision": 23}}]:
            with self.subTest(data=data):
                self.assertTrue(mc.freshness_errors(data, NOW))

    def test_failed_source_fetch_keeps_last_good_clock(self):
        previous = fixture()
        with patch.object(mc, "git", side_effect=OSError("simulated private transport failure")):
            source = mc.source_snapshot(Path("/unused"), NOW + dt.timedelta(hours=1), previous, fetch=False)
        self.assertEqual(source["observed_at"], previous["source"]["observed_at"])
        self.assertEqual(source["revision"], previous["source"]["revision"])
        self.assertEqual(source["fetch_status"], "unavailable")
        self.assertNotIn("private transport", json.dumps(source))

    def test_invalid_prior_source_cache_does_not_crash_recovery(self):
        for prior in [{"source": []}, [], {"source": None}]:
            with patch.object(mc, "git", side_effect=OSError("fixture failure")):
                source = mc.source_snapshot(Path("/unused"), NOW, prior, fetch=False)
            self.assertIsNone(source["observed_at"])
            self.assertEqual(source["fetch_status"], "unavailable")

    def test_outage_with_corrupt_nested_cache_is_safe_and_allowlisted(self):
        for rows in [None, 23, [{"name": "PRIVATE-MARKER", "state": "present"},
                               {"name": "Founder view", "state": "corrupt"}], [{}]]:
            prior = {"source": {"revision": [], "observed_at": [], "commit_at": "invalid", "components": rows}}
            with patch.object(mc, "git", side_effect=OSError("fixture outage")):
                result = mc.source_snapshot(Path("/unused"), NOW, prior, fetch=False)
            self.assertIsNone(result["revision"])
            self.assertIsNone(result["observed_at"])
            self.assertEqual(result["components"], [])
            self.assertNotIn("PRIVATE-MARKER", json.dumps(result))
            data = fixture(); data["source"] = result
            self.assertIn("unavailable", mc.current_report(data))

    def test_private_document_text_never_read_or_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            (repo / "private.md").write_text("PRIVATE-MARKER-DO-NOT-PUBLISH")
            path = repo / mc.COMPONENTS["Founder view"]
            path.parent.mkdir(parents=True)
            path.write_text("implementation")
            subprocess.run(["git", "-C", tmp, "add", "."], check=True)
            subprocess.run(["git", "-C", tmp, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "fixture"], check=True, capture_output=True)
            source = mc.source_snapshot(repo, NOW, {}, fetch=False)
            self.assertEqual(source["fetch_status"], "ok")
            self.assertEqual(next(c for c in source["components"] if c["name"] == "Founder view")["state"], "present")
            self.assertNotIn("PRIVATE-MARKER", json.dumps(source))
            self.assertNotIn("private.md", json.dumps(source))

    def test_build_current_copy_archive_and_machine_output_agree(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            data = fixture()
            mc.build_release(out, data)
            page = (out / "index.html").read_text()
            self.assertNotIn("{{", page)
            self.assertIn("historical", page)
            self.assertIn("current.md", page)
            self.assertIn(data["source"]["revision"], page)
            self.assertEqual(len(data["reports"]), 11)
            self.assertEqual(json.loads((out / "manifest.json").read_text()), data)
            self.assertIn("Implementation is under way", (out / "current.md").read_text())
            self.assertIn("Historical report:", (out / "all-reports.md").read_text())
            self.assertNotIn("current-state digest", page)

    def test_probe_http_200_wrong_body_not_green(self):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.read.return_value = b'{"ok":false,"service":"tonsofskills.com"}'
        with patch.object(mc.urllib.request, "urlopen", return_value=response):
            result = mc.probe("Tons of Skills", "https://example.invalid", "tonsofskills.com", NOW)
        self.assertEqual(result["state"], "unavailable")
        response.read.return_value = b'[]'
        with patch.object(mc.urllib.request, "urlopen", return_value=response):
            self.assertEqual(mc.probe("Tons of Skills", "https://example.invalid", "tonsofskills.com", NOW)["state"], "unavailable")

    def test_probe_timeout_and_bad_json_are_visible(self):
        with patch.object(mc.urllib.request, "urlopen", side_effect=TimeoutError("secret path must not escape")):
            result = mc.probe("Tons of Skills", "https://example.invalid", "tonsofskills.com", NOW)
        self.assertEqual(result["error_category"], "network")
        self.assertNotIn("secret path", json.dumps(result))

    @patch.object(mc, "probe", return_value=fixture()["services"][0])
    @patch.object(mc, "source_snapshot", return_value=fixture()["source"])
    def test_migrate_republish_restart_and_abandoned_candidate(self, source, probe):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            deploy, state = base / "served/mission-control", base / "private-state"
            deploy.mkdir(parents=True)
            (deploy / "index.html").write_text("old July page")
            mc.publish(deploy, state, base / "repo")
            first = deploy.resolve()
            self.assertTrue(deploy.is_symlink())
            self.assertEqual((state / "legacy-feed/index.html").read_text(), "old July page")
            (deploy.parent / ".mission-control.next").symlink_to(first)
            mc.publish(deploy, state, base / "repo")
            self.assertNotEqual(deploy.resolve(), first)
            self.assertTrue(first.is_dir())
            self.assertEqual(len(list((deploy / "reports").glob("*.md"))), 11)

    @patch.object(mc, "probe", return_value=fixture()["services"][0])
    @patch.object(mc, "source_snapshot", return_value=fixture()["source"])
    def test_failed_build_preserves_served_snapshot(self, source, probe):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            deploy, state = base / "served", base / "state"
            mc.publish(deploy, state, base / "repo")
            original = deploy.resolve()
            with patch.object(mc, "build_release", side_effect=ValueError("fixture invalid")):
                with self.assertRaises(ValueError):
                    mc.publish(deploy, state, base / "repo")
            self.assertEqual(deploy.resolve(), original)


if __name__ == "__main__":
    unittest.main()
