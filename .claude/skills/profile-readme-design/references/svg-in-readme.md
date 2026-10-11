# SVG 进 GitHub README：硬约束、字体子集与本地验证

## 约束的由来（理解两条，就能推出一大半规则）

1. GitHub 对 README 做 HTML 净化：只保留白名单标签（div/table/details/summary/img/picture 等），`<style>`、行内 style、JS 全部剥掉 → **样式只能写在 SVG 文件内部**。
2. `<img>` 加载的 SVG 是隔离世界：内部 CSS keyframes 和 SMIL 动画可以播（贪吃蛇就靠这个），但**一切外部资源都加载不了**（字体、外链图、外链 CSS）→ 字体必须 base64 内嵌（`data:` URI）。

## 硬约束速查

- **明暗主题**：只用 `<picture>` + `(prefers-color-scheme)` + 两份文件。`#gh-dark-mode-only` 写法已失效（camo 代理会丢掉 URL fragment，两张图会同时显示）。
- **camo 代理**（外部域名图片）：单图上限 5MB；按完整 URL 缓存 → 更新后要改文件名或加 `?v=N` 破缓存。
- **引用形态**：
  - 仓库内文件用相对路径 `./profile/x.svg` → 渲染时解析为同源 `/OWNER/REPO/raw/main/...`，**不过 camo**，`cache-control: max-age=300`。
  - 其他分支的文件（如 output 分支的蛇）**不能**用相对路径（相对路径永远指向默认分支），必须用 `raw.githubusercontent.com` 绝对 URL。
- `<picture>` 的兜底 `<img>` 必须与 light 版 source 内容一致。
- **typing-svg 的 `lines` 含非 ASCII（中文）时必须百分号编码**：服务端拒绝 URL 中的裸 UTF-8 字节（HTTP 400，2026-10-11 实测，连少量中文也会 400）。旧 URL 可能靠 camo 缓存存活着，缓存过期即裂图——遇到打字机裂图先检查这一点。

## 字体子集（霞鹜文楷）

hero 的 `@font-face` 里内嵌的是字符子集；**新增文案字符后必须重跑**：

```bash
pyftsubset /usr/share/fonts/TTF/LXGWWenKaiScreen.ttf \
  --text='路弥墨染樱世界第一妹控·二次元LumiACGN爱动画' \
  --output-file=/tmp/wenkai-subset.ttf --no-hinting
base64 -w0 /tmp/wenkai-subset.ttf > /tmp/wenkai-subset.b64
```

然后用一个小脚本把 b64 内容替换进两个 hero SVG 的 `@font-face`（几百 KB 级别的手工粘贴容易出错，用脚本替换）：
`python3 -c "b64=open('/tmp/wenkai-subset.b64').read().strip(); [open(p,'w').write(open(p).read().replace(old_b64, b64)) for p in ('assets/hero-dark.svg','assets/hero-light.svg')]"`（old_b64 用现有文件里那一段，或先设为占位符模式）。

字体 SIL OFL-1.1：内嵌允许；署名已在仓库 `NOTICE` 记录，**不要删除**。

## 本地渲染验证（改完必做）

```bash
# 1) 静态（不跑 SMIL，看构图）
rsvg-convert -w 1200 assets/hero-dark.svg -o /tmp/preview.png

# 2) 动态 + 内嵌字体 + 明暗（firefox 真的跑动画和 @font-face）
P=$(mktemp -d)
# 模拟暗色：在 $P/user.js 写入  user_pref("ui.systemUsesDarkTheme", 1);
# 模拟浅色：同样文件写 0（若截图颜色没变化，改试 layout.css.prefers-color-scheme.content-override 的 0/1/2 三个值）
timeout 90 firefox --headless --profile "$P" --screenshot /tmp/shot.png \
  --window-size=1200,300 "file://$PWD/assets/hero-dark.svg"

# 3) 线上抽查（图片有懒加载，截完看一眼是否都加载出来了，没出来就重截）
timeout 90 firefox --headless --profile "$P" --screenshot /tmp/live.png \
  --window-size=1280,2400 "https://github.com/LumiACGN"
```

**坑**：不要用默认 profile 跑 firefox——机器上已有一个 firefox 在跑时会报 "Firefox is already running"；`--profile` 指向一次性目录即可，互不打扰。

## 提交前 checklist

- [ ] dark / light 两份都改了
- [ ] 出现新字 → 已重新子集化并替换两个文件
- [ ] `<picture>` 的兜底 `<img>` = light 版
- [ ] 文件体积正常（hero 约 24KB；上限 5MB，没有理由接近）
