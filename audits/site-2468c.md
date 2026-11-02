# 2468c.com source audit

Checked 2026-11-02 08:51 UTC. This is a bounded observation, not an uptime, rights, or future compatibility guarantee. Evidence files are in this directory; machine-readable counts are in `audit-metrics.json`.

## Actual feed observations

The [site RSS endpoint](https://2468c.com/feed/) returned HTTP 200 (redirecting to `/feed`), `application/rss+xml`, and parseable RSS 2.0. Its channel title is 奥德彪计划 and declared language is `zh-Hans`. The saved response contains 10 items, all within the preceding seven days: oldest 2026-11-02 00:51:36 UTC, latest 2026-11-02 06:01:20 UTC. All 10 have nonempty titles, descriptions, `content:encoded`, and image markup. Nine titles contain Chinese characters; titles also contain English game names. There are zero duplicate titles or links in this ten-item sample. These are sample counts, not a measured long-term publication rate. Evidence: `probe.json`, `feed.body`, `audit-metrics.json`.

The feed exposes article body and image markup. Those fields should not be ingested for this metadata-only integration; the WP API gives tighter field selection. No article pages, images, netdisk links, or game files were requested during this audit. Existing saved feed bytes were parsed locally.

## Actual API and category observations

The [first-party categories endpoint](https://2468c.com/wp-json/wp/v2/categories?per_page=50&_fields=id,name,slug,parent) returned these mappings (`categories.body`):

| ID | Category | Parent |
|---|---|---|
| 53 | PS4 资源 | 0 |
| 65 | PS5 资源 | 0 |
| 111 | PS5工具 | 110 |
| 112 | PS4工具 | 110 |
| 141 | exFAT/ffpkg | 65 |
| 147 | fpkg | 65 |
| 146 | LZ4 | 65 |
| 109 | 游戏攻略 | 0 |
| 69 | PS VR | 0 |

The [bounded filtered posts request](https://2468c.com/wp-json/wp/v2/posts?categories=53,65,111,112&per_page=30&_fields=id,date_gmt,link,title,categories) returned HTTP 200 and 30 items with exactly `id`, `date_gmt`, `link`, `title`, and `categories`. Every returned item intersects the four requested category IDs. Twenty-nine have category 65, one has 53; none of this page has 111 or 112. Category counts overlap: 29 also have 147 and five have 141. There are no duplicate IDs or links. Response headers reported 4,363 matching posts and 146 pages, but only the first 30 were requested. Evidence: `filtered-posts.body`, `audit-metrics.json`.

The observed five-item unfiltered API response also has the expected metadata structure (`posts.body`). Use category IDs from this first-party response; do not infer platforms from game titles. PS5 child categories are represented alongside 65 in this sample, but this does not establish that every future post will include its parent category.

## Access, rights, and operational limits

The [robots file](https://2468c.com/robots.txt) disallows `/wp-admin/`, permits its AJAX endpoint, and publishes a sitemap; it contains no general disallow in the observed response (`robots.body`). This is a crawler directive, not a reuse license or permission to redistribute content.

The [homepage](https://2468c.com/) footer displays © 2023 奥德彪. No reuse-license, terms, or copyright-policy link was identified in the saved homepage anchors. This limited inspection cannot establish that no policy exists elsewhere. The same homepage includes JavaScript that detects debugger delays, stops/reloads the window, and displays “不要扒我了”. That is a meaningful signal against scraping; API availability alone does not establish the operator authorizes aggregation. Evidence: `home.body`. No workaround or bypass was attempted.

A disabled-by-default, bounded metadata-only option is technically possible based on this response, but enabling ongoing collection merits checking operator permission and applicable terms. Restrict output to short titles, canonical site links, source timestamps, and platform labels; omit summaries, body, images, and download links. Preserve source attribution, rate-limit/cache requests, and stop on access refusal or endpoint changes. Do not enumerate all 146 pages or assume the observed sample guarantees stable access. Category names and content appear focused on console resources/packages and tools; this is not evidence of editorial verification, authorized distribution, or software safety.

For the planned integration, keep this optional source in the existing PS and games catalogs only, disabled by default; the main catalog is already at its 64-source cap. This audit changes no app code, catalog, clone, or deployment.
