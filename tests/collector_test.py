import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("collector", Path(__file__).resolve().parents[1] / "tools/collect_web_feeds.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class CollectorTest(unittest.TestCase):
    def test_2468c_platform_scope_and_metadata_only(self):
        site = c.SITES["2468c"]
        payload = [
            {"title": {"rendered": "PS5 &amp; game"}, "link": "https://2468c.com/123.html", "date_gmt": "2026-11-02T06:01:20", "categories": [65, 147], "content": {"rendered": "not collected"}},
            {"title": {"rendered": "PS4 tool"}, "link": "https://2468c.com/124.html", "categories": [112]},
            {"title": {"rendered": "Unknown platform"}, "link": "https://2468c.com/125.html", "categories": [43]},
            {"title": {"rendered": "External link"}, "link": "https://evil.test/126.html", "categories": [65]},
            {"title": {"rendered": "Wrong category type"}, "link": "https://2468c.com/127.html", "categories": "65"},
            {"title": {"rendered": "Duplicate"}, "link": "https://2468c.com/123.html", "categories": [65]}]
        rows = c.convert_wordpress(c.json.dumps(payload), site)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["platform"], ["ps5"])
        self.assertEqual(rows[0]["title"], "PS5 & game")
        self.assertEqual(rows[0]["published_at"], "2026-11-02T06:01:20Z")
        self.assertEqual(rows[1]["platform"], ["ps4"])
        self.assertEqual(rows[1]["category"], "homebrew")
        self.assertEqual(rows[1]["published_at"], "")
        self.assertTrue(all(not r['content'] and not r['image_url'] and not r['summary'] for r in rows))

    def test_gnn_metadata_dates_and_provenance(self):
        payload = '''<rss><channel>
          <item><title>New &amp; Game</title><link>https://gnn.gamer.com.tw/detail.php?sn=12</link>
          <pubDate>Mon, 02 Nov 2026 12:41:49 +0800</pubDate><description>Publisher RSS excerpt</description></item>
          <item><title>Duplicate</title><link>https://gnn.gamer.com.tw/detail.php?sn=12</link></item>
          <item><title>Other domain</title><link>https://evil.test/detail.php?sn=13</link></item>
          <item><title>Unknown date</title><link>https://gnn.gamer.com.tw/detail.php?sn=14</link><pubDate>unknown</pubDate></item>
        </channel></rss>'''
        rows = c.convert_rss(payload, c.SITES['gnn'])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['published_at'], '2026-11-02T04:41:49Z')
        self.assertEqual(rows[1]['published_at'], '')
        self.assertEqual(rows[0]['source_name'], c.SITES['gnn']['name'])
        self.assertTrue(all(not r['content'] and not r['image_url'] for r in rows))
        self.assertEqual(rows[0]['summary'], 'Publisher RSS excerpt')
        with self.assertRaises(ValueError):
            c.convert_rss('<!DOCTYPE rss [<!ENTITY x "bad">]><rss/>', c.SITES['gnn'])

    def test_publisher_excerpt_not_full_article(self):
        payload = [{"title": {"rendered": "Game title"}, "link": "https://vip.gamers520.com/12.html",
                    "excerpt": {"rendered": "<p>Publisher short introduction &amp; notes.</p><script>bad()</script>", "protected": False},
                    "content": {"rendered": "Do not collect full article"}},
                   {"title": {"rendered": "Protected"}, "link": "https://vip.gamers520.com/13.html",
                    "excerpt": {"rendered": "Private description", "protected": True}}]
        rows = c.convert_wordpress(c.json.dumps(payload), c.SITES['gamer520'])
        self.assertEqual(rows[0]['summary'], 'Publisher short introduction & notes.')
        self.assertEqual(rows[0]['content_scope'], 'summary')
        self.assertEqual(rows[1]['summary'], '')
        self.assertEqual(rows[0]['content'], '')
        self.assertEqual(c.clean_excerpt('<p>[&hellip;]</p>'), '')
        self.assertLessEqual(len(c.clean_excerpt('中' * 1000)), 241)

    def test_public_description_cache_and_robots(self):
        site=c.SITES['a9vg']; robots=c.urllib.robotparser.RobotFileParser()
        robots.parse(['User-agent: *', 'Allow: /'])
        row={'title':'New game', 'original_url':'https://www.a9vg.com/article/123', 'summary':''}
        with patch.object(c,'fetch',return_value='<meta content="Publisher provided game introduction." name="description">') as f:
            health=c.fill_descriptions([row],{},site,robots,12)
            self.assertEqual(f.call_count,1)
        self.assertEqual(health['summary_count'],1)
        self.assertEqual(row['summary'],'Publisher provided game introduction.')
        newer={'title':'New game','original_url':row['original_url'],'summary':''}
        with patch.object(c,'fetch') as f:
            c.fill_descriptions([newer],{row['original_url']:row},site,robots,12)
            self.assertEqual(f.call_count,0)
        self.assertEqual(newer['summary'],row['summary'])
        robots=c.urllib.robotparser.RobotFileParser()
        robots.parse(['User-agent: *', 'Disallow: /article/'])
        with patch.object(c,'fetch') as f:
            c.fill_descriptions([{'title':'Other game','original_url':row['original_url'],'summary':''}],{},site,robots,12)
            self.assertEqual(f.call_count,0)

    def test_wordpress_public_metadata(self):
        payload = [{"title": {"rendered": "Switch &amp; Update"},
                    "link": "https://vip.gamers520.com/123.html",
                    "date_gmt": "2026-11-01T00:30:38"},
                   {"title": 42},
                   {"title": {"rendered": "Unsafe"}, "link": "file:///bad"}]
        rows = c.convert_wordpress(c.json.dumps(payload), c.SITES["gamer520"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Switch & Update")
        self.assertEqual(rows[0]["published_at"], "2026-11-01T00:30:38Z")

    def test_unavailable_robots_public_api_and_rate_limit(self):
        payload = c.json.dumps([{"title": {"rendered": "Switch Update"},
                                 "link": "https://vip.gamers520.com/123.html"}])
        for code, expected_calls, expected_status in [(403, 3, "ok"), (429, 1, "unavailable"),
                                                       (503, 1, "unavailable")]:
            with tempfile.TemporaryDirectory() as tmp:
                error = c.urllib.error.HTTPError("https://vip.gamers520.com/robots.txt", code, "error", {}, None)
                with patch.object(c, "fetch", side_effect=[error, payload, payload]) as f:
                    result = c.collect("gamer520", Path(tmp), summary_limit=0)
                    self.assertEqual(f.call_count, expected_calls)
                    self.assertEqual(result["status"], expected_status)

    def test_edits_and_update_signals(self):
        payload = [{"title": {"rendered": "游戏 本体+v1.8d.6523升补"},
                    "link": "https://vip.gamers520.com/123.html",
                    "date_gmt": "2020-01-01T00:00:00", "modified_gmt": "2026-11-03T04:06:19"}]
        rows = c.convert_wordpress(c.json.dumps(payload), c.SITES["gamer520"])
        self.assertEqual(rows[0]["published_at"], "2020-01-01T00:00:00Z")
        self.assertEqual(rows[0]["updated_at"], "2026-11-03T04:06:19Z")
        self.assertEqual(rows[0]["tags"], ["game_update"])
        self.assertEqual(rows[0]["platform"], ["switch1"])
        self.assertEqual(rows[0]["version"], "v1.8d.6523")
        for title in ["遊戲升級補丁", "Game hotfix", "游戏1DLC"]:
            self.assertIn("game_update", c.metadata_tags({"title": title}).get("tags", []))
        self.assertEqual(c.metadata_tags({"title": "固件更新"})["tags"], ["firmware_update"])
        self.assertNotIn("game_update", c.metadata_tags({"title": "游戏攻略"}).get("tags", []))

    def test_new_and_modified_union_retains_old_and_partial(self):
        def payload(id, title):
            return c.json.dumps([{"title": {"rendered": title}, "link": f"https://vip.gamers520.com/{id}.html"}])
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with patch.object(c, "fetch", side_effect=["User-agent: *\nAllow: /", payload(1, "New game"), payload(2, "Old game 升补")]):
                health = c.collect("gamer520", output, summary_limit=0)
            self.assertEqual(health["count"], 2)
            self.assertEqual(health["status"], "ok")
            with patch.object(c, "fetch", side_effect=["User-agent: *\nAllow: /", payload(3, "Another game"), ValueError("timeout")]):
                health = c.collect("gamer520", output, summary_limit=0)
            self.assertEqual(health["status"], "partial")
            self.assertEqual(health["count"], 3)
            self.assertEqual(health["retained_count"], 2)

    def test_nsthwj_platforms_index_and_no_fabricated_download(self):
        games=[{"id":12,"name":"Game title","gameType":"switch","version":"1.2.0","gameSize":"2GB","summary":"Public game description","updateTime":"2026-11-04","picUrl":"https://example.com/a.jpg"},
               {"id":13,"name":"Wrong platform","gameType":"pc"},
               {"id":"../escape","name":"Bad ID","gameType":"switch"}]
        body='<script>ignored()</script><script id="thwj-seo-bootstrap" type="application/json">'+c.json.dumps({"games":games})+'</script>'
        rows=c.convert_nsthwj(body,c.SITES['nsthwj-switch'])
        self.assertEqual(len(rows),1)
        row=rows[0]
        self.assertEqual(row['original_url'],'https://nsthwj.cn/game/switch/12')
        self.assertEqual(row['platform'],['switch1'])
        self.assertEqual(row['version'],'1.2.0')
        self.assertEqual(row['updated_at'],'2026-11-04T00:00:00+08:00')
        self.assertEqual(row['published_at'],'')
        self.assertEqual(row['content'],'')
        self.assertEqual(row['image_url'],'')
        self.assertEqual(row['download_status'],'not_verified')
        self.assertNotIn('download_links',row)
        self.assertNotIn('game_update',row.get('tags',[]))
        for platform in ('pc','ps4'):
            games[0]['gameType']=platform
            body='<script id="thwj-seo-bootstrap">'+c.json.dumps({"games":games[:1]})+'</script>'
            parsed=c.convert_nsthwj(body,c.SITES['nsthwj-'+platform])
            self.assertEqual(parsed[0]['platform'],[platform])
        with self.assertRaises(ValueError):c.convert_nsthwj('<html>Broken index</html>',c.SITES['nsthwj-switch'])

    def test_combined_nsthwj_reserves_space_for_older_platforms(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            for platform, date, count in (("switch", "2026-11-06", 80),
                                          ("pc", "2026-11-05", 45),
                                          ("ps4", "2026-11-04", 12)):
                items = [{"original_url": f"https://nsthwj.cn/game/{platform}/{i}",
                          "updated_at": date} for i in range(count)]
                c.atomic_json(output / f"nsthwj-{platform}.json",
                              {"status": "ok", "generated_at": date, "items": items})
            c.combine_nsthwj(output)
            items = c.json.loads((output / "nsthwj.json").read_text(encoding="utf-8"))["items"]
            self.assertEqual(len(items), 100)
            self.assertEqual(sum("/switch/" in item["original_url"] for item in items), 55)
            self.assertEqual(sum("/pc/" in item["original_url"] for item in items), 33)
            self.assertEqual(sum("/ps4/" in item["original_url"] for item in items), 12)

    def test_verified_nsthwj_share_links_expire_on_version_change(self):
        url='https://nsthwj.cn/game/switch/137808'
        links=c.nsthwj_download_links(url,'最新版本：1.0.0','2026-11-04')
        self.assertEqual(len(links),2)
        self.assertEqual({c.urllib.parse.urlsplit(x['url']).hostname for x in links},{'pan.baidu.com','pan.quark.cn'})
        self.assertEqual(c.nsthwj_download_links(url,'最新版本：2.0.0','2026-11-04'),[])
        self.assertEqual(c.nsthwj_download_links(url,'最新版本：1.0.0','2026-11-05'),[])
        self.assertEqual(c.nsthwj_download_links('https://nsthwj.cn/game/switch/1','最新版本：1.0.0','2026-11-04'),[])

    def test_only_matching_metadata(self):
        html = '''<a href="/article/123"><img src="x">Switch 2 补丁</a>
          <a href="https://evil.test/article/123">Other site</a>
          <a href="/article/123">Switch 2 补丁</a>
          <a href="/article/123">查看详细</a>
          <script><a href="/article/456">Script link</a></script>'''
        rows = c.convert(html, c.SITES["a9vg"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Switch 2 补丁")
        self.assertEqual(rows[0]["published_at"], "")
        self.assertEqual(rows[0]["image_url"], "")

    def test_failure_preserves_good_feed(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            with patch.object(c, "fetch", side_effect=["User-agent: *\nAllow: /", '<a href="/article/123">Example title</a>']):
                self.assertEqual(c.collect("a9vg", output, summary_limit=0)["status"], "ok")
            before = (output / "a9vg.json").read_bytes()
            with patch.object(c, "fetch", side_effect=ValueError("TLS unavailable")):
                self.assertEqual(c.collect("a9vg", output, summary_limit=0)["status"], "unavailable")
            self.assertEqual((output / "a9vg.json").read_bytes(), before)

    def test_robots_and_initial_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(c, "fetch", return_value="User-agent: *\nDisallow: /") as f:
                result = c.collect("gamer520", Path(tmp), summary_limit=0)
                self.assertEqual(f.call_count, 1)
                self.assertEqual(result["status"], "unavailable")
            self.assertIn('"status": "unavailable"', (Path(tmp) / "gamer520.json").read_text())


if __name__ == "__main__":
    unittest.main()
