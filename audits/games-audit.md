# 游戏来源扩展验收（2026-11-02）

## 结论

探测 42 个实际端点，选出 19 个优先候选；新增源均建议默认关闭，由用户开启。原始响应保存在本目录 raw/，不随公开数据仓库分发。单次 HTTP200/XML 合法不等于长期稳定。

覆盖方向：Switch/Switch2新游和攻略、PS4/PS5与Xbox补丁、PS Plus/Game Pass活动、跨平台发售资讯，以及PC版游戏开发者公告。中文补充为GNN/4Gamers繁体中文和3款Steam官方简体中文；不把繁体称简体，不把PC版补丁称为Switch可用更新。Vita暂无经此次验证的高频新游聚合源，保留现有生态及官方工具源，不能假称全平台同等覆盖。

## 验收表

|优先级|源 / 实际 URL|语言 / 默认平台|HTTP / 合法格式|条数 / 近7天|最新UTC|标题 / 摘要 / 图片非空|站内重复标题率|
|---|---|---|---|---|---|---|---|
|1|[巴哈姆特 GNN 游戏新闻](https://gnn.gamer.com.tw/rss.xml)|zh-Hant / 逐条识别|200 / rss|30 / 30|2026-11-02T04:41:49+00:00|30 / 30 / 0|0.0%|
|2|[4Gamers 游戏新闻](https://www.4gamers.com.tw/rss/latest-news)|zh-Hant / 逐条识别|200 / rss|50 / 50|2026-11-02T04:48:48+00:00|50 / 50 / 50|0.0%|
|3|[Nintendo Life 新游与新闻](https://www.nintendolife.com/feeds/news)|en / switch1,switch2|200 / rss|20 / 20|2026-11-02T03:30:00+00:00|20 / 20 / 20|0.0%|
|4|[Nintendo Life 攻略](https://www.nintendolife.com/feeds/guides)|en / switch1,switch2|200 / rss|20 / 9|2026-11-01T14:00:00+00:00|20 / 20 / 20|0.0%|
|5|[Push Square PlayStation 新闻](https://www.pushsquare.com/feeds/news)|en / ps4,ps5|200 / rss|20 / 20|2026-11-02T00:00:00+00:00|20 / 20 / 20|0.0%|
|6|[Push Square 游戏补丁](https://www.pushsquare.com/feeds/latest/tags/updates)|en / ps4,ps5|200 / rss|25 / 4|2026-11-01T13:30:00+00:00|25 / 25 / 25|0.0%|
|7|[Pure Xbox 新游与新闻](https://www.purexbox.com/feeds/news)|en / xbox|200 / rss|20 / 20|2026-11-01T16:00:00+00:00|20 / 20 / 20|0.0%|
|8|[Pure Xbox 游戏补丁](https://www.purexbox.com/feeds/latest/tags/updates)|en / xbox|200 / rss|25 / 3|2026-10-29T18:00:00+00:00|25 / 25 / 25|0.0%|
|9|[Gematsu 多平台新游](https://www.gematsu.com/feed)|en / 逐条识别|200 / rss|20 / 20|2026-11-02T03:16:59+00:00|20 / 20 / 20|0.0%|
|10|[PC Gamer 游戏新闻](https://www.pcgamer.com/rss/)|en / pc|200 / rss|50 / 50|2026-11-02T04:12:30+00:00|50 / 50 / 50|0.0%|
|11|[PlayStation Universe](https://www.psu.com/feed/)|en / ps4,ps5|200 / rss|10 / 10|2026-11-02T03:55:44+00:00|10 / 10 / 0|0.0%|
|12|[Counter-Strike 2 官方动态](https://steamcommunity.com/games/CSGO/rss/)|en / pc|200 / rss|10 / 1|2026-10-28T21:48:09+00:00|10 / 10 / 0|90.0%|
|13|[幻兽帕鲁 Steam 官方中文](https://steamcommunity.com/games/1623730/rss/?l=schinese)|zh-Hans / pc|200 / rss|10 / 1|2026-10-28T01:21:53+00:00|10 / 10 / 4|0.0%|
|14|[怪物猎人 荒野 Steam 官方中文](https://steamcommunity.com/games/2246340/rss/?l=schinese)|zh-Hans / pc|200 / rss|10 / 1|2026-10-28T10:54:39+00:00|10 / 10 / 7|0.0%|
|15|[绝地潜兵2 Steam 官方中文](https://steamcommunity.com/games/553850/rss/?l=schinese)|zh-Hans / pc|200 / rss|10 / 1|2026-10-29T10:00:06+00:00|10 / 10 / 6|0.0%|
|16|[No Man’s Sky Steam 官方动态](https://steamcommunity.com/games/275850/rss/)|en / pc|200 / rss|10 / 1|2026-10-28T14:05:37+00:00|10 / 10 / 10|0.0%|
|17|[Terraria Steam 官方动态](https://steamcommunity.com/games/105600/rss/)|en / pc|200 / rss|10 / 1|2026-10-29T18:10:41+00:00|10 / 10 / 10|0.0%|
|18|[Push Square PS Plus](https://www.pushsquare.com/feeds/latest/tags/ps-plus)|en / ps4,ps5|200 / rss|25 / 3|2026-10-31T18:00:00+00:00|25 / 25 / 25|0.0%|
|19|[Pure Xbox Game Pass](https://www.purexbox.com/feeds/latest/tags/xbox-game-pass)|en / xbox,pc|200 / rss|25 / 8|2026-10-31T14:30:00+00:00|25 / 25 / 25|0.0%|

近7天按探测时间UTC向前计算；图片覆盖是Feed字段出现情况，所有候选images=false，未下载图片。摘要非空只说明Feed提供文字，不保证新闻全文完整。标题截断、替换字符、日期可解析度、URL去重率、跨端点重复率见 games-candidates.json。Steam中文版和英文版可能使用同一公告URL，应在同一聚合中优先目标语言而不是重复展示。

## 平台与可信度

- [Gematsu官网](https://www.gematsu.com/) 自身按Nintendo、PlayStation、Xbox、PC列出新闻；其总Feed保持空默认平台，按每篇标题/源标签识别。
- [Push Square介绍](https://www.pushsquare.com/contact)定位PlayStation；[Pure Xbox介绍](https://www.purexbox.com/contact)定位Xbox。源的主平台不意味着每篇跨平台作品只在该平台发售。
- [Palworld官方Steam页面](https://store.steampowered.com/app/1623730/Palworld/)给出游戏身份、开发/发行方；其社区RSS为开发者公告，保留PC标记。Monster Hunter Wilds app2246340、Helldivers2 app553850、No Man’s Sky app275850、Terraria app105600、CS2官方slug CSGO均以实际Feed标题校验身份。
- 三款简体Steam RSS使用?l=schinese，实测标题有中文；Terraria该参数仍返回英文，因此未把它标为中文。官方公告包含促销、投票、公告，也并非每条都是补丁，需逐条识别game_update标签。

## 许可与使用限制

- [Nintendo Life条款](https://www.nintendolife.com/terms)、[Push Square条款](https://www.pushsquare.com/terms)、[Pure Xbox条款](https://www.purexbox.com/terms)允许个人本地用途，同时保留对再发布、站外存储的控制；不能因为有RSS就镜像全文/摘要/图片。建议这些源直接订阅；若需要公开JSON，先限标题+原链接并复核授权，不把宽泛转载权限标为已取得。其[联系页](https://www.purexbox.com/contact)主动推荐RSS用于链接最新文章。
- [Gematsu页脚](https://www.gematsu.com/follow)明确保留版权并要求来源标注，不等于无限全文复制许可。GNN的[官方RSS帮助](https://user.gamer.com.tw/help/detail.php?sn=136)说明订阅阅读用途；本次未获得GNN、4Gamers或其他媒体的图片/全文再分发授权。
- Steam官方公开公告也是受权利保护内容。订阅索引只收元数据和原链接，不收游戏文件、网盘地址、文章图像或整篇正文，不能把“公开可读”视为所有再利用均已获许可。

## 未通过或不推荐默认收录

|端点|结果|原因|
|---|---|---|
|[siliconera](https://www.siliconera.com/feed/)|403|HTTPError: HTTP Error 403: Forbidden|
|[automaton-zh](https://automaton-media.com/zh/feed/)|200|ValueError: DTD/entity declarations rejected|
|[gamersky-rss](https://www.gamersky.com/news/rss.xml)|404|HTTPError: HTTP Error 404: Not Found|
|[3dm-rss](https://www.3dmgame.com/rss/news.xml)|404|HTTPError: HTTP Error 404: Not Found|
|[epic-news](https://store.epicgames.com/en-US/news/rss)|403|HTTPError: HTTP Error 403: Forbidden|
|[gog-news](https://www.gog.com/news/rss)|200|ValueError: DTD/entity declarations rejected|
|[cs2-steam](https://steamcommunity.com/games/730/rss/)|200|ValueError: DTD/entity declarations rejected|
|[dota2-steam](https://steamcommunity.com/games/570/rss/)|200|ValueError: DTD/entity declarations rejected|

- CS2/Dota2数字社区路径返回HTML，换官方CSGO/dota2 slug后才通过；Steam商店同游戏端点和这些社区端点内容重复，不重复收录。
- GNN `?k=11`与总Feed本次条目相同，不能将该参数当Switch分类接口。
- Stardew Valley、Silksong、Baldur’s Gate3为合法非空RSS但近期无更新，列在额外候选而不是当作“最新更新充足”的证据。
- Rock Paper Shotgun、VGC、GameSpot、AUTOMATON WEST均有合法近期Feed，但与优先媒体角色重叠，留作扩展，不用数量掩盖重复。

## 建议接入方式

保留RSS直接阅读，并将候选列表或按平台拆分的目录发布为数据配置；一条目录最多64个子源，当前45个，工具扩展同时加入时应按平台/用途分目录或选择Top候选。若将无RSS网页或获准的Feed元数据转换JSON，输出必须包含原来源和原文链接，标题日期未知保持空、单源失败保留旧数据；不要复制Feed HTML至公开存储。

本报告只写本次研究目录，不修改BoleNews应用、默认目录或任何线上仓库。
