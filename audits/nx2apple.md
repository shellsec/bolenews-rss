# NX2Apple source audit

Checked 2026-11-02 10:16 UTC. Findings describe saved first-party responses and are not a future availability or compatibility guarantee. Evidence: `repo.body`, `atom.body`, `releases.body`, `readme.body`, `license.body`; counts: `audit-metrics.json`.

## Subscription and observed feed

The native [GitHub release Atom feed](https://github.com/LNPANDY/NX2Apple/releases.atom) is a suitable optional release-news source; no JSON mirror is necessary. The saved HTTP-200 response parses as Atom and has 10 entries, 10 nonempty titles, and 10 nonempty HTML content fields. All ten `updated` timestamps fall within the preceding seven days. Latest updated: 2026-11-01 21:41:43 UTC; oldest: 2026-11-01 02:54:56 UTC. These are entry update dates, not necessarily original release publication dates. There are zero duplicate titles or links and no `<img>` markup in entry content. The feed declares `en-US`; one title contains Chinese characters, and release text is predominantly English with some Chinese. The content field supplies release-note descriptions rather than a separate Atom summary. This ten-entry snapshot is not a long-term cadence estimate.

The newest Atom entry observed is [v1.0.1-rc2](https://github.com/LNPANDY/NX2Apple/releases/tag/v1.0.1-rc2); the [official releases API](https://api.github.com/repos/LNPANDY/NX2Apple/releases?per_page=5) marks it `prerelease: true`, published 2026-11-01 21:41:25 UTC. The latest stable version in the saved API sample is [v1.0.0](https://github.com/LNPANDY/NX2Apple/releases/tag/v1.0.0), published 2026-11-01 17:02:53 UTC. The API also returns an `engine-experimental` prerelease published 2026-11-02 01:00:35 UTC which is absent from the saved Atom sample. Therefore the Atom list should not be described as exhaustive or rc2 as universally the most recently published release. Preserve upstream prerelease flags and titles; the local instruction against adding preview labels to 波乐 branding does not change upstream release facts.

## Correct category and runtime

The [primary README](https://github.com/LNPANDY/NX2Apple/blob/main/README.md) describes a community fork of nxnative which adds a graphical launcher and patch queue. Its own description says game code runs natively on Apple silicon, using Metal, and calls the project not an emulator. This is the project's characterization; no build or performance verification was performed here.

Classify it as a homebrew/development tool in the Switch ecosystem, with runtime platforms `macos` and `ios` (the latter includes iPadOS in the existing platform vocabulary). Switch describes the source game ecosystem, not a device on which this launcher runs. The README supports Apple silicon Mac plus iPhone/iPad targets; it provides no basis for labeling this release as runnable on Switch, Windows, or Android. The launcher opens on macOS 13+, while the documented build toolchain can require newer macOS/Xcode; iPhone/iPad targets require iOS/iPadOS 26+ and recent devices. These upstream requirements can change and are not a test result.

The README requires users' own game dumps and console keys, says these are not bundled or downloaded, and limits support to games with profiles. Subscribe to repository release metadata and source links; do not fetch games, keys, scripts, or release binaries as part of source ingestion.

## Rights and proposed integration

The repository [LICENSE](https://github.com/LNPANDY/NX2Apple/blob/main/LICENSE) is MIT, covering the software and associated documentation and requiring preservation of copyright and permission notices in copies or substantial portions. The [repository API](https://api.github.com/repos/LNPANDY/NX2Apple) also identifies MIT. This supports attribution and linking to project release news, but is not a blanket license for game content, artwork, third-party assets, or every item referenced in release notes. Keep release excerpts proportionate and attributed; do not infer rights to proprietary game files from the repository license.

The proposed disabled-by-default `Source.repo("LNPANDY/NX2Apple")` belongs in tools and Switch-ecosystem catalogs. An optional Apple catalog can remain a flat source list. The current client has no Apple-specific filter; users can view it through all/tools, so avoid implying an Apple filter already exists. This audit changes no application code, catalogs, clones, or deployments.
