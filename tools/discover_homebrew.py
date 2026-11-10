"""Update BoleNews discovery catalogs from public GitHub releases."""

import datetime as dt
from itertools import zip_longest
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 64
RECENT_DAYS = 180
CATALOGS = {
    "switch1": ("switch-homebrew-discovered", (
        "topic:switch-homebrew", "topic:nintendo-switch-homebrew")),
    "switch2": ("switch2-homebrew-discovered", (
        "topic:switch2-homebrew", "topic:nintendo-switch-2-homebrew",
        '"Switch 2" homebrew in:description')),
    "ps5": ("ps5-homebrew-discovered", ("topic:ps5-homebrew",)),
}
REPO_NAME = re.compile(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+")
ATOM = "{http://www.w3.org/2005/Atom}"


def fetch(url):
    headers = {"User-Agent": "BoleNewsHomebrewDiscovery/1.0"}
    if urllib.parse.urlsplit(url).hostname == "api.github.com":
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            limit = 2 * 1024 * 1024
            body = response.read(limit + 1)
            if len(body) > limit:
                raise ValueError(f"Oversized GitHub response for {url}")
            return body
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def candidates(queries, now):
    recent_repos, popular_repos = {}, {}
    recent = (now - dt.timedelta(days=RECENT_DAYS)).date()
    for query in queries:
        for order, found in (("updated", recent_repos), ("stars", popular_repos)):
            params = urllib.parse.urlencode({
                "q": f"{query} archived:false pushed:>={recent}",
                "sort": order, "order": "desc", "per_page": 30,
            })
            body = fetch(f"https://api.github.com/search/repositories?{params}")
            if body is None:
                raise ValueError("GitHub repository search is unavailable")
            result = json.loads(body)
            if result.get("incomplete_results"):
                raise ValueError("GitHub returned incomplete repository search results")
            for repo in result["items"]:
                if REPO_NAME.fullmatch(repo["full_name"]) and not any(
                        repo.get(key) for key in ("archived", "fork", "private", "disabled")):
                    found[repo["id"]] = repo
    newest = sorted(recent_repos.values(), key=lambda repo: repo["pushed_at"], reverse=True)
    popular = sorted(popular_repos.values(), key=lambda repo: repo["stargazers_count"], reverse=True)
    ranked = {}
    for pair in zip_longest(newest, popular):
        for repo in pair:
            if repo is not None:
                ranked.setdefault(repo["id"], repo)
    return list(ranked.values())


def supports_platform(platform, release):
    assets = [asset["name"].lower() for asset in release.get("assets", [])
              if asset.get("state") == "uploaded" and asset.get("size", 0) > 0]
    if platform == "switch1":
        return any(name.endswith(".nro") for name in assets)
    if platform == "switch2":
        return any(name.endswith(".hbx") for name in assets)
    # Shared PKG/ELF extensions need a PS5-specific marker on the actual asset.
    return any(name.endswith((".pkg", ".elf", ".zip")) and
               re.search(r"ps5|prospero|ppsa[0-9]{5}", name) and
               not re.search(r"source|symbols|sdk", name) for name in assets)


def release_feed(repo, platform):
    name = repo["full_name"]
    body = fetch(f"https://api.github.com/repos/{name}/releases/latest")
    if body is None:
        return None
    release = json.loads(body)
    if (release.get("draft") or release.get("prerelease") or not release.get("published_at")
            or not supports_platform(platform, release)):
        return None
    url = f"https://github.com/{name}/releases.atom"
    atom = fetch(url)
    if atom is None:
        return None
    try:
        feed = ET.fromstring(atom)
    except ET.ParseError:
        return None
    if feed.tag != ATOM + "feed":
        return None
    release_url = release.get("html_url")
    if not release_url or not any(link.get("href") == release_url
                                  for entry in feed.findall(ATOM + "entry")
                                  for link in entry.findall(ATOM + "link")):
        return None
    return url


def known_repo(source):
    if source.get("repo"):
        return source["repo"].lower()
    url = urllib.parse.urlsplit(source.get("url", ""))
    if url.hostname == "github.com":
        return "/".join(url.path.strip("/").split("/")[:2]).lower()
    return ""


def discover(root, now):
    catalogs = root / "catalogs"
    paths = {platform: catalogs / (slug + ".json") for platform, (slug, _) in CATALOGS.items()}
    documents = {path: json.loads(path.read_text(encoding="utf-8"))
                 for path in [root / "sources.json", *sorted(catalogs.glob("*.json"))]}
    # Preserve earlier entries and prefer curated listings when they already exist.
    known = {known_repo(s) for doc in documents.values() for s in doc["sources"]}
    seen_ids = {s["id"] for path in paths.values() for s in documents.get(path, {}).get("sources", [])}
    updates = {}
    for platform, (_, queries) in CATALOGS.items():
        path = paths[platform]
        old = documents.get(path)
        sources = list(old["sources"]) if old else []
        if len(sources) < LIMIT:
            for repo in candidates(queries, now):
                name = repo["full_name"]
                ident = f"gh-homebrew-{repo['id']}"
                if name.lower() in known or ident in seen_ids or name.lower() == "gomprime/switchiptv":
                    continue
                url = release_feed(repo, platform)
                if not url:
                    continue
                sources.append({
                    "id": ident, "name": repo["name"], "url": url, "repo": name,
                    "category": "homebrew", "language": "en", "platforms": [platform],
                    "enabled": False, "images": False, "fullContent": True, "builtin": True,
                    "evidence": "upstream",
                    "rights_policy": "direct upstream release feed; no mirrored binaries or game data",
                })
                known.add(name.lower())
                seen_ids.add(ident)
                if len(sources) == LIMIT:
                    break
        if old is None or sources != old["sources"]:
            updates[path] = {
                "schema_version": 1, "config_version": old["config_version"] + 1 if old else 1,
                "min_app_version": "0.1.4", "generated_at": now.isoformat(), "sources": sources,
            }
        print(f"{platform}: {len(sources)} sources ({len(sources) - len(old['sources']) if old else len(sources)} added)")

    # A transient fetch failure leaves every catalog at its last successful snapshot.
    for path, doc in updates.items():
        temp = path.with_suffix(".part")
        temp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp.replace(path)


if __name__ == "__main__":
    discover(ROOT, dt.datetime.now(dt.timezone.utc))
