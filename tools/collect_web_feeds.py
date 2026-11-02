"""Opt-in index metadata adapters for sites without RSS. No scripts or downloads.

Run: python tools/collect_web_feeds.py --site all
Publish the feeds/ directory separately; this command never pushes or deploys.
"""
import argparse
import datetime as dt
import hashlib
import html as html_entities
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

ROOT = Path(__file__).resolve().parents[1]
SITES = {
    "ns45": {"name": "NS45", "url": "https://www.ns45.com/news/",
             "hosts": {"www.ns45.com", "ns45.com"}, "path": r"/news/\d+\.html"},
    "gamer520": {"name": "Gamer520 public WordPress API (Switch category)",
                 "url": "https://vip.gamers520.com/wp-json/wp/v2/posts?categories=2&per_page=20&_fields=id,date_gmt,link,title",
                 "hosts": {"vip.gamers520.com"}, "path": r"/\d+\.html",
                 "format": "wordpress"},
    "a9vg": {"name": "A9VG", "url": "https://www.a9vg.com/",
             "hosts": {"www.a9vg.com"}, "path": r"/article/\d+"},
    "nintendo-tw": {"name": "Nintendo Taiwan", "url": "https://www.nintendo.com/tw/topics",
                    "hosts": {"www.nintendo.com"}, "path": r"/tw/topics/article/[A-Za-z0-9_-]+",
                    "language": "zh-Hant"},
}
AGENT = "BoleNewsMetadata/0.1 (+https://github.com/shellsec/bolenews)"
LIMIT = 2 * 1024 * 1024


def allowed(url, site):
    p = urllib.parse.urlsplit(url)
    return (p.scheme == "https" and p.hostname in site["hosts"] and
            not p.username and not p.password and p.port in (None, 443))


class Redirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, site):
        self.site = site

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl, self.site):
            raise ValueError("Cross-site or non-HTTPS redirect rejected")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, site):
    if not allowed(url, site):
        raise ValueError("URL not allowed for this adapter")
    opener = urllib.request.build_opener(Redirect(site),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    req = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with opener.open(req, timeout=20) as response:
        body = response.read(LIMIT + 1)
        if len(body) > LIMIT:
            raise ValueError("Response exceeds 2 MiB")
        return body.decode(response.headers.get_content_charset() or "utf-8", errors="strict")


class Links(HTMLParser):
    def __init__(self, site):
        super().__init__(convert_charrefs=True)
        self.site, self.link, self.text, self.blocked = site, None, [], 0
        self.items = {}

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.blocked += 1
        if tag == "a" and not self.blocked:
            attrs = dict(attrs)
            url = urllib.parse.urljoin(self.site["url"], attrs.get("href", ""))
            p = urllib.parse.urlsplit(url)
            self.link = (url if allowed(url, self.site) and
                         re.fullmatch(self.site["path"], p.path) and not p.query else None)
            self.text = []

    def handle_data(self, data):
        if self.link and not self.blocked:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.blocked = max(0, self.blocked - 1)
        if tag == "a" and self.link:
            title = " ".join("".join(self.text).split())
            if (4 <= len(title) <= 512 and len(self.items) < 100 and
                    self.link not in self.items and
                    title.lower() not in {"查看详情", "查看详细", "阅读全文", "read more"}):
                self.items[self.link] = {
                    "id": hashlib.sha256(self.link.encode()).hexdigest(),
                    "title": title, "original_url": self.link,
                    "summary": "", "content": "", "image_url": "",
                    "published_at": "", "evidence": "community",
                    "language": self.site.get("language", "zh-Hans"), "content_scope": "metadata",
                }
            self.link = None


def convert(html, site):
    parser = Links(site)
    parser.feed(html)
    return list(parser.items.values())


def convert_wordpress(body, site):
    posts = json.loads(body)
    if not isinstance(posts, list):
        raise ValueError("WordPress posts must be an array")
    items = {}
    for post in posts[:100]:
        try:
            title = post["title"]["rendered"]
            url = post["link"]
            if not isinstance(title, str) or not isinstance(url, str):
                continue
            title = " ".join(html_entities.unescape(re.sub(r"<[^>]*>", " ", title)).split())
            p = urllib.parse.urlsplit(url)
            if (not title or len(title) > 512 or not allowed(url, site) or
                    not re.fullmatch(site["path"], p.path) or p.query or url in items):
                continue
            date = post.get("date_gmt", "")
            try:
                date = dt.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").isoformat() + "Z"
            except (ValueError, TypeError):
                date = ""
            items[url] = {"title": title, "original_url": url, "published_at": date,
                          "summary": "", "content": "", "image_url": "",
                          "content_scope": "metadata", "language": "zh-Hans",
                          "evidence": "community"}
        except (KeyError, TypeError, ValueError):
            continue
    return list(items.values())


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.part")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def collect(key, output):
    site = SITES[key]
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    path = output / (key + ".json")
    health = {"source": key, "attempted_at": now, "status": "unavailable"}
    try:
        robots = urllib.robotparser.RobotFileParser()
        try:
            robots_text = fetch(urllib.parse.urljoin(site["url"], "/robots.txt"), site)
        except urllib.error.HTTPError as error:
            # RFC 9309 2.3.1.3: unavailable robots (4xx) has no rules.
            # Rate limiting, server errors and TLS errors still stop collection.
            if not (400 <= error.code < 500) or error.code == 429:
                raise
            robots_text = "User-agent: *\nAllow: /"
            health["robots_status"] = error.code
        robots.parse(robots_text.splitlines())
        if not robots.can_fetch(AGENT, site["url"]):
            raise ValueError("robots.txt disallows the index")
        body = fetch(site["url"], site)
        items = (convert_wordpress(body, site) if site.get("format") == "wordpress"
                 else convert(body, site))
        if not items:
            raise ValueError("No matching entries; adapter needs review")
        atomic_json(path, {"schema_version": 1, "status": "ok", "generated_at": now,
                           "source_url": site["url"], "items": items})
        health.update(status="ok", count=len(items))
    except Exception as error:
        health["error"] = str(error)[:500]
        # Never replace a successful feed with an error or fabricate current articles.
        if not path.exists():
            atomic_json(path, {"schema_version": 1, "status": "unavailable",
                               "source_url": site["url"], "items": []})
    atomic_json(output / (key + ".health.json"), health)
    return health


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--site", choices=["all", *SITES], required=True)
    cli.add_argument("--output", type=Path, default=ROOT / "feeds")
    args = cli.parse_args()
    keys = SITES if args.site == "all" else [args.site]
    results = [collect(key, args.output) for key in keys]
    print(json.dumps(results, ensure_ascii=True, indent=2))
    raise SystemExit(0 if all(r["status"] == "ok" for r in results) else 1)
