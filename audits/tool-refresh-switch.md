# Switch practical tool source audit — 2026-11-02

Read-only primary-source audit. No upstream scripts or binaries executed; no binary/media/playlists/game files downloaded. Feed raw bodies, repository metadata, README (base64 API response), latest release metadata retained under `raw/` locally. Repository-code licenses do not automatically cover release prose, screenshots, trademarks, third-party services or media. Candidates read upstream feeds directly for personal use; no content or images bundled. Hardware/firmware compatibility not tested.

## Recommended order

Top eight: switchfin, wiliwili, checkpoint, moonlight-switch, nx-activity-log, sysdvr, nxmp, nx-ovlloader. Others are practical fallbacks, not claims of recent releases. All candidate sources are disabled by default, images off, full content on. No Switch 2 runtime inferred.

Atom uses `<updated>`; latest and last-seven-days metrics therefore measure release-feed edits, not necessarily new app binaries. Switchfin has dependency-package tags: latest observed feed update 2026-10-27 and three recent entries are not a new Switchfin app version; app 0.9.4 metadata publishes 2026-08-25.

## Observed metrics

|Source|HTTP|Entries|Latest Atom update UTC|Last7|Titles / summaries / dates|Images / non-avatar|Title / URL duplicate ratio|
|---|---:|---:|---|---:|---|---|---|
|switchfin|200|10|2026-10-27T09:00:08+00:00|3|10 / 5 / 10|10 / 10|0.0 / 0.0|
|wiliwili|200|10|2026-04-25T14:11:22+00:00|0|10 / 10 / 10|10 / 2|0.0 / 0.0|
|checkpoint|200|10|2026-10-13T19:25:37+00:00|0|10 / 10 / 10|10 / 10|0.0 / 0.0|
|moonlight-switch|200|10|2026-06-24T20:27:07+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|nx-activity-log|200|10|2026-10-19T13:40:00+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|sysdvr|200|10|2026-02-10T21:15:07+00:00|0|10 / 10 / 10|10 / 1|0.0 / 0.0|
|nxmp|200|10|2025-12-17T09:24:48+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|nx-ovlloader|200|9|2026-07-18T12:22:08+00:00|0|9 / 9 / 9|9 / 0|0.0 / 0.0|
|nx-hbloader|200|10|2025-11-15T16:51:11+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|turnips|200|10|2026-05-16T18:34:32+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|nx-shell|200|10|2022-08-07T18:32:20+00:00|0|10 / 10 / 10|10 / 1|0.0 / 0.0|
|sys-con|200|10|2024-11-06T19:17:45+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|
|tesla-menu|200|10|2023-05-27T12:55:49+00:00|0|10 / 10 / 10|10 / 0|0.0 / 0.0|

## 1. Switchfin (`switchfin`)

Jellyfin client: browse and play your server media.
- [Official repository / README](https://github.com/dragonflylee/switchfin); [native release feed](https://github.com/dragonflylee/switchfin/releases.atom); [release metadata](https://api.github.com/repos/dragonflylee/switchfin/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1, psvita, ps4, windows, macos, linux, android. Latest assets: `IV0001-SFIN00000_00-SFIN000000009400.pkg, switchfin-0.9.4-1-x86_64.pkg.tar.zst, Switchfin-arm64-v8a.apk, Switchfin-armeabi-v7a.apk, Switchfin-Linux-aarch64-gl.flatpak, Switchfin-Linux-aarch64-gles2.flatpak, Switchfin-Linux-x86_64-gl.flatpak, Switchfin-macOS-Intel.dmg, Switchfin-macOS-Silicon.dmg, Switchfin-windows-arm64.zip, Switchfin-windows-x64.zip, Switchfin-windows-x86.zip, Switchfin.nro, Switchfin.vpk`.
- Repository archived: False; fork: False; pushed: 2026-10-27T09:19:50Z. Code license detected by GitHub: Apache-2.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-08-25T16:39:52Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["Switchfin 0.9.4", "vita-packages", "switch-portlibs"].

## 2. wiliwili (`wiliwili`)

Controller-oriented third-party Bilibili client.
- [Official repository / README](https://github.com/xfangfang/wiliwili); [native release feed](https://github.com/xfangfang/wiliwili/releases.atom); [release metadata](https://api.github.com/repos/xfangfang/wiliwili/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1, psvita, ps4, windows, macos, linux. Latest assets: `wiliwili-Linux-aarch64-gl.flatpak, wiliwili-Linux-aarch64-gles2.flatpak, wiliwili-Linux-aarch64-switchroot-ubuntu.AppImage, wiliwili-Linux-aarch64-switchroot-ubuntu.deb, wiliwili-Linux-x86_64.flatpak, wiliwili-macOS-AppleSilicon.dmg, wiliwili-macOS-IntelChip.dmg, wiliwili-macOS-IntelChip_10.11.dmg, wiliwili-macOS-Universal.dmg, wiliwili-NintendoSwitch.zip, wiliwili-PS4.pkg, wiliwili-PSV.vpk, wiliwili-Windows-arm64.zip, wiliwili-Windows-x86-OldGPU.zip, wiliwili-Windows-x86.zip, wiliwili-Windows-x86_64-OldGPU.zip, wiliwili-Windows-x86_64.zip`.
- Repository archived: False; fork: False; pushed: 2026-10-31T14:00:15Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-04-25T07:39:58Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language zh; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["wiliwili v1.6.0", "wiliwili v1.5.3", "wiliwili v1.5.2"].

## 3. Checkpoint (`checkpoint`)

Save backups and restores.
- [Official repository / README](https://github.com/FlagBrew/Checkpoint); [native release feed](https://github.com/FlagBrew/Checkpoint/releases.atom); [release metadata](https://api.github.com/repos/FlagBrew/Checkpoint/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1, 3ds. Latest assets: `Checkpoint.3dsx, Checkpoint.3dsx.elf, Checkpoint.cia, Checkpoint.nro, Checkpoint.nro.elf`.
- Repository archived: False; fork: False; pushed: 2026-10-14T17:58:57Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-10-13T19:22:44Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["Checkpoint 5.3.0", "Checkpoint 5.2.0", "Checkpoint 5.1.0"].

## 4. Moonlight-Switch (`moonlight-switch`)

PC game streaming client.
- [Official repository / README](https://github.com/XITRIX/Moonlight-Switch); [native release feed](https://github.com/XITRIX/Moonlight-Switch/releases.atom); [release metadata](https://api.github.com/repos/XITRIX/Moonlight-Switch/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1, ios, macos. Latest assets: `Debug.elf, moonlight-app-release.apk, Moonlight-Switch.nro, Moonlight-windows-clangarm64.zip, Moonlight-windows-ucrt64.zip`.
- Repository archived: False; fork: False; pushed: 2026-07-26T19:39:26Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-05-24T20:04:16Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["1.5.0-2-ios", "1.5.0-ios", "Release v1.5.0"].

## 5. NX Activity Log (`nx-activity-log`)

Per-user playtime and session history.
- [Official repository / README](https://github.com/zdm65477730/NX-Activity-Log); [native release feed](https://github.com/zdm65477730/NX-Activity-Log/releases.atom); [release metadata](https://api.github.com/repos/zdm65477730/NX-Activity-Log/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `NX-Activity-Log.nro`.
- Repository archived: False; fork: True; pushed: 2026-10-19T13:39:58Z. Code license detected by GitHub: MIT; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-10-19T13:39:58Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["NX-Activity-Log v1.6.0", "NX-Activity-Log v1.5.9", "NX-Activity-Log v1.5.8"].
- This is the maintained zdm65477730 fork; upstream lineage is visible in repository metadata. Do not substitute the older original automatically.

## 6. SysDVR (`sysdvr`)

Stream supported Switch game video/audio over USB or network to a desktop/mobile client.
- [Official repository / README](https://github.com/exelix11/SysDVR); [native release feed](https://github.com/exelix11/SysDVR/releases.atom); [release metadata](https://api.github.com/repos/exelix11/SysDVR/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1, windows, macos, linux, android. Latest assets: `SysDVR-Client-Android.apk, SysDVR-Client-dotnet.zip, SysDVR-Client-Linux-x64.flatpak, SysDVR-Client-Windows-x64-with-framework.7z, SysDVR-USB-Only.zip, SysDVR.zip, SysDVRClient-MacOs-arm64.zip, SysDVRClient-MacOs-x64.zip`.
- Repository archived: False; fork: False; pushed: 2026-07-16T21:42:56Z. Code license detected by GitHub: GPL-2.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-02-10T21:15:07Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["Version 6.3", "Version 6.2.2", "Version 6.2.1"].
- README: fixed 720p30 capture, and normally requires games with video recording enabled; native client builds evidence host platforms, not Switch 2 support.

## 7. NXMP (`nxmp`)

Local and network video player using MPV.
- [Official repository / README](https://github.com/proconsule/nxmp); [native release feed](https://github.com/proconsule/nxmp/releases.atom); [release metadata](https://api.github.com/repos/proconsule/nxmp/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `nxmp-0.9.3.zip`.
- Repository archived: False; fork: False; pushed: 2026-08-29T06:59:46Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2025-12-17T09:24:48Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["NXMP 0.9.3", "NXMP 0.9.2", "NXMP 0.9.1"].

## 8. nx-ovlloader (`nx-ovlloader`)

Background loader for Ultrahand/Tesla overlays.
- [Official repository / README](https://github.com/ppkantorski/nx-ovlloader); [native release feed](https://github.com/ppkantorski/nx-ovlloader/releases.atom); [release metadata](https://api.github.com/repos/ppkantorski/nx-ovlloader/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `nx-ovlloader.zip`.
- Repository archived: False; fork: True; pushed: 2026-07-18T12:16:50Z. Code license detected by GitHub: ISC; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-07-17T21:54:18Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["nx-ovlloader v2.0.3", "nx-ovlloader v2.0.2", "nx-ovlloader v2.0.1"].
- Fork maintained by Ultrahand author; complements existing Ultrahand source but has a separate loader release stream.

## 9. nx-hbloader (`nx-hbloader`)

Core homebrew loader used by Switch homebrew launch setups.
- [Official repository / README](https://github.com/switchbrew/nx-hbloader); [native release feed](https://github.com/switchbrew/nx-hbloader/releases.atom); [release metadata](https://api.github.com/repos/switchbrew/nx-hbloader/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `hbl.nsp`.
- Repository archived: False; fork: False; pushed: 2025-11-15T16:49:59Z. Code license detected by GitHub: ISC; prose/images retain separate rights boundaries.
- Latest API app release published: 2025-11-15T16:51:11Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["nx-hbloader v2.4.5", "nx-hbloader v2.4.4", "nx-hbloader v2.4.3"].

## 10. Turnips (`turnips`)

Reads Animal Crossing New Horizons save data to display turnip prices.
- [Official repository / README](https://github.com/averne/Turnips); [native release feed](https://github.com/averne/Turnips/releases.atom); [release metadata](https://api.github.com/repos/averne/Turnips/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `Turnips-1.7.7-6c8fda4.zip`.
- Repository archived: False; fork: False; pushed: 2026-10-03T16:26:28Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2026-05-16T18:34:32Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["v1.7.7", "v1.7.6", "v1.7.5"].

## 11. NX-Shell (`nx-shell`)

File manager with copy/move/rename and image viewing.
- [Official repository / README](https://github.com/joel16/NX-Shell); [native release feed](https://github.com/joel16/NX-Shell/releases.atom); [release metadata](https://api.github.com/repos/joel16/NX-Shell/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `NX-Shell.nro`.
- Repository archived: False; fork: False; pushed: 2022-12-10T04:33:31Z. Code license detected by GitHub: GPL-2.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2022-08-07T18:32:20Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["NX-Shell v4.01", "NX-Shell v4.0.0", "NX-Shell (Next) v3.2.0"].
- Older release retained only for demonstrated utility; not described as recently released or verified on current firmware.

## 12. sys-con (`sys-con`)

Wired third-party game controller sysmodule.
- [Official repository / README](https://github.com/cathery/sys-con); [native release feed](https://github.com/cathery/sys-con/releases.atom); [release metadata](https://api.github.com/repos/cathery/sys-con/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `sys-con-0.6.5.zip`.
- Repository archived: False; fork: False; pushed: 2024-11-06T19:16:48Z. Code license detected by GitHub: GPL-3.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2024-11-06T19:16:48Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["0.6.5", "0.6.4", "0.6.3"].
- Older release retained only for demonstrated utility; not described as recently released or verified on current firmware.

## 13. Tesla-Menu (`tesla-menu`)

Menu for selecting installed overlay modules.
- [Official repository / README](https://github.com/WerWolv/Tesla-Menu); [native release feed](https://github.com/WerWolv/Tesla-Menu/releases.atom); [release metadata](https://api.github.com/repos/WerWolv/Tesla-Menu/releases?per_page=1).
- Runtime platforms evidenced by README installation/platform badges and release assets: switch1. Latest assets: `ovlmenu.zip`.
- Repository archived: False; fork: False; pushed: 2023-05-27T12:55:49Z. Code license detected by GitHub: GPL-2.0; prose/images retain separate rights boundaries.
- Latest API app release published: 2023-05-27T12:55:49Z; feed valid/nonempty: True. Observed script: no CJK observed; configured language en; title replacement characters 0; potentially truncated titles 0.
- Existing catalog repository duplicate: False. Feed title samples: ["libtelsa update", "Proper 16.0.0+ Support", "16.0.0 Support"].
- Older release retained only for demonstrated utility; not described as recently released or verified on current firmware.

## Rejected endpoints

ITotalJustice/All-in-One-Updater, averne/Linkalho, ndeadly/Triplayer: native release Atom HTTP 404 in this run. No candidate registration. User-cancelled gomprime/switchiptv were not probed or added.

## Scope and selection

13 valid practical candidates researched from 16 endpoint tests; root agent chooses within remaining catalog capacity. No catalog or app changes by this research task. Same-repository duplicates checked against current tools catalog; cross-source release URL overlap is zero because each candidate release URL has a distinct repository prefix. Semantically overlapping tools (Checkpoint versus JKSV, nx-ovlloader versus Ultrahand, NX-Shell versus sphaira) are complementary/alternative utilities, not duplicate feeds.
