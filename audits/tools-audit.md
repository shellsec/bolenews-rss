# 工具 / Homebrew / 模拟器新增源验收（2026-11-02）

本轮对23个未在当前45源目录中的官方项目Release Atom进行了实际HTTPS读取：23个返回200、XML合法且非空。仅代表本次网络观察，不代表长期稳定、Switch真机兼容性或全部固件适配。没有下载发布附件、商业游戏、文章图片，也没有执行安装或更新。

机器结果及完整Source对象见 [tools-candidates.json](tools-candidates.json)，复验脚本为 [probe-tools.py](probe-tools.py)，原始Feed保留本地 `raw/` 供解析回放，不作为新闻全文打包发布。

## 主目录优先10项

现有27个项目源之外，优先填补Vita、Xbox、Linux掌机及Android空白，并补Switch实用工具。以下所有新增源建议 `enabled:false`，由用户更新目录后自行开启。源证据标为 `upstream`：表示发布者自己的更新说明，不能扩大为“所有功能或漏洞已经独立验证”。

| 项目 / 原生Atom | 运行平台 | 条目 | 最新发布日期（北京时间） | 近7天 | 标题 / 摘要完整数 | 可检测图片 / 非头像内联图 | 重复标题 / URL |
|---|---|---:|---|---:|---|---|---|
| [Goldleaf](https://github.com/XorTroll/Goldleaf/releases.atom) | switch1 | 10 | 2026-09-23 02:32 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [VitaDB Downloader](https://github.com/Rinnegatamante/VitaDB-Downloader/releases.atom) | vita | 10 | 2026-10-26 07:38 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [Apollo Save Tool (PS4)](https://github.com/bucanero/apollo-ps4/releases.atom) | ps4 | 10 | 2026-10-17 20:09 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [PS5 ELF Loader](https://github.com/ps5-payload-dev/elfldr/releases.atom) | ps5 | 10 | 2026-10-22 01:44 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [XBSX2](https://github.com/XboxEmulationHub/XBSX2/releases.atom) | xbox | 4 | 2026-10-20 23:04 | 0 | 4/4 · 4/4 | 4 / 0 | 0% / 0% |
| [ROCKNIX](https://github.com/ROCKNIX/distribution/releases.atom) | linux | 10 | 2026-11-01 22:29 | 1 | 10/10 · 10/10 | 10 / 7 | 0% / 0% |
| [PortMaster](https://github.com/PortsMaster/PortMaster-GUI/releases.atom) | linux | 10 | 2026-11-02 12:35 | 3 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [Lemuroid](https://github.com/Swordfish90/Lemuroid/releases.atom) | android | 10 | 2026-05-31 16:26 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader/releases.atom) | pc, linux | 10 | 2026-10-27 12:26 | 2 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |
| [Fizeau](https://github.com/averne/Fizeau/releases.atom) | switch1 | 10 | 2026-08-08 03:37 | 0 | 10/10 · 10/10 | 10 / 0 | 0% / 0% |

图片数量是Feed中可识别的图像标记，不代表新闻配图覆盖；GitHub Atom通常含发布者头像，不能以此宣称文章均有配图。所有Source `images:false`。摘要计数仅检查清理HTML后非空，不保证更新日志详尽。发布日期采用条目published，缺少才取updated；不能用采集时间冒充发布。英文为主要内容语言，部分作者可能混用中文；观察脚本信息、字符替换和疑似截断数量记录在JSON。

## 平台与功能依据（官方项目）

- [Goldleaf](https://github.com/XorTroll/Goldleaf)：Switch content and file manager; metadata only, no installation executed. 代码许可证本次检测：[AGPL](https://raw.githubusercontent.com/XorTroll/Goldleaf/HEAD/LICENSE)。
- [VitaDB Downloader](https://github.com/Rinnegatamante/VitaDB-Downloader)：Official VitaDB client for PSVita/PSTV. 代码许可证本次检测：[AGPL](https://raw.githubusercontent.com/Rinnegatamante/VitaDB-Downloader/HEAD/LICENSE)。
- [Apollo Save Tool (PS4)](https://github.com/bucanero/apollo-ps4)：PS4 save-game management tool; not game-content downloads. 代码许可证本次检测：[AGPL](https://raw.githubusercontent.com/bucanero/apollo-ps4/HEAD/LICENSE)。
- [PS5 ELF Loader](https://github.com/ps5-payload-dev/elfldr)：ELF loader for already-compatible PS5 homebrew environments; no universal firmware support implied. 代码许可证本次检测：[AGPL](https://raw.githubusercontent.com/ps5-payload-dev/elfldr/HEAD/LICENSE)。
- [XBSX2](https://github.com/XboxEmulationHub/XBSX2)：PS2 emulator running on Xbox One/Series UWP; this is runtime Xbox, not PC Xenia. 代码许可证本次检测：[本次未确认](https://raw.githubusercontent.com/XboxEmulationHub/XBSX2/HEAD/LICENSE)。
- [ROCKNIX](https://github.com/ROCKNIX/distribution)：Linux handheld OS releases, device-specific images; not Switch firmware. 代码许可证本次检测：[project licence text; inspect upstream](https://raw.githubusercontent.com/ROCKNIX/distribution/HEAD/LICENSE.md)。
- [PortMaster](https://github.com/PortsMaster/PortMaster-GUI)：Port manager for supported ARM Linux handhelds; game asset licences remain per-port. 代码许可证本次检测：[MIT](https://raw.githubusercontent.com/PortsMaster/PortMaster-GUI/HEAD/LICENSE)。
- [Lemuroid](https://github.com/Swordfish90/Lemuroid)：Libretro-based Android emulator frontend. 代码许可证本次检测：[本次未确认](https://raw.githubusercontent.com/Swordfish90/Lemuroid/HEAD/LICENSE)。
- [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader)：Steam Deck/Linux plugin loader; not Switch software. 代码许可证本次检测：[LGPL](https://raw.githubusercontent.com/SteamDeckHomebrew/decky-loader/HEAD/LICENSE)。
- [Fizeau](https://github.com/averne/Fizeau)：Switch display colour adjustment utility. 代码许可证本次检测：[LGPL](https://raw.githubusercontent.com/averne/Fizeau/HEAD/LICENSE)。

附加交叉核验：ROCKNIX官方[Ports说明](https://rocknix.org/systems/ports/)确认PortMaster针对ARM掌机，官方[安装文档](https://portmaster.games/installation.html)列出支持环境；XboxEmulationHub的[XBSX2说明](https://github.com/XboxEmulationHub/XBSX2)明确Xbox One/Series，不能把PC端PCSX2或Xenia当作Xbox可运行版本。没有新加入Switch 2工具源，因为本轮未取得对应开发者正式运行兼容性证据。

## 保留候选及低活跃源

| 项目 / 官方页面 | 平台 | Atom条目 | 最新日期UTC | 处理 |
|---|---|---:|---|---|
| [Homebrew App Store](https://github.com/fortheusers/hb-appstore) | switch1 | 9 | 2023-03-23 | 不进新增更新清单：长期无新Release |
| [ProtonUp-Qt](https://github.com/DavidoTek/ProtonUp-Qt) | pc, linux | 10 | 2026-10-11 | 已验证，供平台独立可选目录使用 |
| [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) | pc, linux | 10 | 2026-10-15 | 已验证，供平台独立可选目录使用 |
| [AutoPlugin II](https://github.com/ONElua/AutoPlugin2) | vita | 10 | 2026-08-16 | 已验证，供平台独立可选目录使用 |
| [Apollo Save Tool (Vita)](https://github.com/bucanero/apollo-vita) | vita | 10 | 2026-10-17 | 已验证，供平台独立可选目录使用 |
| [PS5 websrv](https://github.com/ps5-payload-dev/websrv) | ps5 | 10 | 2026-10-10 | 已验证，供平台独立可选目录使用 |
| [ftpd](https://github.com/mtheall/ftpd) | switch1 | 10 | 2025-11-19 | 已验证，供平台独立可选目录使用 |
| [uLaunch](https://github.com/XorTroll/uLaunch) | switch1 | 10 | 2026-07-24 | 已验证，供平台独立可选目录使用 |
| [emuiibo](https://github.com/XorTroll/emuiibo) | switch1 | 10 | 2026-03-14 | 已验证，供平台独立可选目录使用 |
| [Adrenaline](https://github.com/TheOfficialFloW/Adrenaline) | vita | 10 | 2020-09-23 | 不进新增更新清单：长期无新Release |
| [Lutris](https://github.com/lutris/lutris) | pc, linux | 10 | 2026-02-26 | 已验证，供平台独立可选目录使用 |
| [Cemu](https://github.com/cemu-project/Cemu) | pc, linux | 10 | 2026-05-12 | 已验证，供平台独立可选目录使用 |
| [Dolphin](https://github.com/dolphin-emu/dolphin) | pc, linux, android | 10 | 2026-10-08 | 已验证，供平台独立可选目录使用 |

Homebrew App Store的[上游Release说明](https://github.com/fortheusers/hb-appstore/releases)提到迁移GitLab；GitHub Atom最新观察仍是2023年，不应把旧流当持续更新源。Adrenaline的最后观察Release为2020年，不能伪装为新发布。有效但低频的Lemuroid（2026年5月）保留为Android工具覆盖，不宣称最近7天有更新。

## 许可与使用边界

- 这里只添加开发者公开Atom端点和官方项目链接，不复制项目代码、预编译程序或游戏文件；代码许可证与Release说明/图像的再分发许可是不同问题。
- 已逐项目探测公开LICENSE路径，结果在JSON；17项取得许可证文本，其余明确记录未确认，不推断许可。任何源码组合/二进制再分发须单独按项目许可处理。
- 客户端直接个人阅读Release Feed，`fullContent:true`仅沿用既有官方项目更新日志能力，`images:false`。不把这些上游更新日志同步为公共镜像全文。
- 主目录容量按当前客户端单目录64源约束选择10项，其他11项可放单独平台可选目录；排除两项长期无新Release的源。新源默认关闭，用户启停选择与已有源分别存储。
- 同一项目各Release URL本次无重复；所有候选与现有源仓库路径去重检查通过。平台指软件运行环境，不是它所模拟的主机。

## 本次验收结论

通过的是可访问性、格式、条目、时间、标题/摘要、图像标记、语言观察与Feed内部重复检查；并非“稳定可用”保证。一次性4并发验证，启用后仍需客户端超时、重试、源隔离与本地缓存。未请求RSSHub或付费/登录接口，没有API Key要求。
