# 2026-11-02 实用工具源补充验收

新增16个不同项目，均使用原生GitHub Releases Atom直接订阅。精选工具目录由52增加到64；其余4项同时提供工具补充目录，并加入对应平台目录。所有新增默认关闭，不改旧源及本地开关。主目录仍v4/64项，现有NRO不需要重编。

## 本轮收录

|项目|用途/收录依据|目录|
|---|---|---|
|[Switchfin（Jellyfin客户端，含依赖发布）](https://github.com/dragonflylee/switchfin)|Jellyfin客户端；Feed含应用与依赖包发布，最近编辑不是新版应用的证明|工具精选及平台|
|[wiliwili（哔哩哔哩客户端）](https://github.com/xfangfang/wiliwili)|哔哩哔哩客户端；发布内容含中文，按简体中文标记|工具精选及平台|
|[Checkpoint（存档备份）](https://github.com/FlagBrew/Checkpoint)|存档备份；本目录只标当前客户端支持的Switch运行标签，项目另有3DS版本|工具精选及平台|
|[Moonlight-Switch（串流客户端）](https://github.com/XITRIX/Moonlight-Switch)|串流客户端；已核对README和实际NRO/APK/Windows资产，Apple目标与Linux构建有上游说明|工具精选及平台|
|[NX Activity Log（维护分支，游玩统计）](https://github.com/zdm65477730/NX-Activity-Log)|zdm65477730维护分支，游玩统计；不冒充旧原仓库|工具精选及平台|
|[SysDVR（Switch画面串流及客户端）](https://github.com/exelix11/SysDVR)|Switch采集端及桌面/Android客户端，不能把客户端与采集端混同|工具精选及平台|
|[NXMP（视频播放器）](https://github.com/proconsule/nxmp)|视频播放器，Release较低频，2026年仍有代码活动|工具精选及平台|
|[nx-ovlloader（ppkantorski维护分支）](https://github.com/ppkantorski/nx-ovlloader)|ppkantorski维护分支，Ultrahand/Tesla覆盖层载入器|工具精选及平台|
|[nx-hbloader（Homebrew载入器）](https://github.com/switchbrew/nx-hbloader)|Switch底层Homebrew载入器，低频基础工具|工具补充及平台|
|[Turnips（动森大头菜辅助）](https://github.com/averne/Turnips)|动森大头菜价格辅助，游戏专用工具|工具补充及平台|
|[Sunshine（串流主机端，含开发构建）](https://github.com/LizardByte/Sunshine)|串流主机端，含频繁开发构建，按上游发布事实阅读|工具精选及平台|
|[chiaki-ng（PS远程串流客户端，含Canary）](https://github.com/chiaki-ng/chiaki-ng)|PS远程串流的桌面客户端；含Canary，不标成PS4/PS5本机软件|工具精选及平台|
|[RetroFlow Launcher（Vita前端）](https://github.com/jimbob4000/RetroFlow-Launcher)|Vita前端，规范仓库jimbob4000/RetroFlow-Launcher|工具精选及平台|
|[Moonlight Qt（桌面串流客户端）](https://github.com/moonlight-stream/moonlight-qt)|桌面串流客户端，与Sunshine主机端角色不同|工具精选及平台|
|[VitaDeploy（Vita工具箱）](https://github.com/SKGleba/VitaDeploy)|Vita工具箱，较低频实用项，不宣称最近新发版|工具补充及平台|
|[Itemzflow（PS4/PS5管理，含开发更新）](https://github.com/LightningMods/Itemzflow)|PS4/PS5管理；最近记录含开发更新，无当前二进制资产保证|工具补充及平台|

## 验证与边界

- 16个Atom端点实际HTTP200、合法XML且非空；原始指标见[Switch验收](tool-refresh-switch.md)和[其他平台验收](tool-refresh-multiplatform.md)，涵盖最近时间/近7天、标题摘要、图像标记、语言、重复率、维护与许可。
- 当前0.1.4原生解析器读出16份非空内容，运行平台保持精确声明；7份变化目录通过Storage集合校验，证据见tool-refresh-parser.json。
- Source平台名统一windows→pc、psvita→vita；保守保留当前内容平台词表，不把模拟/串流目标当作软件运行平台。多组件项目按上游文档标记范围，不构成每个Release资产或固件兼容保证。
- Atom updated可能是编辑；尤其Switchfin最近编辑含依赖包，不写成近期新版本。Sunshine频繁构建、chiaki-ng Canary状态按上游保留，不保证全部为稳定版。API配额不足时不绕过限制，以Atom及官网证据验收。
- 已归档GoldHEN Cheat Manager排除；旧NX-Shell、sys-con、Tesla-Menu未加入本轮，避免与更新更近的工具重复。VitaDeploy按低频实用项目记录。
- 用户询问的Sphaira原已在内置源且默认启用，保留用户开关，不重复收录。误发的gomprime/switchiptv按用户要求不添加。
- 此次只发布源地址与审计元数据，不镜像安装包、游戏、频道、播放列表、文章全文或图片；代码许可证不等于这些内容的再分发授权。
- 单次网络和解析观察，不构成长期稳定或真机验收。

## 远程目录

|目录|版本|数量|
|---|---:|---:|
|[tools](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/tools.json)|7|64|
|[switch](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/switch.json)|7|52|
|[playstation](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/playstation.json)|6|39|
|[pc-handheld](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/pc-handheld.json)|5|47|
|[android](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/android.json)|5|7|
|[apple](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/apple.json)|3|9|
|[tools-extra](https://raw.githubusercontent.com/shellsec/bolenews-rss/master/catalogs/tools-extra.json)|1|4|

每份都是平面目录，无嵌套；优先选择对应平台或工具精选即可，重叠目录可能重复请求同一Feed。工具精选达到64项后，补充项保留在平台目录和tools-extra.json，不删用户已有条目。
