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
              "url": "https://2468c.com/wp-json/wp/v2/posts?categories=53,65,111,112,141,146,147&per_page=100&_fields=id,date_gmt,modified_gmt,link,title,categories,excerpt",
              "hosts": {"2468c.com"}, "path": r"/\d+\.html",
              "platform_categories": {"ps4": {53, 112}, "ps5": {65, 111, 141, 146, 147}},
              "tool_categories": {111, 112}},
    "gnn": {"name": "巴哈姆特 GNN", "url": "https://gnn.gamer.com.tw/rss.xml",
            "hosts": {"gnn.gamer.com.tw"}, "path": r"/detail\.php",
            "format": "rss", "language": "zh-Hant", "numeric_query": "sn"},
    "4gamers-game-guides": {
        "name": "4Gamers 中文遊戲攻略", "url": "https://www.4gamers.com.tw/rss/latest-news",
        "hosts": {"www.4gamers.com.tw"}, "path": r"/news/detail/\d+/[a-z0-9-]+",
        "format": "rss", "language": "zh-Hant",
        "illustrated_guide_title": r"攻略|全收集|隱藏要素|任務流程|圖鑑|解謎",
    },
    "gamer520": {"name": "Gamer520 public WordPress API (Switch category)",
                 "url": "https://vip.gamers520.com/wp-json/wp/v2/posts?categories=2&per_page=100&_fields=id,date_gmt,modified_gmt,link,title,categories,excerpt",
                 "hosts": {"vip.gamers520.com"}, "path": r"/\d+\.html",
                 "format": "wordpress", "platforms": ["switch1"]},
    "gamer520-switch2": {"name": "Gamer520 Switch 2",
                 "url": "https://vip.gamers520.com/wp-json/wp/v2/posts?categories=1493&per_page=100&_fields=id,date_gmt,modified_gmt,link,title,categories,excerpt",
                 "hosts": {"vip.gamers520.com"}, "path": r"/\d+\.html",
                 "format": "wordpress", "platforms": ["switch2"]},
    "gamesradar-calendar": {"name": "GamesRadar 全平台发售表",
                 "url": "https://www.gamesradar.com/video-game-release-dates/",
                 "hosts": {"www.gamesradar.com"}, "path": r"/video-game-release-dates/",
                 "format": "calendar", "max_bytes": 4 * 1024 * 1024},
    "a9vg": {"name": "A9VG", "url": "https://www.a9vg.com/",
             "hosts": {"www.a9vg.com"}, "path": r"/article/\d+"},
    "nintendo-tw": {"name": "Nintendo Taiwan", "url": "https://www.nintendo.com/tw/topics",
                    "hosts": {"www.nintendo.com"}, "path": r"/tw/topics/article/[A-Za-z0-9_-]+",
                    "language": "zh-Hant"},
}
for _platform, _route in (("switch", "/"), ("pc", "/pc"), ("ps4", "/ps4")):
    SITES["nsthwj-" + _platform] = {
        "name": "NS头号玩家 " + _platform.upper(), "url": "https://nsthwj.cn" + _route,
        "hosts": {"nsthwj.cn"}, "path": r"/game/" + _platform + r"/[0-9]+",
        "format": "nsthwj", "platform": _platform,
    }

MUSHROOM_HOST = "www.xn--ogtt23ghrb.cn"
MUSHROOM_DETAIL_PATH = r"/SEO/%E6%B8%B8%E6%88%8F/\d+\.html"
RESOURCE_SCAN_LIMIT = 20
for key, category, platform in (("switch", "Switch", "switch1"), ("pc", "PC游戏", "pc"), ("ps4", "PS4", "ps4")):
    path = urllib.parse.quote(f"/SEO/分类/{category}.html")
    SITES[f"mushroom-{key}"] = {
        "name": f"蘑菇屋 · {category}", "url": f"https://{MUSHROOM_HOST}{path}",
        "hosts": {MUSHROOM_HOST}, "path": MUSHROOM_DETAIL_PATH, "format": "mushroom",
        "platform": platform, "site_category": category,
    }

SITES["ccplay-android"] = {
    "name": "虫虫助手 · Android", "url": "https://g.ccplay.cc/",
    "hosts": {"g.ccplay.cc"}, "path": r"/package/\d+\.html",
    "format": "ccplay", "platform": "android",
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
        limit = site.get("max_bytes", LIMIT)
        body = response.read(limit + 1)
        if len(body) > limit:
            raise ValueError("Response exceeds configured byte limit")
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


class BootstrapData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active, self.parts = False, []
    def handle_starttag(self, tag, attrs):
        if tag == "script" and dict(attrs).get("id") == "thwj-seo-bootstrap":
            self.active = True
    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False
    def handle_data(self, text):
        if self.active:
            self.parts.append(text)


def nsthwj_download_links(url, version, update_date):
    """Only explicitly verified public share links for this exact game version/date."""
    try:
        path = ROOT / "resources/nsthwj-download-links.json"
        if path.is_symlink() or path.stat().st_size > 256 * 1024:
            return []
        config = json.loads(path.read_text(encoding="utf-8"))
        if config.get("schema_version") != 1:
            return []
        entry = config.get("entries", {}).get(url, {})
        version = " ".join(html_entities.unescape(re.sub(r"<[^>]*>", " ", version)).split())[:80]
        if entry.get("version") != version or entry.get("update_date") != update_date:
            return []
        links = []
        for link in entry.get("links", [])[:4]:
            target = link.get("url", "")
            parsed = urllib.parse.urlsplit(target)
            if (len(target) <= 1024 and parsed.scheme == "https" and parsed.hostname in {"pan.baidu.com", "pan.quark.cn", "pan.xunlei.com"}
                    and not parsed.username and not parsed.password and parsed.port in (None,443) and parsed.path.startswith("/s/")):
                links.append({"provider": {"pan.baidu.com":"百度网盘","pan.quark.cn":"夸克网盘","pan.xunlei.com":"迅雷网盘"}[parsed.hostname],
                    "url": target, "extraction_code": str(link.get("extraction_code", ""))[:64]})
        return links
    except (OSError, ValueError, TypeError, KeyError):
        return []


def convert_nsthwj(body, site):
    parser = BootstrapData()
    parser.feed(body)
    data = json.loads("".join(parser.parts))
    if not isinstance(data, dict) or not isinstance(data.get("games"), list):
        raise ValueError("Missing public game index bootstrap")
    rows = {}
    for game in data["games"][:100]:
        if not isinstance(game, dict) or game.get("gameType") != site["platform"]:
            continue
        ident, name = str(game.get("id", "")), game.get("name")
        if not ident.isdigit() or len(ident) > 12 or not isinstance(name, str) or not 1 <= len(name) <= 512:
            continue
        url = "https://nsthwj.cn/game/" + site["platform"] + "/" + ident
        if url in rows:
            continue
        item = {"id": hashlib.sha256(url.encode()).hexdigest(), "title": name,
                "original_url": url, "source_name": site["name"], "summary": clean_excerpt(game.get("summary", "")),
                "summary_origin": "publisher_game_index", "content": "", "image_url": "", "published_at": "",
                "content_scope": "summary", "language": "zh-Hans", "evidence": "community",
                "platform": ["switch1" if site["platform"] == "switch" else site["platform"]],
                "category": "discovery", "download_status": "not_verified"}
        version = game.get("version", "")
        if isinstance(version, str):
            item["version"] = " ".join(html_entities.unescape(re.sub(r"<[^>]*>", " ", version)).split())[:80]
        date = game.get("updateTime", "")
        if isinstance(date, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
            try:
                stamp = dt.datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=dt.timezone(dt.timedelta(hours=8)))
                # Preserve date precision and mark as an index update, never a release date.
                item["updated_at"] = stamp.isoformat()
                item["update_date_precision"] = "day"
            except ValueError:
                pass
        links = nsthwj_download_links(url, version, date)
        if links:
            item["download_links"] = links
            item["download_status"] = "public_browser_verified"
        rows[url] = metadata_tags(item)
    return list(rows.values())


def combine_nsthwj(output):
    limit = 100
    platforms = ("switch", "pc", "ps4")
    items, reserved, generated = {}, {}, []
    def updated(item):
        return item.get("updated_at", "")
    for platform in platforms:
        path = output / ("nsthwj-" + platform + ".json")
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") != "ok":
            continue
        generated.append(data.get("generated_at", ""))
        platform_items = sorted(data.get("items", []), key=updated, reverse=True)[:limit]
        items.update((item["original_url"], item) for item in platform_items)
        for item in platform_items[:limit // len(platforms)]:
            reserved[item["original_url"]] = item
    if items:
        # Fill unused platform slots with the newest remaining entries.
        remaining = (item for url, item in items.items() if url not in reserved)
        extras = sorted(remaining, key=updated, reverse=True)[:limit - len(reserved)]
        ordered = sorted([*reserved.values(), *extras], key=updated, reverse=True)
        atomic_json(output / "nsthwj.json", {"schema_version": 1, "status": "ok",
            "generated_at": max(generated), "source_url": "https://nsthwj.cn/", "items": ordered})


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


class ExcerptText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.blocked = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.blocked += 1
        elif tag in ("p", "br", "div", "li") and not self.blocked:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.blocked = max(0, self.blocked - 1)
        elif tag in ("p", "div", "li") and not self.blocked:
            self.parts.append(" ")

    def handle_data(self, text):
        if not self.blocked:
            self.parts.append(text)


def clean_excerpt(value):
    if not isinstance(value, str):
        return ""
    parser = ExcerptText()
    parser.feed(value[:65536])
    text = " ".join("".join(parser.parts).split())
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\[\s*(?:…|\.\.\.)\s*\]", "…", text).strip()
    if len(text.strip(".… ")) < 8:
        return ""
    return text[:240].rstrip() + ("…" if len(text) > 240 else "")


class DescriptionMeta(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.description, self.og_description = "", ""

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attrs = dict(attrs)
        key = attrs.get("property", attrs.get("name", "")).lower()
        if key == "description":
            self.description = clean_excerpt(attrs.get("content", ""))
        elif key == "og:description":
            self.og_description = clean_excerpt(attrs.get("content", ""))


def fill_descriptions(items, previous, site, robots, limit):
    pending, attempts, failures = [], 0, []
    for item in items:
        old = previous.get(item["original_url"], {})
        unchanged = (old.get("title") == item["title"] and old.get("updated_at", "") == item.get("updated_at", ""))
        if not item.get("summary") and unchanged:
            for field in ("summary", "summary_origin", "summary_checked_at"):
                if old.get(field):
                    item[field] = old[field]
        if not item.get("summary"):
            pending.append(item)
    pending.sort(key=lambda item: item.get("summary_checked_at", ""))
    for item in pending[:limit]:
        if not robots.can_fetch(AGENT, item["original_url"]):
            continue
        if attempts:
            time.sleep(0.3)
        attempts += 1
        item["summary_checked_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            parser = DescriptionMeta()
            parser.feed(fetch(item["original_url"], site))
            text = parser.og_description or parser.description
            if text and text != item["title"]:
                item.update(summary=text, summary_origin="publisher_description", content_scope="summary")
        except Exception as error:
            failures.append(str(error)[:160])
            if isinstance(error, urllib.error.HTTPError) and error.code in (401, 403, 429):
                break
    return {"summary_count": sum(bool(x.get("summary")) for x in items),
            "summary_attempts": attempts, "summary_missing": sum(not x.get("summary") for x in items),
            "summary_errors": failures[:5]}


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
            excerpt = post.get("excerpt", {})
            if isinstance(excerpt, dict) and not excerpt.get("protected", False):
                summary = clean_excerpt(excerpt.get("rendered", ""))
                if summary:
                    item.update(summary=summary, summary_origin="publisher_excerpt", content_scope="summary")
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
    if root.tag != "rss" or root.find("channel") is None:
        raise ValueError("Expected RSS channel")
    items = {}
    for entry in root.findall("./channel/item")[:100]:
        title = " ".join(html_entities.unescape(re.sub(r"<[^>]*>", " ", entry.findtext("title", ""))).split())
        url = entry.findtext("link", "").strip()
        p = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(p.query)
        query_key = site.get("numeric_query")
        valid_query = (set(query) == {query_key} and len(query[query_key]) == 1
                       and query[query_key][0].isdigit()) if query_key else not p.query
        if (not 4 <= len(title) <= 512 or not allowed(url, site) or
                not re.fullmatch(site["path"], p.path) or p.fragment or not valid_query or url in items):
            continue
        guide_title = site.get("illustrated_guide_title")
        if guide_title:
            if not re.search(guide_title, title):
                continue
            html = entry.findtext("{http://purl.org/rss/1.0/modules/content/}encoded", "")
            if not 1 <= len(re.findall(r"<img\b", html, re.I)) <= 32 or len(clean_excerpt(html)) < 100:
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
        summary = clean_excerpt(entry.findtext("description", ""))
        if summary:
            items[url].update(summary=summary, summary_origin="publisher_feed_excerpt", content_scope="summary")
    return [metadata_tags(item) for item in items.values()]


class ReleaseCalendar(HTMLParser):
    """Read the publisher's dated game lists, excluding editorial prose and widgets."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.heading = None
        self.section = None
        self.sections = []
        self.line = None
        self.line_has_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            if attrs.get("id") == "article-body":
                self.depth = 1
            elif self.depth:
                self.depth += 1
        if not self.depth:
            return
        if tag == "h3":
            self.section = None
            anchor = attrs.get("id", "")
            if re.fullmatch(r"section-[a-z0-9-]+", anchor):
                self.heading = {"anchor": anchor, "title": [], "games": [], "image": ""}
        if tag == "li" and self.section is not None:
            self.line = []
            self.line_has_title = False
        if tag == "strong" and self.line is not None:
            self.line_has_title = True
        if tag == "img" and self.section is not None and not self.section["image"]:
            image = attrs.get("src", "")
            if urllib.parse.urlsplit(image).hostname == "cdn.mos.cms.futurecdn.net" and image.startswith("https://"):
                self.section["image"] = image

    def handle_data(self, text):
        if self.depth and self.heading is not None:
            self.heading["title"].append(text)
        if self.depth and self.line is not None:
            self.line.append(text)

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "h3" and self.heading is not None:
            self.heading["title"] = " ".join("".join(self.heading["title"]).split())
            self.section = self.heading
            self.sections.append(self.section)
            self.heading = None
        if tag == "li" and self.line is not None:
            line = " ".join("".join(self.line).split())
            # Keep explicitly unknown platforms such as (TBC) as well.
            if self.section is not None and self.line_has_title and re.search(r"\([^)]*\)", line):
                self.section["games"].append(line)
            self.line = None
        if tag == "div":
            self.depth -= 1


def convert_calendar(body, site):
    parser = ReleaseCalendar()
    parser.feed(body)
    items = []
    for section in parser.sections:
        games = list(dict.fromkeys(section["games"]))
        if not games:
            continue
        title = "GamesRadar · " + section["title"]
        content = "<h2>" + html_entities.escape(title) + "</h2>"
        content += "<p>发售安排按原站列示，平台、抢先体验及待定标记均保留。日期请以发行商公告为准。</p>"
        image = section["image"]
        if image:
            content += '<img src="' + html_entities.escape(image, quote=True) + '" alt="GamesRadar calendar illustration">'
        content += "<ul>" + "".join("<li>" + html_entities.escape(game) + "</li>" for game in games) + "</ul>"
        url = site["url"] + "#" + section["anchor"]
        content += '<p>来源：<a href="' + url + '">GamesRadar 原始发售表</a></p>'
        items.append({"title": title, "original_url": url, "published_at": "",
                      "summary": str(len(games)) + " 款游戏的发售安排，包含原站列出的平台、日期及待定标记。",
                      "content": content, "image_url": image, "content_scope": "full_feed",
                      "source_name": site["name"], "language": "en", "evidence": "community",
                      "category": "launches", "game_count": len(games)})
    if not items:
        raise ValueError("Calendar sections or platform-tagged games are missing")
    return items


def mushroom_item(html, url, site):
    match = re.search(r'<script\b[^>]*\btype=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                      html, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("Missing resource metadata")
    graph = json.loads(match[1]).get("@graph", [])
    game = next((entry for entry in graph if entry.get("@type") == "VideoGame"), {})
    if game.get("applicationCategory") != site["site_category"]:
        raise ValueError("Resource category does not match the index")
    if urllib.parse.urlsplit(game.get("url", "")).path != urllib.parse.urlsplit(url).path:
        raise ValueError("Resource metadata does not match the requested page")
    title = " ".join(game.get("name", "").split())
    if not 1 <= len(title) <= 512:
        raise ValueError("Missing or invalid resource title")
    date_fields = {}
    for source, target in (("datePublished", "published_at"), ("dateModified", "updated_at")):
        value = game.get(source, "")
        if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            try:
                date_fields[target] = dt.date.fromisoformat(value).isoformat() + "T00:00:00+08:00"
            except ValueError:
                pass
    if not date_fields:
        raise ValueError("Missing resource date")
    cover = game.get("image", "")
    p = urllib.parse.urlsplit(cover)
    if (p.scheme != "https" or p.netloc != "www.oupai.xyz" or p.query or p.fragment
            or not re.fullmatch(r"/%E6%B8%B8%E6%88%8F%E5%B0%81%E9%9D%A2/\d+\.webp", p.path)):
        cover = ""
    return {"title": title, "original_url": url, "published_at": "", **date_fields,
            "update_date_precision": "day", "image_url": cover, "summary": "", "content": "",
            "content_scope": "metadata", "language": "zh-Hans", "evidence": "community",
            "source_name": site["name"], "platform": [site["platform"]], "category": "discovery"}


def ccplay_item(body, url, site):
    if not re.search(r'<h2>更新内容</h2>', body):
        return None
    def field(pattern):
        match = re.search(pattern, body, re.DOTALL)
        if not match:
            raise ValueError("Missing game detail field")
        return match[1].strip()

    title = clean_excerpt(field(r'<meta property="og:title" content="([^"]+)"'))
    date = dt.date.fromisoformat(field(r'<meta property="og:release_date"\s+content="([^"]+)"'))
    version = field(r'<div class="detail_related">\s*<p>版本：([0-9][0-9A-Za-z.+_-]{0,63})</p>')
    cover = urllib.parse.urljoin(url, field(r'<dt class="dt-(?:developer|cps)">\s*<img src="([^"]+)"'))
    image = urllib.parse.urlsplit(cover)
    if image.scheme != "https" or image.netloc != "ws-resource.ccplay.cc" or not image.path.startswith("/media/images/") or image.query or image.fragment:
        raise ValueError("Unexpected game cover")
    notes = field(r'<h2>更新内容</h2>[^<]*(?:(?!<h2>).)*?<pre>(.*?)</pre>')
    summary = clean_excerpt(re.sub(r"(?:https?:)?//[^\s<]+", "", notes))
    if not title or not summary:
        raise ValueError("Missing title or update notes")
    return {"title": title, "original_url": url, "published_at": "",
            "updated_at": date.isoformat() + "T00:00:00+08:00", "update_date_precision": "day",
            "version": version, "summary": summary, "image_url": cover, "content": "",
            "content_scope": "summary", "language": "zh-Hans", "evidence": "community",
            "source_name": site["name"], "platform": ["android"], "category": "discovery"}


def resource_details(body, site, robots, parse_item):
    rows, failures = [], []
    for index, candidate in enumerate(convert(body, site)[:RESOURCE_SCAN_LIMIT]):
        url = candidate["original_url"]
        if not robots.can_fetch(AGENT, url):
            failures.append("robots.txt disallows a resource page")
            continue
        if index:
            time.sleep(0.3)
        try:
            item = parse_item(fetch(url, site), url, site)
            if item is not None:
                rows.append(item)
        except (OSError, ValueError, TypeError, AttributeError) as error:
            failures.append(f"{url}: {error}")
            if isinstance(error, urllib.error.HTTPError) and error.code in (401, 403, 429):
                break
    return rows, failures


def collect(key, output, summary_limit=12):
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
        converter = {"wordpress": convert_wordpress, "rss": convert_rss, "nsthwj": convert_nsthwj, "calendar": convert_calendar}.get(site.get("format"), convert)
        incoming, failures = {}, []
        allow_empty = bool(site.get("illustrated_guide_title"))
        for index, url in enumerate(urls):
            if not robots.can_fetch(AGENT, url):
                failures.append("robots.txt disallows an index query")
                continue
            if index:
                time.sleep(1)
            try:
                body = fetch(url, site)
                if site.get("format") in {"mushroom", "ccplay"}:
                    parse_item = ccplay_item if site["format"] == "ccplay" else mushroom_item
                    converted, detail_errors = resource_details(body, site, robots, parse_item)
                    failures.extend(detail_errors[:5])
                else:
                    converted = converter(body, site)
                if not converted and not allow_empty:
                    raise ValueError("No matching entries; adapter needs review")
                for item in converted:
                    old = incoming.get(item["original_url"])
                    if old is None or item.get("updated_at", item["published_at"]) >= old.get("updated_at", old["published_at"]):
                        incoming[item["original_url"]] = item
            except Exception as error:
                failures.append(str(error)[:300])
                if isinstance(error, urllib.error.HTTPError) and error.code == 429:
                    break
        if not incoming and (failures or not allow_empty):
            raise ValueError("; ".join(failures) or "No matching entries")
        # Retain bounded last-good entries when a short upstream window drops them.
        previous = {}
        if path.exists() and site.get("format") != "calendar":
            try:
                cached = json.loads(path.read_text(encoding="utf-8"))
                if cached.get("status") == "ok":
                    previous = {x["original_url"]: x for x in cached["items"] if allowed(x["original_url"], site) and re.fullmatch(site["path"], urllib.parse.urlsplit(x["original_url"]).path)}
            except (ValueError, KeyError, TypeError):
                pass
        cached = previous.copy()
        previous.update(incoming)
        items = [metadata_tags(item) for item in previous.values()]
        # Dated updates lead; undated index entries retain upstream order, not fake times.
        items.sort(key=lambda x: max(x.get("updated_at", ""), x.get("published_at", "")), reverse=True)
        total = len(items)
        items = items[:100]  # All supported clients accept at most 100 items per feed.
        if site.get("format") not in {"mushroom", "ccplay"}:
            health.update(fill_descriptions(items, cached, site, robots, summary_limit))
        if site.get("format")=="nsthwj":
            health.update(download_items=sum(bool(x.get("download_links")) for x in items), download_links=sum(len(x.get("download_links",[])) for x in items))
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
    cli.add_argument("--summary-limit", type=int, choices=range(0, 101), default=12,
                     help="Maximum missing public description requests per source (0..100)")
    args = cli.parse_args()
    keys = SITES if args.site == "all" else [args.site]
    results = [collect(key, args.output, args.summary_limit) for key in keys]
    if any(key.startswith("nsthwj-") for key in keys):
        combine_nsthwj(args.output)
    print(json.dumps(results, ensure_ascii=True, indent=2))
    raise SystemExit(0 if all(r["status"] == "ok" for r in results) else 1)
