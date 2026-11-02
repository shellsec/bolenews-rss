# BoleNews sources

Data repository for [BoleNews](https://github.com/shellsec/bolenews). Contains a declarative source catalog, public index metadata and the bounded maintenance collector. No application installers, game files, private tokens, article bodies or publisher image copies.

## One subscription

Original catalog: https://raw.githubusercontent.com/shellsec/bolenews-rss/master/sources.json

Accelerated catalog: https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/bolenews-rss/master/sources.json

Use the original URL in BoleNews. Version0.1.2+ recognizes a collection, uses proxy→origin fallback for eligible Raw JSON and loads the declared child feeds. The catalog also lists native RSS/Atom sources; RSS is not replaced. A single content JSON can still be subscribed directly, such as `/master/feeds/ns45.json`. Source and article state remain local.

`schema_version:1`, increasing positive `config_version`, and `sources:[...]` describe a catalog. Child URLs are absolute public HTTPS feeds. No executable fields, scripts, installation commands or nested catalogs. Increment config_version when changing source definitions; updating article content alone does not require a catalog-version change. Personal subscriptions/overrides are separate from catalog snapshots.

## Automatic and manual updates

GitHub Actions runs hourly at minute23 and can be run manually: Actions → Update BoleNews sources → Run workflow. The app can also manually refresh the catalog and its child feeds; that downloads current published files, it does not launch server-side collection.

Local maintenance: `python3 tools/collect_web_feeds.py --site all`, then `python3 tools/validate_feeds.py`. Four adapters read only public directory titles/links and, where explicitly supplied, publication dates. Gamer520 uses its public WordPress API Switch category, not its inaccessible homepage. Empty/failed parsing preserves prior successful files; `.health.json` records each attempt. Partial failure publishes other successful updates, retains failed sources' last-good content and marks the workflow failed for visibility.

The exposed metadata does not verify claims in article titles or confer fulltext/image redistribution permission. Community information remains labeled community. No download links are resolved, no game files fetched and no page scripts executed. HTTPS verification remains enabled. robots.txt rules are honored; HTTP4xx unavailable handling follows RFC9309, while429/server/TLS failures stop collection.

GitHub scheduled workflows can be delayed, so generated_at and health files record actual times. gh-proxy is a third-party transport, not storage and not a fix for an absent origin file. If the origin returns404, publish the missing file/branch first. No token/API key is needed by BoleNews readers.
