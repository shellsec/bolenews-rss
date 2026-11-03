# RSSHub gaming route research — 2026-11-03

Scope: source candidates for BoleNews Switch, PlayStation, Steam and homebrew **news/release metadata**. No catalog changes or publication performed.

Verification: inspected the official [DIYgod/RSSHub repository](https://github.com/DIYgod/RSSHub) at commit `e616b5fd392113aa06ee71dc07a6143055cf5225` (remote HEAD at research time). The documentation site returned HTTP 403 to the research browser, so route declarations, parameters and implementations were checked directly. **Route existence does not establish live RSSHub endpoint health**; this report's route table records source verification, not live execution. Separate live instance results are recorded in `instance-results.json`, `route-results.json` and `english-platform-results.json` in this directory. The native feeds in the following section were independently checked live.

## Verified route candidates

Prepend the chosen RSSHub instance origin to each path. The source links are pinned to the inspected commit. “No config/browser” means the source declares `requireConfig:false` and `requirePuppeteer:false`; it is not an uptime guarantee.

| # | Source / fit | Exact candidate route | Limitations and evidence |
|---|---|---|---|
| 1 | Nintendo HK official news, Traditional Chinese | `/nintendo/news` | Explicitly **Hong Kong only**; parses HK topics and article pages. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/nintendo/news.ts) |
| 2 | Nintendo Direct official archive, English | `/nintendo/direct` | US/global Nintendo archive, depends on embedded Next.js/Apollo page data; not an HK-localized feed. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/nintendo/direct.ts) |
| 3 | Nintendo Switch official firmware notes, Japanese | `/nintendo/system-update` | Japan **Switch** system-update page; do not label it Switch 2 or homebrew news. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/nintendo/system-update.ts) |
| 4 | Nintendo HK new releases, Traditional Chinese | `/nintendo/eshop/hk` | HK software JSON and product-page extraction; not general news or a comprehensive price tracker. Feature flags not explicitly declared. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/nintendo/eshop-hk.ts) |
| 5 | PlayStation Plus official monthly games, English | `/ps/monthly-games` | Uses **Singapore English** PS Plus page. Regional lineups can differ. Notification-style entries can lack publication dates. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/ps/monthly-games.tsx) |
| 6 | Steam app announcements, Simplified Chinese | `/steam/news/730/schinese` | App-specific, **730 is Counter-Strike 2**; replace with the desired numeric app ID. Language selects source language, does not promise translation. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/steam/news.ts) |
| 7 | Steam app announcements, English | `/steam/news/730/english` | Same app-specific route; default language is English when omitted. Prefer native Steam feed for simple metadata use. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/steam/news.ts) |
| 8 | 游民星空 NS news, Simplified Chinese | `/gamersky/news/ns` | `ns` is explicitly mapped to NS; no `ps5` category exists in this route declaration. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/gamersky/news.ts) |
| 9 | 游民星空 PC/console news, Simplified Chinese | `/gamersky/news/pc` | Category label is 单机电玩, wider than Steam; platform filtering must be downstream. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/gamersky/news.ts) |
| 10 | A9VG Switch, Simplified Chinese | `/a9vg/news/Switch` | Case-sensitive category in official route table; do not use guessed `/a9vg/switch`. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/a9vg/index.ts) |
| 11 | A9VG PS5, Simplified Chinese | `/a9vg/news/PS5` | Official route table supports this exact category. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/a9vg/index.ts) |
| 12 | A9VG PC, Simplified Chinese | `/a9vg/news/PC` | PC is broader than Steam. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/a9vg/index.ts) |
| 13 | 巴哈姆特 GNN Switch, Traditional Chinese | `/gamer/gnn/ns` | Exact category option verified. **`antiCrawler:true`** in source; evaluate on the intended hosting network. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/gamer/gnn-index.ts) |
| 14 | 巴哈姆特 GNN PS5, Traditional Chinese | `/gamer/gnn/ps5` | Exact category option verified; same anti-crawler risk. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/gamer/gnn-index.ts) |
| 15 | 机核 news, Simplified Chinese | `/gcores/news` | General gaming news, requires topic classification/deduplication. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/gcores/news.ts) |
| 16 | 电玩巴士 news, Simplified Chinese | `/tgbus/list/news` | Exact allowed category is `news`; general gaming. Feature flags not explicitly declared. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/tgbus/list.ts) |
| 17 | 二柄 news, Simplified Chinese | `/diershoubing/news` | General gaming; app-origin source, extraction can change. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/diershoubing/news.tsx) |
| 18 | 游研社 articles, Simplified Chinese | `/yystv/docs` | All articles, includes features/culture beyond current news. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/yystv/docs.ts) |
| 19 | indienova articles, Simplified Chinese | `/indienova/article` | Independent games coverage; downstream Switch/PC matching needed. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/indienova/article.ts) |
| 20 | Eurogamer news, English | `/eurogamer/news` | Exact `news` category exists. Source states native feeds contain excerpts, while this RSSHub route fetches full article bodies; **prefer native feed for metadata aggregation**. No config/browser. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/eurogamer/index.ts) |

## Native alternatives checked live

Checked on 2026-11-03 using `curl.exe` with redirects. This proves response format/status at that moment, not ongoing availability or content licensing.

| Native feed | Result | Intended use |
|---|---|---|
| [PlayStation Blog](https://blog.playstation.com/feed/) | HTTP 200, `application/rss+xml` response header | Official English PS announcements. Full body was not XML-counted in this check. |
| [Steam CS2 news](https://store.steampowered.com/feeds/news/app/730/?l=schinese) | HTTP 200, RSS XML, 10 items | Official app news; replace app ID for selected games. `l=schinese` does not guarantee Chinese items: the response may remain English; classify actual item language. |
| [Eurogamer](https://www.eurogamer.net/feed) | HTTP 200, RSS XML, 100 items | English news metadata/excerpts; broad feed needs filtering. |
| [Atmosphère releases](https://github.com/Atmosphere-NX/Atmosphere/releases.atom) | HTTP 200, Atom XML, 10 entries | Switch open-source homebrew ecosystem release titles, dates and upstream links. |
| [hekate releases](https://github.com/CTCaer/hekate/releases.atom) | HTTP 200, Atom XML, 10 entries | Switch open-source bootloader release metadata; upstream links only. |

The two GitHub Atom feeds are preferable to inventing an RSSHub `/github/releases/...` route: no such route file appeared in the inspected current GitHub namespace. Do not substitute generic repo events without checking its token requirements; current `/github/repo_event/:owner/:repo/:types?` declares `GITHUB_ACCESS_TOKEN`. [Source](https://github.com/DIYgod/RSSHub/blob/e616b5fd392113aa06ee71dc07a6143055cf5225/lib/routes/github/repo-event.ts)

## Suggested initial shortlist and ingestion boundary

Start by testing Nintendo HK news, Nintendo system updates, A9VG Switch/PS5, 游民 NS/PC, 机核, native PlayStation Blog, native Steam app feeds, Eurogamer native RSS, and the two upstream GitHub release feeds. This balances official announcements, Chinese coverage and English reporting. Add GNN only after testing anti-crawler behavior on the deployment network.

Treat feeds as discovery inputs. For BoleNews retain source name, original title, canonical upstream URL, publication time, platform tags and a short attributed excerpt/summary. RSSHub extraction of a complete article does not itself grant republication rights. Keep homebrew coverage to project news, compatibility announcements and release metadata; do not ingest game dumps, ROM/download catalogs, keys, piracy links or circumvention tutorials. No claim of a formal legal review is made here.

Before catalog adoption, execute candidate routes on the intended RSSHub instance; check HTTP/XML success, nonempty entries, recent dates, canonical links, duplicate handling and whether the supplied source language matches the display label. These checks remain outstanding.
