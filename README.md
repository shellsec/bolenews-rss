# BoleNews sources

Data repository for [BoleNews](https://github.com/shellsec/bolenews). Contains a declarative source catalog, public index metadata and the bounded maintenance collector. No application installers, game files, private tokens, article bodies or publisher image copies.

## One subscription

Original catalog: https://raw.githubusercontent.com/shellsec/bolenews-rss/master/sources.json

Accelerated catalog: https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/bolenews-rss/master/sources.json

Use the original URL in BoleNews. Version0.1.2+ recognizes a collection, uses proxy→origin fallback for eligible Raw JSON and loads the declared child feeds. The catalog also lists native RSS/Atom sources; RSS is not replaced. A single content JSON can still be subscribed directly, such as `/master/feeds/ns45.json`. Source and article state remain local.

`schema_version:1`, increasing positive `config_version`, and `sources:[...]` describe a catalog. Child URLs are absolute public HTTPS feeds. No executable fields, scripts, installation commands or nested catalogs. Increment config_version when changing source definitions; updating article content alone does not require a catalog-version change. Personal subscriptions/overrides are separate from catalog snapshots.

## Content updates

Open BoleNews to read subscribed content. Refresh the catalog in the app and enable the sources you want. Newly added sources are off by default; existing choices are stored locally. Server-side collection runs automatically. Readers do not need to visit GitHub or operate workflows.

The main catalog stays within version0.1.2's 64-child limit. Additional opt-in catalogs in `catalogs/` provide tools, games and platform-specific selections. Add the desired catalog as a normal remote JSON subscription; these are independent flat catalogs, not nested collections. Importing overlapping catalogs can request the same feed twice, so choose a main catalog or a suitable specialist selection.

Local maintenance: `python3 tools/collect_web_feeds.py --site all`, then `python3 tools/validate_feeds.py`. Six adapters read only public directory/feed titles/links and, where explicitly supplied, publication dates. Gamer520 uses its public WordPress API Switch category, not its inaccessible homepage. The opt-in 2468c adapter requests only five metadata fields and uses verified PS4/PS5 category IDs; site post dates are not game release dates. GNN metadata includes attribution and unchanged original links under its non-commercial RSS terms (see audits). Other newly listed media RSS feeds are read directly, not copied into this repository. Empty/failed parsing preserves prior successful files; `.health.json` records each attempt. Partial failure publishes other successful updates, retains failed sources' last-good content and marks the workflow failed for visibility.

The exposed metadata does not verify claims in article titles or confer fulltext/image redistribution permission. Community information remains labeled community. No download links are resolved, no game files fetched and no page scripts executed. HTTPS verification remains enabled. robots.txt rules are honored; HTTP4xx unavailable handling follows RFC9309, while429/server/TLS failures stop collection.

GitHub scheduled workflows can be delayed, so generated_at and health files record actual times. gh-proxy is a third-party transport, not storage and not a fix for an absent origin file. If the origin returns404, publish the missing file/branch first. No token/API key is needed by BoleNews readers.

2468c / 奥德彪计划 PS4/PS5 metadata: https://raw.githubusercontent.com/shellsec/bolenews-rss/master/feeds/2468c.json . Available as a disabled opt-in source in catalogs/playstation.json and catalogs/games.json (v5). The main catalog stays v4/64 to preserve compatibility and existing choices. No NRO rebuild is needed: select or refresh the PlayStation catalog in the app, then enable this source if desired.

NX2Apple: native Release Atom https://github.com/LNPANDY/NX2Apple/releases.atom . Added disabled in tools and Switch-ecosystem catalogs; also available in the independent https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/apple.json catalog. Runtime tags are macos/ios (including iPadOS), not Switch/Windows/Android. Existing clients can read it from All/Tools; they do not yet expose Apple-specific filter choices. Upstream candidate/experimental release facts are preserved; game files and release bodies are not mirrored here.

TsVitch: native Release Atom https://github.com/giovannimirulla/TsVitch/releases.atom . This homebrew IPTV player is listed disabled in tools, Switch and Apple catalogs with switch1/macos runtimes. Only software update information is subscribed; no playlists, channels, media or program binaries are mirrored.

The tools catalog is a 64-source selection. Additional practical sources are in the platform catalogs and `catalogs/tools-extra.json`; do not import every overlapping catalog blindly. New sources remain disabled until the reader chooses to enable them. Source audits distinguish recent app publications from release edits, dependency packages and canary builds.
