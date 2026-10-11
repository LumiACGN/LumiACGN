#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 LumiACGN
# SPDX-License-Identifier: MIT
# -*- coding: utf-8 -*-
# 生成「世界観卡」：散华礼弥配图（内嵌 base64）+ 自制打字题词（SMIL 逐字浮现），墨夜樱风格，明暗各一版
# 依赖：python-fonttools（pyftsubset）、 imagemagick（magick）、字体 /usr/share/fonts/TTF/LXGWWenKaiScreen.ttf
# 用法：python tools/gen_stage_cards.py   （输出到 assets/stage-{dark,light}.svg）
# 说明：打字动画用 clipPath 宽度动画实现；clip 矩形的基础宽度=完整宽度（静态渲染器显示全文，浏览器则由动画接管）
import base64, subprocess, os, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '/usr/share/fonts/TTF/LXGWWenKaiScreen.ttf'
OUTDIR = os.path.join(HERE, '..', 'assets')
PHOTO = os.path.join(HERE, '..', 'assets', 'images', 'sankarea.jpg')
TMP = tempfile.mkdtemp(prefix='stage-cards-')

PETAL = "M0,10 C-6,6 -9,1 -8,-4 C-7.4,-8 -3.5,-9.5 -1.6,-6.8 C-1,-5.6 1,-5.6 1.6,-6.8 C3.5,-9.5 7.4,-8 8,-4 C9,1 6,6 0,10 Z"

PAL = {
    'dark': dict(panel0='#1e1d29', panel1='#13121c', panel_stroke='#3a3949',
                 pink='#f5c2e7', pink2='#f8b8d0', pink3='#fbd3e6', pink4='#eeb5d6',
                 title0='#fad2ec', title1='#eaa9d6', text='#f7f0f7',
                 dots='#ffffff', dots_op='.05', glow='#f5c2e7', glow_op='.13',
                 frame='#3a3949', shadow_op='.35', ink='#262535'),
    'light': dict(panel0='#fffcfd', panel1='#fbeaf4', panel_stroke='#eed6e4',
                  pink='#d479ab', pink2='#e98ab8', pink3='#ef9ec6', pink4='#f4b2d3',
                  title0='#d479ab', title1='#b8548a', text='#26242f',
                  dots='#5a5568', dots_op='.10', glow='#f2a7cb', glow_op='.10',
                  frame='#ecd2e2', shadow_op='.16', ink='#2b2a38'),
}

# 题词三句：(前缀文本, 高亮词) —— 高亮词用粉色
LINES = [('我知道的最温暖的一个字是', '爱'),
         ('两个字是', '动漫'),
         ('三个字是', '二次元')]
FS = 33          # 题词字号
TX = 700         # 题词左端 x
LY = [240, 294, 348]   # 三行基线
BASE_DUR = 10    # 动画循环总时长（秒）

STYLE_TMPL = '''<style>
      @font-face{font-family:"LXGW WenKai Hero";src:url(data:font/ttf;base64,@B64@) format("truetype");}
      text{font-family:"LXGW WenKai Hero","LXGW WenKai Screen","Noto Sans CJK SC",sans-serif;}
    </style>'''

def subset_b64(chars):
    txt = ''.join(sorted(set(chars)))
    sub = os.path.join(TMP, 'stage-subset.ttf')
    subprocess.run(['pyftsubset', FONT, f'--text={txt}', f'--output-file={sub}', '--no-hinting'], check=True)
    return base64.b64encode(open(sub, 'rb').read()).decode()

def photo_b64():
    out = os.path.join(TMP, 'sankarea-card.jpg')
    subprocess.run(['magick', PHOTO, '-resize', '1000x', '-quality', '86', out], check=True)
    return base64.b64encode(open(out, 'rb').read()).decode()

def petal_use(p, x, y, rot, s, ci, op='.85'):
    col = [p['pink'], p['pink2'], p['pink3'], p['pink4']][ci]
    return f'<use href="#petal" fill="{col}" transform="translate({x},{y}) rotate({rot}) scale({s})" opacity="{op}"/>'

def build(theme):
    p = PAL[theme]
    w, h = 1200, 540
    fb64 = subset_b64(''.join(a + b for a, b in LINES))
    pb64 = photo_b64()

    # —— 题词行的宽度与裁剪路径（基础宽度=全文宽，静态渲染显示全文；浏览器由动画接管）——
    clips, lines_svg = [], []
    for i, (pre, hi) in enumerate(LINES):
        nchars = len(pre) + len(hi)
        full_w = nchars * FS + 8          # 全宽 + 光标余量
        y = LY[i]
        clips.append(f'<clipPath id="clipL{i}"><rect x="{TX-4}" y="{y-38}" width="{full_w}" height="46"/></clipPath>')
        # 动画：0 → 全文宽（打字）→ 保持 → 收回到 0（与整组淡出同一时刻）
        t0 = [0.02, 0.19, 0.36][i]   # 每行开始
        t1 = t0 + 0.15               # 打字结束
        vals = f"0;0;{full_w};{full_w};0;0"
        kts = f"0;{t0};{t1};0.83;0.88;1"
        animate = (f'<animate attributeName="width" calcMode="linear" dur="{BASE_DUR}s" repeatCount="indefinite" '
                   f'values="{vals}" keyTimes="{kts}"/>')
        # 光标（位于行尾，被 clip 遮挡直到该行打完）
        cur_x = TX + nchars * FS + 4
        cursor = (f'<rect x="{cur_x}" y="{y-26}" width="3.5" height="36" rx="1.7" fill="{p["pink"]}" opacity=".85">'
                  f'<animate attributeName="opacity" values=".9;0;.9" dur="1.1s" repeatCount="indefinite"/></rect>')
        text = (f'<text x="{TX}" y="{y}" font-size="{FS}" fill="{p["text"]}">'
                f'<tspan>{pre}</tspan><tspan fill="{p["pink"]}">{hi}</tspan></text>')
        # clip 矩形的宽度动画写在 rect 上（先放基础宽度，再挂 animate）
        clips[i] = (f'<clipPath id="clipL{i}"><rect x="{TX-4}" y="{y-38}" width="{full_w}" height="46">'
                    f'{animate}</rect></clipPath>')
        lines_svg.append(f'<g clip-path="url(#clipL{i})">{text}{cursor}</g>')

    lines_block = ('<g>\n      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.81;0.87;1" '
                   f'dur="{BASE_DUR}s" repeatCount="indefinite"/>\n      ' + '\n      '.join(lines_svg) + '\n    </g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <title>散华礼弥 · 题词</title>
  <desc>Artwork (c) 2026 LumiACGN. Embedded font subset: LXGW WenKai Screen (SIL OFL 1.1, https://github.com/lxgw/LxgwWenKai).</desc>
  <defs>
    {STYLE_TMPL.replace('@B64@', fb64)}
    <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p['panel0']}"/><stop offset="1" stop-color="{p['panel1']}"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{p['glow']}" stop-opacity="{p['glow_op']}"/>
      <stop offset="1" stop-color="{p['glow']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="34" height="34" patternUnits="userSpaceOnUse">
      <circle cx="6" cy="8" r="1" fill="{p['dots']}" opacity="{p['dots_op']}"/>
      <circle cx="24" cy="22" r=".8" fill="{p['dots']}" opacity="{p['dots_op']}"/>
      <circle cx="17" cy="4" r=".6" fill="{p['dots']}" opacity="{p['dots_op']}"/>
      <circle cx="3" cy="27" r=".7" fill="{p['dots']}" opacity="{p['dots_op']}"/>
    </pattern>
    <path id="petal" d="{PETAL}"/>
    <clipPath id="photoClip"><rect x="108" y="80" width="538" height="380" rx="10"/></clipPath>
    {''.join(clips)}
  </defs>
  <clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20"/></clipPath>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#panel)"/>
    <rect width="{w}" height="{h}" fill="url(#dots)"/>
    <circle cx="940" cy="240" r="330" fill="url(#glow)"/>
    <circle cx="320" cy="270" r="300" fill="url(#glow)"/>
    <path d="M-20,470 C 200,440 420,500 640,462 C 830,430 1010,494 1220,458 L1220,496 C 1010,528 830,466 640,498 C 420,534 200,474 -20,506 Z" fill="{p['ink']}" opacity=".28"/>
    <!-- 礼弥画框 -->
    <rect x="114" y="88" width="538" height="380" rx="12" fill="#000000" opacity="{p['shadow_op']}"/>
    <rect x="98" y="70" width="558" height="400" rx="16" fill="none" stroke="{p['frame']}" stroke-width="1.5"/>
    <rect x="104" y="76" width="546" height="388" rx="13" fill="none" stroke="{p['pink']}" stroke-opacity=".35" stroke-width="1"/>
    <image href="data:image/jpeg;base64,{pb64}" x="108" y="80" width="538" height="380" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoClip)"/>
    {petal_use(p, 98, 70, -30, .7, 1)}{petal_use(p, 656, 470, 150, .65, 2)}{petal_use(p, 640, 66, 45, .55, 3)}
    <!-- 题词 -->
    {petal_use(p, 716, 170, 20, .8, 0)}{petal_use(p, 894, 178, -35, .6, 2)}
    <line x1="742" y1="170" x2="880" y2="170" stroke="{p['pink']}" stroke-opacity=".4" stroke-width="1.5"/>
    {lines_block}
    <path d="M700,386 C 800,379 900,392 1000,383 C 1050,379 1085,385 1112,381" stroke="{p['pink']}" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".5"/>
    {petal_use(p, 1118, 381, 70, .6, 1)}
    {petal_use(p, 1150, 120, -50, .6, 3)}{petal_use(p, 240, 58, 25, .55, 2)}{petal_use(p, 64, 300, 60, .55, 0)}
  </g>
  <rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="20" fill="none" stroke="{p['panel_stroke']}" stroke-width="1.5"/>
  <rect x="8" y="8" width="{w-16}" height="{h-16}" rx="13" fill="none" stroke="{p['pink']}" stroke-opacity=".25" stroke-width="1"/>
</svg>
'''
    path = os.path.join(OUTDIR, f'stage-{theme}.svg')
    with open(path, 'w') as f:
        f.write(svg)
    print(f'written {path}  ({os.path.getsize(path)/1024:.1f} KB)')

for theme in ('dark', 'light'):
    build(theme)
