# Multiplatform tool source audit

Checked 2026-11-02 UTC. Research only; no catalog changes or binary downloads. Feed requests reused research/probe_sources.py. Raw HTTP bodies, repository HTML, release HTML and asset-list HTML are saved in raw/. API 403 rate limits are documented in source-results.json; primary HTML supplied license/archive/runtime evidence instead. A single successful observation is not stability or device verification.

| Rank | Source | HTTP/items | Latest UTC | Last 7d | Titles/summaries/images | Duplicate title/URL | License; archive | Runtime |
|---|---|---|---|---|---|---|---|---|
| 1 | [Sunshine](https://github.com/LizardByte/Sunshine) | 200/10 | 2026-11-02T10:02:42+00:00 | 2 | 10/10/10 | 0.0/0.0 | GPL-3.0; no archived banner | pc, linux, macos |
| 2 | [chiaki-ng](https://github.com/chiaki-ng/chiaki-ng) | 200/10 | 2026-10-31T02:33:38+00:00 | 1 | 10/10/10 | 0.0/0.0 | AGPL-3.0; no archived banner | pc, linux, macos |
| 3 | [RetroFlow Launcher](https://github.com/jimbob4000/RetroFlow-Launcher) | 200/10 | 2026-10-11T10:53:49+00:00 | 0 | 10/10/10 | 0.0/0.0 | MIT; no archived banner | vita |
| 4 | [Moonlight Qt](https://github.com/moonlight-stream/moonlight-qt) | 200/10 | 2026-10-06T02:07:37+00:00 | 0 | 10/10/10 | 0.0/0.0 | GPL-3.0; no archived banner | pc, linux, macos |

All four primary feeds declare en-US and have parseable dates and nonempty English release titles. Feed image counts include contributor avatars; images stay disabled. No selected repository or URL duplicates the current 52-source catalog, nor each other. Sunshine is a streaming host; Moonlight Qt is its complementary desktop client, so these have distinct roles. chiaki-ng targets PS4/PS5 remote play but executes on client systems: do not tag PS4/PS5 runtime. README lists wider historical Chiaki ports; selected platforms conservatively describe desktop chiaki-ng. Its latest feed includes weekly canary releases, factual upstream status. RetroFlow is a substantial launcher with per-game emulator integration, not another generic emulator fork.

Primary runtime and packaging evidence:
- [Sunshine README](https://github.com/LizardByte/Sunshine) and [getting started](https://github.com/LizardByte/Sunshine/blob/master/docs/getting_started.md): host on Windows/Linux/macOS; latest expanded assets contain MSI, AppImage/Flatpak/RPM and DMG.
- [Moonlight Qt README](https://github.com/moonlight-stream/moonlight-qt): Windows/Mac/Linux PC client; v6.2.0 assets contain EXE, AppImage and DMG. No Android tag: Android client is another repository.
- [chiaki-ng README](https://github.com/chiaki-ng/chiaki-ng): client for PlayStation Remote Play; latest asset listing has Windows EXE and Linux Flatpak/AppImage; macOS is explicitly listed by README. Canonical owner verified from Streetpea redirect.
- [RetroFlow README](https://github.com/jimbob4000/RetroFlow-Launcher): PS Vita launcher, installation requires RetroFlow VPK; v8.5.0 asset is RetroFlow_v8.5.0.vpk. Original suggested RetroFlowTeam owner returned 404 and is excluded.

Additional practical candidates and exclusions:
- VitaDeploy: valid 200 Atom, 7 entries, latest 2025-10-25, useful Vita setup toolbox; practical fallback but older release activity than four selected.
- Itemzflow: valid 200 Atom, 8 entries, latest 2026-05-31; actual PS4/PS5 manager. Reserve for console emphasis, not among four strongest current sources.
- GoldHEN Cheat Manager: valid 200 Atom but one 2024-01-02 entry and repository explicitly archived. Reject as inactive.

Rights: repository code licenses are factual metadata, not permission to redistribute release articles or binaries. Candidates use direct personal upstream feed reading only, images disabled, no bundled articles/media, code, or executables. No binaries, scripts, media, or game files were requested.

Complete candidates (four primary plus VitaDeploy and Itemzflow reserves) are disabled for root selection. source-results.json records raw feed metrics; primary-evidence.json records archive checks; asset-evidence.json lists packaging metadata only.

Release dates versus Atom updates: Atom exposes `updated`, not publication dates. Primary release-page relative-time records show Sunshine 2026-11-02T06:38:31Z; chiaki-ng 2026-10-31T02:14:28Z; RetroFlow 2026-10-11T10:51:36Z; Moonlight Qt 2026-10-04T00:44:48Z (Atom updated October 6); VitaDeploy 2025-10-25T08:01:44Z; Itemzflow 2026-05-31T22:08:52Z. Sunshine recent feeds include frequent upstream builds; chiaki-ng latest is explicitly weekly canary, not a stable version claim. No test or build performed.

Reserve evidence: VitaDeploy repository license MIT, not archived; current release HTML lists VitaDeploy.vpk and VitaDeploy-mshell.vpk, actual Vita runtime. Itemzflow repository GPL-3.0, not archived; README describes PS4 manager and explicit PS5 compatibility list; feed includes dedicated PS5 release. Latest release is source/developer update with no attached binary assets, so no current package availability claim. Both feeds have English titles, parseable dates, title/URL duplicate ratios zero. Reserve candidates added for platform catalogs at root discretion; GoldHEN Cheat Manager stays excluded because archive status outweighs older practical utility.
