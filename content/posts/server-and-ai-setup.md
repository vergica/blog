---
title: "服务器与我的 AI 助手：从零搭建到多模态全配置"
date: 2026-08-17T15:30:00+08:00
draft: false
tags: ["技术", "服务器", "AI"]
categories: ["折腾记录"]
math: false
---

## 前言

八月中旬，我买了一台腾讯云轻量服务器（Ubuntu 24.04，2 核 3.6G），折腾了两天，实现了三个目标：

1. 一个自己的博客
2. 一个随时在线的 AI 助手（接入 Telegram）
3. 一套内外网服务的基础设施（代理、穿透、备份）

这篇文章记录最终配置和过程中踩过的坑，供自己复盘，也供有同样需求的人参考。

## 博客：Hugo + PaperMod + Caddy

博客选了 **Hugo + PaperMod 主题**，静态站点，部署简单、速度快。

- **Caddy 反向代理**，自动申请和续期 HTTPS 证书，无需手动配置
- 公式渲染用 **KaTeX 本地托管**（静态文件放在 `static/katex/`），不依赖 CDN——国内访问 CDN 经常失败，本地托管一劳永逸

踩过的坑：

- **Hugo goldmark 的 passthrough 配置**：`$$...$$`（块级公式）和 `$...$`（行内公式）都要在 `hugo.yaml` 里显式声明，否则公式不渲染
- **typographer 必须关闭**：实测确认，开启后正文和行内公式里的 `--`、`---`、`...` 会被自动替换成 Unicode 字符（en-dash、省略号等），直接破坏数学公式
- KaTeX 的特殊符号（≠、∥ 等）需要对应字体文件（`static/katex/fonts/`），只放 JS/CSS 不够

部署脚本很简单：`hugo build` 生成静态文件，rsync 到 Web 根目录，一条命令完成。

## 代理：mihomo

服务器在国内，访问 Telegram、GitHub 等需要代理。选用了 **mihomo**（Clash Meta 内核），机场订阅节点。

- 本地混合代理端口（HTTP + SOCKS5）
- 另外开了一个 SOCKS5 监听在 0.0.0.0，供局域网/外部设备使用
- 系统级代理变量写在 `/etc/profile.d/proxy.sh`，新终端自动生效

### 坑：systemd 服务不读 profile

Hermes 的 gateway 是 systemd user service 运行的，**systemd 不加载 `/etc/profile.d/proxy.sh`**，所以 gateway 进程没有代理环境变量，连不上 Telegram。

一开始直接改 service 文件加环境变量，结果 `hermes gateway restart` 会重新生成 service 文件，改动被覆盖。正解是用：

```bash
systemctl --user set-environment http_proxy=http://127.0.0.1:7890
systemctl --user set-environment https_proxy=http://127.0.0.1:7890
systemctl --user set-environment all_proxy=http://127.0.0.1:7890
```

注意：服务器重启后这些变量会丢，需要重新注入。

## AI 助手：Hermes + Telegram

AI 助手用的是 **Hermes Agent**（开源，v0.20.1），通过 Telegram bot 接入，手机随时能聊。

- 渠道最初试过微信，不稳定，果断切 Telegram
- 语音识别：本地 **faster-whisper**（base 模型），免费不限量
- 语音合成：**Edge TTS**（微软免费），选了「晓伊」音色（zh-CN-XiaoyiNeural），活泼可爱
- 定时任务：早上 9 点每日计划提醒、晚上 8 点英语聊天（话题随机抽取）、晚上 23:58 催睡觉

## 模型与多模态

最初用 OpenRouter 聚合 API，DeepSeek 为主模型。后来发现 **OpenRouter 按账单地址封锁 OpenAI / Anthropic / Google 的模型**（403），于是切换到 **OpenCode**。

OpenCode 分两个套餐，付费模式不同：

- **Go 套餐**：订阅制（$10/月），模型价格便宜，但 GPT 和 Grok 在中国大陆不可用
- **Zen 套餐**：按量计费，可用 Claude 系列（同样不能用 GPT 和 Gemini），贵一些，需要时再买

我主力用 Go 套餐的 **deepseek-v4-flash**，Claude 按需走 Zen。

用脚本实测了 OpenCode Go 全部模型的多模态能力，结论：

| 能力 | 结论 |
|---|---|
| 图片理解 | 只有 4 个模型支持：minimax-m3 / kimi-k3 / kimi-k2.7-code / mimo-v2.5 |
| 图片生成 | 全部不支持（无端点） |
| 语音合成 | 全部不支持（无端点） |
| 音频输入 | 全部不支持 |

最终配置：

- 主模型：**deepseek-v4-flash**（OpenCode Go）
- 视觉模型：**minimax-m3**
- 语音识别：本地 faster-whisper
- 语音合成：Edge TTS

图片生成的免费方案也实测过：

- **Hugging Face 免费 API**：已经砍掉了全部生图模型，不可用
- **Pollinations.ai**：免费、无需 key、2-3 秒出图，可用（`image.pollinations.ai/prompt/描述词`）

## 基础设施

- **frps 内网穿透**（frp 服务端），systemd 托管开机自启
- **GitHub 备份**：博客源码推到 GitHub 仓库，避免服务器故障丢源码
- **防火墙**：UFW 只开放必要的端口（SSH、HTTP/HTTPS、代理、穿透等）

## 最终配置总表

| 项目 | 方案 |
|---|---|
| 服务器 | 腾讯云轻量 Ubuntu 24.04，2核 3.6G |
| 博客 | Hugo + PaperMod + Caddy + KaTeX 本地 |
| 代理 | mihomo（本地混合代理 + SOCKS5） |
| AI 助手 | Hermes Agent v0.20.1 + Telegram |
| 主模型 | deepseek-v4-flash（OpenCode Go） |
| 视觉 | minimax-m3（OpenCode Go） |
| 语音识别 | 本地 faster-whisper（base） |
| 语音合成 | Edge TTS（晓伊） |
| 图片生成 | Pollinations.ai（备用） |
| 内网穿透 | frps |
| 源码备份 | GitHub |
