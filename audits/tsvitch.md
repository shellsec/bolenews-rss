# TsVitch source audit

Checked 2026-11-02 14:00 UTC against first-party repository metadata, releases, Atom, README and LICENSE. Evidence is saved alongside this note as `repo.body`, `atom.body`, `releases.body`, `readme.body`, `license.body`; counts are in `audit-metrics.json`. This is a snapshot, not an availability or runtime guarantee.

## Feed quality and freshness

The [native release Atom feed](https://github.com/giovannimirulla/TsVitch/releases.atom) returned HTTP 200 in the saved probe and is well-formed Atom XML. It contains six entries with six nonempty titles and six nonempty HTML content fields. No separate summaries, image markup, duplicate titles, or duplicate links occur in this sample. It declares `en-US`; the titles are version strings or English, and release notes are English. The newest entry update is 2026-01-09 21:58:25 UTC and the oldest is 2024-11-23 17:01:46 UTC; zero entries were updated in the preceding seven days. A live endpoint should not be described as a recently active publication stream based on these results.

The [official releases API](https://api.github.com/repos/giovannimirulla/TsVitch/releases?per_page=5) confirms [v0.3.2](https://github.com/giovannimirulla/TsVitch/releases/tag/v0.3.2) published 2026-01-09 21:58:25 UTC, with `prerelease: false`. The five saved API releases are all marked non-prerelease. The newest release lists `TsVitch.nro`, an Apple silicon DMG and an Intel DMG. Only asset names and metadata were inspected; binaries were not downloaded or executed. Preserve actual upstream statuses and titles; the instruction against adding preview labels to 波乐 does not modify upstream release facts.

## Classification and actual runtime evidence

The [README](https://github.com/giovannimirulla/TsVitch/blob/main/README.md) describes an IPTV/M3U multimedia player for Nintendo Switch, including Joy-Con/touch interface and installation of its NRO through hbmenu. It also explicitly states PC support is currently macOS and provides macOS build instructions; the README badge claims macOS 10.11+. Release asset names independently support both Intel and Apple silicon macOS packages. These are upstream statements, not device tests.

Use category `homebrew`/tools, and runtime tags `switch1` and `macos`. Do not claim Switch 2, Windows, Linux or Android support from this evidence. Acknowledgements mentioning other console toolchains are not runtime support claims. A Switch-ecosystem catalog and tools catalog are appropriate; keep the new source disabled by default. Subscribe through `Source.repo("giovannimirulla/TsVitch")` and GitHub Releases Atom; a custom remote JSON mirror is unnecessary.

## Scope and rights

The [repository API](https://api.github.com/repos/giovannimirulla/TsVitch) identifies GPL-3.0 and the [LICENSE](https://github.com/giovannimirulla/TsVitch/blob/main/LICENSE) contains the GNU GPL version 3. This is the software's source license; it does not establish permission for arbitrary images, IPTV playlists, streams or other referenced media. The README says the app includes a default playlist sourced from Free-TV/IPTV while separately stating it does not host IPTV content and users must ensure playlist content is authorized. This audit does not verify playlist rights or channel availability.

The requested integration is repository release news only. No playlist, stream, image, media data, or binary was fetched; no install/build scripts were run. Keep upstream attribution and links and avoid importing those unrelated resources into the news source. This audit changes no application, catalogs, publication, or deployment.
