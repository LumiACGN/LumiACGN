---
name: profile-readme-design
description: LumiACGN 个人主页（GitHub profile README）的设计规范、资产地图与维护流程。改动这个主页的任何部分——README.md、hero 横幅 SVG、配色、排版、统计卡、贪吃蛇或相关 workflow——之前都应该先读本 skill，即使用户只说"改改主页 / 换个图 / 更新卡片 / 美化一下"也要触发。关键词：主页、个人主页、README、profile、hero、横幅、墨染樱、二次元、卡片、snake、配色、美化。
---

# LumiACGN 主页设计规范（墨夜樱）

## 设计基调

定稿方案「A · 墨夜樱」：墨夜底 + 樱枝 + 月晕。**一主色（樱粉）、一辅助色（紫/mauve）、一强调色（深樱）**——除 hero 与贪吃蛇外的元素都从这套色板取色，不要引入新色系；多色系会立刻把页面拉回"拼装感"，这是这个设计唯一的纪律。

**暗色板**：页底 `#1d1c27→#11101a`｜樱粉 `#f5c2e7`（主）/`#f8b8d0`/`#fbd3e6`｜mauve `#cba6f7`｜正文 `#f7f0f7`｜次要 `#a6adc8`｜墨痕 `#262535`/`#2a2938`

**浅色板**：页底 `#fffbfd→#f5e6f0`｜深樱 `#c9629a`/`#d479ab`｜正文 `#26242f`｜次要 `#7a7590`

**字体**：霞鹜文楷 Screen（OFL-1.1）。hero 里的文字是 SVG `<text>`，依赖**内嵌的子集字体**（data: URI）而非系统字体——这保证所有访客看到同一款字；改文案时如果出现新字，必须重新子集化（见下）。

**动效纪律**：全页只允许三处动画——typing、hero 飘樱、贪吃蛇。动效越少越高级，这是刻意的克制，不要额外加。

## 资产地图（谁生成、谁维护）

| 文件 | 生成方式 | 想改时改哪里 |
|---|---|---|
| `assets/hero-{dark,light}.svg` | 手绘（受本规范约束） | 直接改 SVG，见"改 hero" |
| `README.md` | 手写 | 直接改 |
| `profile/*.svg`（stats/streak 卡） | **CI 每日生成**（cards.yml） | 改 `.github/workflows/cards.yml` 的 options；**不要手改产物**（会被下次 CI 覆盖） |
| output 分支的蛇 | **CI 生成**（snake.yml） | 改 workflow 里的 `color_snake`/`color_dots` |

## 常见改动怎么做

- **改 hero 文案/配色**：dark、light 两版**必须同步改**（否则明暗切换时会露出不协调）；文案出现新字 → 重新做字体子集（命令见 `references/svg-in-readme.md`），否则新字在访客机器上会退化成系统字体。
- **改卡片配色**：cards.yml 里四张卡的 options 成对改（stats light/dark、streak light/dark）；改完手动 `gh workflow run cards.yml` 立即生效，不必等定时。
- **改 README 布局**：先读 `references/svg-in-readme.md` 的净化约束；明暗一律 `<picture>` 双份引用，兜底 `<img>` 与 light 版一致（老客户端只读 `<img>`）。

## 本地验证（改完必须做）

1. **静态布局**：`rsvg-convert -w 1200 assets/hero-dark.svg -o /tmp/x.png`（它不跑 SMIL，飘樱会停在静态 transform 位置，只看构图）。
2. **动态 + 内嵌字体 + 明暗**：一次性 profile 跑 firefox headless 截图（完整命令见 `references/svg-in-readme.md`）——它会真的播动画、真的用内嵌字体，这两条是本项目最容易悄悄坏掉的地方。
3. **上线后抽查**：截 `https://github.com/LumiACGN` 真实渲染图确认。

## 提交与发布

- Conventional Commits；作者邮箱用 no-reply（全局已配好）。
- 迭代期间破缓存：外部服务 URL 加 `&v=N`；仓库内相对路径（`./profile/x.svg`）靠 `max-age=300` 自然过期。
- 想了解原理与完整清单：`references/theme-lumi.md`（色板全表、hero 结构、README 区块台账）。
