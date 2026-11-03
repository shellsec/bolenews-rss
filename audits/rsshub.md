# RSSHub 实例与游戏路由验收（2026-11-03）

范围：用户提供四个实例，47 次有界请求，实际 HTTP/XML 验证。原始响应仅本地研究，不随产品分发。一次成功不代表长期稳定；超时/503仅说明本次测试失败。未根据旧实例列表确认服务器地理位置或维护者身份。

## 四个实例（各六条相同路由）

| 实例 | 有效非空订阅 | 本轮观察 |
|---|---:|---|
| rsshub.rssforever.com | 1/6 | The read operation timed out; 成功 |
| hub.slarker.me | 1/6 | The read operation timed out; 成功 |
| rsshub.ktachibana.party | 5/6 | HTTP Error 503: Service Unavailable; 成功 |
| rsshub.isrss.com | 5/6 | HTTP Error 503: Service Unavailable; 成功 |

## 有效路由与内容指标

数量来自返回窗口，非全站总量。近7天忽略未来时间；无时间不是0条更新，而是无法统计。图片仅检测HTML img/媒体字段，不证明图片链接可加载或有再分发许可。标题重复率不是文章重复率（例如多次 Steam 更新同名）。

| URL | 条数 | 近7天 | 有图片条数 | 最新源时间 UTC |
|---|---:|---:|---:|---|
| https://rsshub.rssforever.com/nintendo/direct | 18 | 1 | 18 | 2026-10-31T07:00:00+00:00 |
| https://hub.slarker.me/3dmgame/news/game | 20 | 20 | 19 | 2026-11-03T08:01:27+00:00 |
| https://rsshub.ktachibana.party/nintendo/direct | 18 | 1 | 18 | 2026-10-31T07:00:00+00:00 |
| https://rsshub.ktachibana.party/nintendo/system-update | 81 | 0 | 0 | 2026-09-30T15:00:00+00:00 |
| https://rsshub.ktachibana.party/3dmgame/news/game | 20 | 20 | 19 | 2026-11-03T08:01:27+00:00 |
| https://rsshub.ktachibana.party/epicgames/freegames/zh-CN/CN | 1 | 1 | 1 | 2026-10-29T15:00:00+00:00 |
| https://rsshub.ktachibana.party/jump/discount/switch/all | 10 | 未知 | 10 | 无 |
| https://rsshub.isrss.com/nintendo/news | 24 | 7 | 24 | 2026-11-03T15:00:00+00:00 |
| https://rsshub.isrss.com/nintendo/direct | 18 | 1 | 18 | 2026-10-31T07:00:00+00:00 |
| https://rsshub.isrss.com/3dmgame/news/game | 20 | 20 | 19 | 2026-11-03T08:15:21+00:00 |
| https://rsshub.isrss.com/epicgames/freegames/zh-CN/CN | 1 | 1 | 1 | 2026-10-29T15:00:00+00:00 |
| https://rsshub.isrss.com/jump/discount/switch/all | 10 | 未知 | 10 | 无 |
| https://rsshub.ktachibana.party/gamersky/news/ns | 20 | 20 | 20 | 2026-11-03T07:50:00+00:00 |
| https://rsshub.ktachibana.party/ps/monthly-games | 3 | 未知 | 3 | 无 |
| https://rsshub.ktachibana.party/steam/news/730/schinese | 100 | 1 | 23 | 2026-10-28T21:48:09+00:00 |
| https://rsshub.isrss.com/gamersky/news/ns | 20 | 20 | 20 | 2026-11-03T07:50:00+00:00 |
| https://rsshub.isrss.com/ps/monthly-games | 3 | 未知 | 3 | 无 |
| https://rsshub.isrss.com/steam/news/730/schinese | 100 | 1 | 23 | 2026-10-28T21:48:09+00:00 |
| https://rsshub.isrss.com/a9vg/news | 15 | 13 | 15 | 2026-11-03T02:06:00+00:00 |
| https://rsshub.isrss.com/tgbus/list/news | 20 | 10 | 15 | 2026-11-03T07:43:00+00:00 |
| https://rsshub.isrss.com/diershoubing/news | 20 | 20 | 20 | 2026-11-03T07:55:00+00:00 |
| https://rsshub.isrss.com/gcores/news | 30 | 30 | 26 | 2026-11-03T05:58:13+00:00 |
| https://rsshub.isrss.com/yystv/docs | 12 | 12 | 12 | 2026-11-01T08:26:08+00:00 |
| https://rsshub.isrss.com/indienova/article | 12 | 6 | 12 | 2026-10-30T16:00:00+00:00 |
| https://rsshub.isrss.com/steam/news/730/english | 100 | 1 | 23 | 2026-10-28T21:48:09+00:00 |
| https://rsshub.isrss.com/epicgames/freegames/en-US/US | 1 | 1 | 1 | 2026-10-29T15:00:00+00:00 |

## 接入结论

- 最有补充价值：游民 Switch `/gamersky/news/ns`、电玩巴士 `/tgbus/list/news`、第二手柄 `/diershoubing/news`、任天堂香港 `/nintendo/news`、Direct `/nintendo/direct`、Epic 中英文免费活动。isRSS 本次返回有效内容。
- PS会免 `/ps/monthly-games`、Jump Switch折扣 `/jump/discount/switch/all` 返回有图内容，但缺日期，应展示为活动/价格列表，不能伪造发布时间；PS会免当期仍需比对官方公告。
- Steam `/steam/news/730/schinese` 和 `/english` 都返回100条；730只是CS2，不代表全部Steam游戏。语言参数不保证上游提供中文，实际标题仍可能英文。不应把schinese参数当实际中文验证。优先官方原生 https://store.steampowered.com/feeds/news/app/730/?l=schinese 。
- 任天堂系统更新 `/nintendo/system-update` 在KTachibana可解析81条，最近为9月30日UTC，近7天0；这是原Switch日本支持页，不据此认定Switch2固件覆盖。
- 机核、游研社、indienova、A9VG已有内容来源，不因更换实例重复添加；已有原生RSS优先。
- 任天堂eshop港服两实例503；游民PS5 `/gamersky/news/ps5` 本次503，不能标为已验收可用。
- KTachibana后续出现429，不继续重试；后续研究脚本遇429应停止该实例并尊重Retry-After。当前批次并非长期可用性测试。
- RSSHub是转换服务，不是新增版权授权。仅确定可读取，不承诺全文、图片的公开转载权限；未审核条款前不镜像全文与图片。
- Homebrew和工具继续使用项目原生GitHub Atom。游戏破解、固件兼容性、模拟器新闻中的传闻不能因为出现在RSS就标为已验证；需回查开发者与官方公告。
- 推荐按内容源选一个已验证URL，其他实例作为人工候选，不把同内容的四个实例都加入列表制造重复。当前客户端可配置RSSHub基地址，未实现按路由自动跨实例容灾，不宣称已有。
- 后续用户授权更新：新增8个默认关闭源，更新5个平面目录；主目录64项保持不变，不改变已有用户开关或应用/NRO。来源内容通过RSSHub直读，不在源仓库镜像文章或图片。详见selected-sources.json和rsshub-parser.json。

## 一手参考

- 官方源代码：https://github.com/DIYgod/RSSHub/tree/master/lib/routes
- 游戏路由文档：https://rsshub.netlify.app/routes/game
- 各URL的HTTP状态、时间、标题摘要完整度、图片检测、标题重复率详见 instance-results.json / route-results.json / english-platform-results.json；源码路由与局限详见 routes.md。

## 发布选源

8个新源：任天堂香港（繁中）、Nintendo Direct（英文）、游民Switch（简中）、3DM（简中）、电玩巴士（简中）、二柄（简中）、Epic中文/中国区、Epic英文/美国区。全部使用本轮通过的isRSS地址，默认关闭，images/fullContent=false。Nintendo Direct源为英文，不是日语。

- games.json: v6, 47项，新增8项。
- switch.json: v8, 58项，新增6项。
- pc-handheld.json: v6, 52项，新增5项。
- playstation.json: v7, 42项，新增3项。
- xbox.json: v5, 26项，新增3项。

主目录已64项，不扩容；现有用户刷新对应平台目录或游戏目录后自行开启。未提供实例自动容灾承诺。
