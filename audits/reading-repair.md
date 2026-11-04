# 全源阅读内容与退出确认修复（2026-11-04）

## 问题与修复

此前6个JSON适配器主动将summary置空，即使WordPress公开excerpt和HTML description可用也丢弃，造成用户只能看到标题。现取公开WordPress excerpt、RSS description、HTML description/og:description，去除脚本/样式/HTML后最多240字符（截断标记可多1字符）。不获取或镜像文章完整正文、发布方图片、下载地址和游戏文件。protected excerpt不读取；文章页面只提取meta简介，不提取正文段落。沿用HTTPS、固定来源主机、robots检查、2MiB、超时和拒绝跨站跳转。

默认每源每轮最多12个缺失简介请求，已缓存且标题/修改时间不变则复用；记录summary_count/summary_missing/errors。初始化补采用100请求上限完成当前窗口。403/401/429停止该源后续简介请求，不能绕过限制。

原生阅读器对任意RSS/Atom/JSON的标题条目，在用户打开详情时单独异步读取原文公开meta简介，并写入缓存。仅HTTPS公网地址，沿用原网络层TLS/IP固定连接/重定向校验及2MiB限制。一次只执行一个详情请求，返回/休眠/退出取消；正文不执行脚本。刷新不会覆盖同标题、同时间的缓存简介，已变动条目不沿用过期简介。Web增加同源/api/description，采用现有公网IP固定连接网关并缓存简介。

## B键问题

根因是主界面/侧栏B键分支和设置退出选项直接running_=false，并非已证实的崩溃。现显示是否退出弹窗，默认取消，左=取消、右=退出，B取消，A执行当前选择，触摸明确确认才退出；重复Enter/Escape不重复执行。详情B仍返回列表，源管理/目录/输入各自返回，不触发退出。系统强制关闭/固件终止不属于可拦截的用户确认流程。

## 实测覆盖与边界

检查115个地址，113个返回非空有效内容，Nintendo HK的RSSHub本轮超时，BoleMusic成功但无Release。113源共1786条通过原生解析，其中1643条已直接具备摘要、正文或简介。剩余143条分别为Nintendo JP 100条（原生RSS仅标题）、Game520 25条（无公开可读excerpt，页面403）、A9VG 13条（跳转论坛而非同域文章）、Switchfin 5条（上游依赖Release无说明）。新阅读器会在打开缺简介条目时尝试原站meta，失败则明确显示更新索引和原文入口；没有伪造正文，不能把这些限制宣称为已补齐全文。

6个JSON共339条，301条有发布方简介：Game520 75/100，2468c 100/100，GNN 60/60，NS45 14/14，A9VG 28/41，任天堂台湾24/24。源数据字段和现有用户开关兼容，读取新摘要仅需刷新；通用详情补读和B退出确认需更新客户端。

## 验证

原生13项CTest通过（含11项采集回归）；Web21项网关测试和4个Node套件通过。真实App诊断23验证主界面B、默认A取消、B取消、触摸外部/取消和明确退出，退出码0；Game520真实摘要缓存渲染截图通过。Switch NRO重编完成，图标/资源及签名身份沿用；未进行Switch真机运行测试。Android代码同步无简介提示，但本轮未重新构建APK；其他平台未重发安装包。iOS工程仍在建设，本报告不表示IPA已完成。

初次探测和内容覆盖见reading-repair-sources.json、reading-repair-parser.json、reading-repair-metrics.json；采集覆盖见reading-repair-collection.json。
