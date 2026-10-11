# 墨夜樱 · 色板全表与组件台账

## 色板全表

| 用途 | 暗色 | 浅色 |
|---|---|---|
| 页底渐变 | `#1d1c27 → #11101a` | `#fffbfd → #f5e6f0` |
| 墨痕（远→近） | `#262535` / `#2a2938` | 同色但 opacity 0.07 / 0.09 |
| 月晕 glow | `#f5c2e7`（.34→0） | `#f2a7cb`（.30→0） |
| 月盘（外/内） | `#f5c2e7`(.15) / `#fbd8ee`(.22) | `#f3b1d2`(.30) / `#fbd8ee`(.45) |
| 樱枝（主/细） | `#3d3c50` / `#3b3a4e` | `#4a4356` / `#544c62` |
| 花瓣 4 色 | `#f5c2e7` `#f8b8d0` `#fbd3e6` `#eeb5d6` | `#ef9ec6` `#e98ab8` `#f4b2d3` `#e585b5` |
| 标题「路弥」 | `#f7f0f7` | `#26242f` |
| 标题「墨染樱」 | 渐变 `#fad2ec→#f5c2e7→#eaa9d6` | 渐变 `#d479ab→#c9629a→#b8548a` |
| 下划线 | `#f5c2e7` | `#d479ab` |
| 副标题 | `#a6adc8` | `#7a7590` |
| 蛇（snake/dots） | 蛇 `#f5c2e7`；dots `#1f1e2b,#3a2c44,#5f3a5e,#934b81,#d16aa9` | 蛇 `#d4577f`；dots `#f7eef4,#fbd3e6,#f4b0d3,#e58bb9,#cf5f9d` |
| 卡片（stats） | theme `catppuccin_mocha` + title `#f5c2e7` / icon `#cba6f7` / text `#cdd6f4` | theme `catppuccin_latte` + title `#c9629a` / icon `#d479ab` / text `#4c4452` |

> 卡片色以 `.github/workflows/cards.yml` 为准（那里是唯一会被执行的真源），上表用于对齐 hero/徽章等手绘元素。

## hero 结构（assets/hero-*.svg，viewBox 1200×300）

绘制顺序 = 图层顺序：

1. `rect` 页底渐变 → 2. 月晕（radialGradient + 内外两层月盘圆）→ 3. 墨痕 2 条（宽波形路径）+ 3 个斑点点缀 → 4. 樱枝 4 段（粗细递减的 stroke，模拟锥度）+ 小枝 2 段 → 5. 枝上花簇 12 朵（`<use>` 引用花瓣 path，各自 translate/rotate/scale）→ 6. 飘落花瓣 6 枚（SMIL translate+rotate 循环；**静态 transform 写在动画中点位置**，这样 rsvg 这类不跑动画的渲染器也能看到合理构图）→ 7. 静置花瓣 3 枚 → 8. 标题（`路弥` x=96 与 `墨染樱` x=292，84px，letter-spacing 6）→ 9. 下划线波浪（y≈196）+ 末端小花瓣 → 10. 副标题（y=244，21px，spacing 7）

- 花瓣形状：`#petal` path（顶端带凹口的樱瓣，尺寸约 16×19，原点在花心）。
- 文字字体：内嵌 `LXGW WenKai Hero`（子集），fallback 链 `LXGW WenKai Screen → LXGW WenKai → Noto Sans CJK SC`。

## README 区块台账

自上而下（全部居中，间距用空 `<div>&nbsp;</div>`）：

1. hero 横幅（`<picture>` 双份，相对路径）
2. typing-svg（明暗双 URL：暗 `color=f5c2e7`、浅 `color=d16d9e`，`background=00000000`）
3. `assets/images/sankarea.jpg`（408×288 装饰图，不随主题切换）
4. stats + streak 卡（`<picture>` 双份，`./profile/*.svg`，宽约 49%）
5. 贪吃蛇（`<picture>` 双份，raw 绝对 URL 指 output 分支）
6. 徽章行（shields 静态徽章 + komarev 计数，统一 `style=flat-square` 与樱粉色系）
7. 「关于我」文字块（中文，简短；文案在 README 里直接改）
8. 页脚小字

保留文案：typing 三句（我知道的最温暖的一个字是爱 / 两个字是动漫 / 三个字是二次元）；副标题（LumiACGN · 世界第一妹控 · 二次元）。
