import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.parse


spec = importlib.util.spec_from_file_location(
    "discovery", Path(__file__).resolve().parents[1] / "tools/discover_homebrew.py")
discovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(discovery)


class DiscoveryTest(unittest.TestCase):
    def test_recent_zero_star_repo_is_considered_with_popular_repos(self):
        recent = {"id": 1, "full_name": "example/recent", "stargazers_count": 0,
                  "pushed_at": "2026-11-10T00:00:00Z"}
        popular = {"id": 2, "full_name": "example/popular", "stargazers_count": 1200,
                   "pushed_at": "2026-11-01T00:00:00Z"}

        def search(url):
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
            self.assertNotIn("stars:", query["q"][0])
            items = [recent, popular] if query["sort"] == ["updated"] else [popular]
            return json.dumps({"items": items}).encode()

        with patch.object(discovery, "fetch", side_effect=search):
            found = discovery.candidates(("topic:switch-homebrew",), dt.datetime(2026, 11, 10))
        self.assertEqual([repo["id"] for repo in found], [1, 2])

    def test_platform_uses_release_artifact(self):
        def release(name):
            return {"assets": [{"name": name, "state": "uploaded", "size": 100}]}

        self.assertTrue(discovery.supports_platform("switch1", release("tool.nro")))
        self.assertFalse(discovery.supports_platform("switch2", release("tool.nro")))
        self.assertTrue(discovery.supports_platform("switch2", release("tool.hbx")))
        self.assertTrue(discovery.supports_platform("ps5", release("PPSA92000.zip")))
        self.assertFalse(discovery.supports_platform("ps5", release("desktop.zip")))

    def test_deduplicates_and_keeps_defaults_and_versions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "catalogs").mkdir()
            (root / "sources.json").write_text(json.dumps({"sources": [
                {"url": "https://github.com/EXAMPLE/Existing/releases.atom"},
            ]}), encoding="utf-8")
            repos = [{"id": 1, "name": "Existing", "full_name": "example/existing"},
                     {"id": 2, "name": "New", "full_name": "example/New"}]
            with patch.object(discovery, "candidates", return_value=repos), patch.object(
                    discovery, "release_feed", return_value="https://github.com/example/New/releases.atom") as check:
                discovery.discover(root, dt.datetime(2026, 11, 10, tzinfo=dt.timezone.utc))
                discovery.discover(root, dt.datetime(2026, 11, 11, tzinfo=dt.timezone.utc))
            check.assert_called_once_with(repos[1], "switch1")
            saved = json.loads((root / "catalogs/switch-homebrew-discovered.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["config_version"], 1)
            self.assertEqual([s["id"] for s in saved["sources"]], ["gh-homebrew-2"])
            self.assertFalse(saved["sources"][0]["enabled"])
            self.assertEqual(saved["sources"][0]["platforms"], ["switch1"])
