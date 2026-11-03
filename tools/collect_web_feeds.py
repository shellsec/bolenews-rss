"""Opt-in index metadata adapters for sites without RSS. No scripts or downloads.

Run: python tools/collect_web_feeds.py --site all
Publish the feeds/ directory separately; this command never pushes or deploys.
"""
import argparse
import datetime as dt
import email.utils
import hashlib
import html as html_entities
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITES = {
    "2468c": {"name": "奥德彪计划 PS4 / PS5", "format": "wordpress",
              "url": "https://2468c.com/wp-json/wp/v2/posts?categories=53,65,111,112,141,146,147&per_page=100&_fields=id,date_gmt,modified_gmt,link,title,categories",
              "hosts": {"2468c.com"}, "path": r"/\d+\.html",
              "platform_categories": {"ps4": {53, 112}, "ps5": {65, 111, 141, 146, 147}},
              "tool_categories": {111, 112}},
    "gnn": {"name": "巴哈姆特 GNN", "url": "https://gnn.gamer.com.tw/rss.xml",
            "hosts": {"gnn.gamer.com.tw"}, "path": r"/detail\.php",
            "format": "rss", "language": "zh-Hant"},
    "ns45": {"name": "NS45", "url": "https://www.ns45.com/news/",
             "hosts": {"www.ns45.com", "ns45.com"}, "path": r"/news/\d+\.html"},
    "gamer520": {"name": "Gamer520 public WordPress API (Switch category)",
                 "url": "https://vip.gamers520.com/wp-json/wp/v2/posts?categories=2&per_page=100&_fields=id,date_gmt,modified_gmt,link,title,categories",
                 "hosts": {"vip.gamers520.com"}, "path": r"/\d+\.html",
                 "format": "wordpress", "platforms": ["switch1"]},
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
    return [metadata_tags(item) for item in parser.items.values()]


def metadata_tags(item):
    """Explicit title signals only: an edited post is not proof of a game patch."""
    title = item["title"].lower()
    tags = []
    if re.search(r"固件|韌體|系统更新|系統更新|firmware|system update", title):
        tags.append("firmware_update")
    elif re.search(r"升补|升補|升级补丁|升級補丁|更新补丁|更新補丁|版本更新|更新日志|更新日誌|补丁|補丁|(?<![a-z])dlc(?![a-z])|\bhotfix\b|patch notes|title update|\bupdate\b", title):
        tags.append("game_update")
    if re.search(r"传闻|傳聞|据传|據傳|rumou?r", title):
        item["evidence"] = "rumor"
    elif re.search(r"实验|實驗|proof of concept|experimental", title):
        item["evidence"] = "experimental"
    if tags and item.get("category") != "homebrew":
        item["tags"] = tags
    version = re.search(r"(?:\bv\d+(?:[.][a-z0-9]+)+|\b\d+(?:[.][a-z0-9]+)+(?=\s*(?:升补|升補|补丁|補丁)))", title)
    if version:
        item["version"] = version.group(0)
    return item


def wp_date(value):
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").isoformat() + "Z"
    except (ValueError, TypeError):
        return ""


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
            date = wp_date(post.get("date_gmt", ""))
            modified = wp_date(post.get("modified_gmt", ""))
            item = {"title": title, "original_url": url, "published_at": date,
                          "summary": "", "content": "", "image_url": "",
                          "content_scope": "metadata", "language": "zh-Hans",
                          "evidence": "community"}
            if modified and (not date or modified >= date):
                item["updated_at"] = modified
            if site.get("platforms"):
                item["platform"] = site["platforms"]
            if site.get("platform_categories"):
                categories = post.get("categories", [])
                if not isinstance(categories, list) or any(type(value) is not int for value in categories):
                    continue
                categories = set(categories)
                platforms = [name for name, ids in site["platform_categories"].items() if categories & ids]
                if not platforms:
                    continue
                item["platform"] = platforms
                item["category"] = "homebrew" if categories & site.get("tool_categories", set()) else "hot"
                item["source_name"] = site["name"]
            items[url] = metadata_tags(item)
        except (KeyError, TypeError, ValueError):
            continue
    return list(items.values())


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.part")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def convert_rss(body, site):
    """Publish only attributed title/link/date metadata, never RSS bodies/images."""
    if "<!DOCTYPE" in body.upper() or "<!ENTITY" in body.upper():
        raise ValueError("DTD/entity declarations are not allowed")
    root = ET.fromstring(body)
    if root.tag != "rss":
        raise ValueError("Expected RSS")
    items = {}
    for entry in root.findall("./channel/item")[:100]:
        title = " ".join(html_entities.unescape(re.sub(r"<[^>]*>", " ", entry.findtext("title", ""))).split())
        url = entry.findtext("link", "").strip()
        p = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(p.query)
        if (not 4 <= len(title) <= 512 or not allowed(url, site) or
                not re.fullmatch(site["path"], p.path) or p.fragment or
                set(query) != {"sn"} or len(query["sn"]) != 1 or
                not query["sn"][0].isdigit() or url in items):
            continue
        date = ""
        try:
            parsed = email.utils.parsedate_to_datetime(entry.findtext("pubDate", ""))
            if parsed.tzinfo is not None:
                date = parsed.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
        except (ValueError, TypeError, OverflowError):
            pass
        items[url] = {"title": title, "original_url": url, "published_at": date,
                      "source_name": site["name"], "language": site["language"],
                      "summary": "", "content": "", "image_url": "",
                      "content_scope": "metadata", "evidence": "community"}
    return [metadata_tags(item) for item in items.values()]


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
        urls = [site["url"]]
        if site.get("format") == "wordpress":
            urls.append(site["url"] + "&orderby=modified&order=desc")
        converter = {"wordpress": convert_wordpress, "rss": convert_rss}.get(site.get("format"), convert)
        incoming, failures = {}, []
        for index, url in enumerate(urls):
            if not robots.can_fetch(AGENT, url):
                failures.append("robots.txt disallows an index query")
                continue
            if index:
                time.sleep(1)
            try:
                converted = converter(fetch(url, site), site)
                if not converted:
                    raise ValueError("No matching entries; adapter needs review")
                for item in converted:
                    old = incoming.get(item["original_url"])
                    if old is None or item.get("updated_at", item["published_at"]) >= old.get("updated_at", old["published_at"]):
                        incoming[item["original_url"]] = item
            except Exception as error:
                failures.append(str(error)[:300])
                if isinstance(error, urllib.error.HTTPError) and error.code == 429:
                    break
        if not incoming:
            raise ValueError("; ".join(failures) or "No matching entries")
        # Retain bounded last-good entries when a short upstream window drops them.
        previous = {}
        if path.exists():
            try:
                cached = json.loads(path.read_text(encoding="utf-8"))
                if cached.get("status") == "ok":
                    previous = {x["original_url"]: x for x in cached["items"] if allowed(x["original_url"], site)}
            except (ValueError, KeyError, TypeError):
                pass
        previous.update(incoming)
        items = [metadata_tags(item) for item in previous.values()]
        # Dated updates lead; undated index entries retain upstream order, not fake times.
        items.sort(key=lambda x: max(x.get("updated_at", ""), x.get("published_at", "")), reverse=True)
        total = len(items)
        items = items[:100]  # All supported clients accept at most 100 items per feed.
        atomic_json(path, {"schema_version": 1, "status": "ok", "generated_at": now,
                           "source_url": site["url"], "items": items})
        health.update(status="partial" if failures else "ok", count=len(items),
                      fetched_count=len(incoming), retained_count=sum(x["original_url"] not in incoming for x in items),
                      input_urls=urls, dropped_by_limit=max(0, total - 100))
        if failures:
            health["error"] = "; ".join(failures)
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
