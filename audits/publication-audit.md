# 2026-11-02 源扩展发布验收

## 实际收录

原有45源保留，新增43个不同订阅（工具21、游戏22），共88个可选源。主目录容量64，包含19个优先新增源；其余见独立用途/平台目录。新增源全部默认关闭，原有用户启停设置独立保留。不同语言或不同媒体的内容可能交叉报道；数量不是独家新闻数量。

- 工具扩展：Goldleaf、Fizeau、VitaDB、Apollo PS4/Vita、PS5 ELF Loader/websrv、XBSX2、ROCKNIX、PortMaster、Lemuroid、Decky Loader、ProtonUp-Qt、Heroic、AutoPlugin2、ftpd、uLaunch、emuiibo、Lutris、Cemu、Dolphin。
- 游戏扩展：Nintendo Life新闻/攻略/评测，Push Square新闻/补丁/PS Plus，Pure Xbox新闻/补丁/Game Pass，Gematsu，PC Gamer，PlayStation Universe，GNN/4Gamers中文新闻，Steam单游戏公告（Dota2、CS2、幻兽帕鲁、怪物猎人荒野、Terraria、无人深空、绝地潜兵2）。Steam提供的是该PC游戏的公告，不据此推断其他主机补丁同步。

## 验证边界

研究报告分别记录实际URL、HTTP、XML格式、最近日期、近7天条数、标题/摘要完整性、图片标记、语言观察、重复比例及许可限制，见[工具验收](tools-audit.md)与[游戏验收](games-audit.md)。本次43个新增源的样本都由BoleNews 0.1.2原生解析器读出非空内容；8个目录（主目录加7个可选目录）通过原生Storage目录验证；主目录通过旧版内置主机允许表验证，不需为读取它更换NRO。证据为parser-report.json和publication-report.json。仅单次主机软件/联网验收，不宣称长期稳定或真机验收。

## GNN JSON

[GNN官方RSS使用说明](https://user.gamer.com.tw/help/detail.php?sn=136)允许个人及非商业使用并要求标明出处、保持原链接。新增gnn.json只发布原始标题、原链接、来源和明确日期，共30条；不复制摘要、正文或图片。机器人规则本次允许该RSS路径。无日期保持空，不把采集时间作为新闻时间。其他媒体仅收录原生RSS地址，尤其Hookshot旗下站点不制作全文/图像镜像。公开Feed不等于取得商业再分发许可。

## 补充主目录的Steam与评测端点

|源|HTTP/条数|近7天|最近条目|摘要完整|图片标记|重复URL比例|
|---|---|---|---|---|---|---|
|[Dota 2 Steam](https://store.steampowered.com/feeds/news/app/570/?l=schinese)|200/10|0|2026-10-07T00:22:41+00:00|10/10|7/10|0.0|
|[CS2 Steam](https://store.steampowered.com/feeds/news/app/730/?l=schinese)|200/10|1|2026-10-28T21:48:09+00:00|10/10|0/10|0.0|
|[Palworld Steam](https://store.steampowered.com/feeds/news/app/1623730/?l=schinese)|200/10|1|2026-10-28T01:21:53+00:00|10/10|4/10|0.0|
|[Monster Hunter Wilds Steam](https://store.steampowered.com/feeds/news/app/2246340/?l=schinese)|200/10|1|2026-10-28T10:54:39+00:00|10/10|8/10|0.0|
|[Terraria Steam](https://store.steampowered.com/feeds/news/app/105600/?l=english)|200/10|1|2026-10-29T18:10:41+00:00|10/10|10/10|0.0|
|[Nintendo Life Reviews](https://www.nintendolife.com/feeds/reviews)|200/25|5|2026-10-28T14:00:00+00:00|25/25|25/25|0.0|

Steam订阅采用公开单游戏Feed，包含公告、活动、补丁等，不能把每条都标成版本更新。CS2的相同标题有多个不同公告URL，不能仅按标题删除。图片覆盖只表示Feed带有图像，不开启请求或复制图片。

## 已排除与拆分

排除旧域名TLS失败、返回HTML/403/404的端点；Homebrew App Store旧GitHub流和Adrenaline多年未发布，不作为新增持续更新来源。移除Palworld/MHWilds/Terraria重复语言端点，保留已验证的首选版本。仍保留CS2中英文双语Feed，按语言偏好选择。所有工具平台表示运行平台，不是模拟目标；ROCKNIX/PortMaster标linux，未伪装成Switch软件。当前应用若没有Linux专属筛选，可从掌机目录启用并在全部内容查看。

## 可选目录

每个文件是可直接添加的平面目录，无嵌套目录、脚本或自动安装功能。选择适合自己的目录即可，不必把所有目录同时导入；重叠目录可能重复请求同一个RSS。
- [android（4源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/android.json)
- [games（38源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/games.json)
- [pc-handheld（40源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/pc-handheld.json)
- [playstation（33源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/playstation.json)
- [switch（40源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/switch.json)
- [tools（50源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/tools.json)
- [xbox（23源）](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/xbox.json)
