#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 LumiACGN
# SPDX-License-Identifier: MIT
# -*- coding: utf-8 -*-
# 生成「关于我」三块内容卡：勇者部六条 / 喜欢的句子 / 妹控二十条（墨夜樱风格，明暗各一版，内嵌霞鹜文楷子集）
# 依赖：python-fonttools（pyftsubset）、字体 /usr/share/fonts/TTF/LXGWWenKaiScreen.ttf
# 用法：python tools/gen_about_cards.py   （输出到 assets/）
# 注意：wrap() 末尾的外框 rect 必须 fill="none"——带填充会盖住整块内容（踩过坑）
import base64, subprocess, os, tempfile

FONT = '/usr/share/fonts/TTF/LXGWWenKaiScreen.ttf'
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
TMP = tempfile.mkdtemp(prefix='about-cards-')

PETAL = "M0,10 C-6,6 -9,1 -8,-4 C-7.4,-8 -3.5,-9.5 -1.6,-6.8 C-1,-5.6 1,-5.6 1.6,-6.8 C3.5,-9.5 7.4,-8 8,-4 C9,1 6,6 0,10 Z"

PAL = {
    'dark': dict(panel0='#1e1d29', panel1='#13121c', panel_stroke='#3a3949',
                 pink='#f5c2e7', pink2='#f8b8d0', pink3='#fbd3e6', pink4='#eeb5d6',
                 title0='#fad2ec', title1='#eaa9d6', text='#f7f0f7', sub='#a6adc8',
                 roller='#45435e', knob='#cba6f7', knob_in='#1e1d29',
                 dots='#ffffff', dots_op='.05', glow='#f5c2e7', glow_op='.13',
                 ink='#262535', stamp='#e0799c'),
    'light': dict(panel0='#fffcfd', panel1='#fbeaf4', panel_stroke='#eed6e4',
                  pink='#d479ab', pink2='#e98ab8', pink3='#ef9ec6', pink4='#f4b2d3',
                  title0='#d479ab', title1='#b8548a', text='#26242f', sub='#7a7590',
                  roller='#ecd2e2', knob='#d479ab', knob_in='#fffcfd',
                  dots='#5a5568', dots_op='.10', glow='#f2a7cb', glow_op='.10',
                  ink='#2b2a38', stamp='#d4577f'),
}

RULE6 = [('一：', '要好好打招呼。'), ('二：', '尽量不要放弃。'), ('三：', '要吃好睡好。'),
         ('四：', '有烦心事要一起商量。'), ('五：', '只要努力了，基本都会有办法。'), ('六：', '不要逞强，自己也要幸福。')]

QUOTE_A = ['她们是点阵、是数据、这种事情我知道。',
           '那你喜欢的那个女孩又是什么？蛋白质？钙？',
           '争论是愚蠢的，重要的是充满爱的心。']
QUOTE_B = ['决定现在无聊与否，快乐与否，平凡与否的',
           '不是现实，是我来决定的。']

RULE20 = ['妹妹永远是最重要之人', '享受和妹妹相处的时间', '满足妹妹的任性要求',
          '再怎么夸奖妹妹也不为过', '妹妹的喜好牢记于心', '妹妹的请求高于一切',
          '妹妹的生日是最重要的日子', '认真倾听妹妹的每一句话', '全力守护妹妹的笑容',
          '尊重妹妹的隐私', '不可让妹妹等待/秒回妹妹的消息', '第一时间处理妹妹的烦恼',
          '避免让妹妹不安的状况', '不惜一切代价保护妹妹', '妹妹的眼泪是最大的失败，绝不允许发生',
          '不吃光妹妹做的饭菜是不可饶恕的罪行', '妹妹买给自己的东西，从一开始就不存在送人或是扔掉的选择',
          '妹妹的夸奖是全天下最强的动力', '要永远和妹妹在一起', '保证妹妹永远走在正确的道路上']

STYLE_TMPL = '''<style>
      @font-face{font-family:"LXGW WenKai Hero";src:url(data:font/ttf;base64,@B64@) format("truetype");}
      text{font-family:"LXGW WenKai Hero","LXGW WenKai Screen","Noto Sans CJK SC",sans-serif;}
    </style>'''

def subset_b64(chars):
    txt = ''.join(sorted(set(chars)))
    sub = os.path.join(TMP, 'about-subset.ttf')
    subprocess.run(['pyftsubset', FONT, f'--text={txt}', f'--output-file={sub}', '--no-hinting'], check=True)
    return base64.b64encode(open(sub, 'rb').read()).decode()

def defs(p, b64):
    return f'''  <defs>
    {STYLE_TMPL.replace('@B64@', b64)}
    <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{p['panel0']}"/><stop offset="1" stop-color="{p['panel1']}"/>
    </linearGradient>
    <linearGradient id="ttl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{p['title0']}"/><stop offset="1" stop-color="{p['title1']}"/>
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
  </defs>'''

def petal_use(p, x, y, rot, s, ci, op='.85'):
    col = [p['pink'], p['pink2'], p['pink3'], p['pink4']][ci]
    return f'<use href="#petal" fill="{col}" transform="translate({x},{y}) rotate({rot}) scale({s})" opacity="{op}"/>'

def tline(x, y, spans, size, fill, anchor='middle', ls=0):
    inner = ''.join((f'<tspan fill="{f}">{t}</tspan>' if f else f'<tspan>{t}</tspan>') for t, f in spans)
    a = ' text-anchor="middle"' if anchor == 'middle' else ''
    l = f' letter-spacing="{ls}"' if ls else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{l}>{inner}</text>'

def panel(p, w, h, r=18):
    # 只画描边外框（内容与底色都在被裁剪的组里，这里绝不能带填充）
    return (f'<rect x="0.75" y="0.75" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="none" stroke="{p["panel_stroke"]}" stroke-width="1.5"/>\n'
            f'<rect x="8" y="8" width="{w-16}" height="{h-16}" rx="{r-7}" fill="none" stroke="{p["pink"]}" stroke-opacity=".25" stroke-width="1"/>')

def clip_def(w, h, r=18):
    return f'<clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}"/></clipPath>'

def wrap(w, h, p, b64, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <title>关于我 · LumiACGN</title>
  <desc>Embedded font subset: LXGW WenKai Screen (SIL OFL 1.1, https://github.com/lxgw/LxgwWenKai).</desc>
{defs(p, b64)}
  {clip_def(w, h)}
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#panel)"/>
    <rect width="{w}" height="{h}" fill="url(#dots)"/>
{body}
  </g>
  {panel(p, w, h)}
</svg>
'''

# ---------------- 卡片 1：勇者部六条 ----------------
def card_rule6(theme):
    p = PAL[theme]
    w, h = 760, 470
    b64 = subset_b64('「」勇者部六条' + ''.join(a + b for a, b in RULE6))
    body = []
    body.append(f'<circle cx="380" cy="70" r="260" fill="url(#glow)"/>')
    body.append(f'<line x1="150" y1="92" x2="240" y2="92" stroke="{p["pink"]}" stroke-opacity=".45" stroke-width="1.5"/>')
    body.append(f'<line x1="520" y1="92" x2="610" y2="92" stroke="{p["pink"]}" stroke-opacity=".45" stroke-width="1.5"/>')
    body.append(petal_use(p, 132, 92, 60, .55, 1) + petal_use(p, 628, 92, -30, .55, 2))
    body.append(tline(380, 112, [('「勇者部六条」', 'url(#ttl)')], 42, p['text'], ls=4))
    y = 186
    for pre, txt in RULE6:
        body.append(tline(380, y, [(pre, p['pink']), (txt, None)], 29, p['text'], ls=1))
        y += 48
    body.append(petal_use(p, 88, 150, 30, .6, 3))
    body.append(petal_use(p, 676, 210, -45, .55, 2))
    body.append(petal_use(p, 96, 386, 80, .5, 0))
    body.append(petal_use(p, 668, 392, 15, .6, 1))
    body.append(petal_use(p, 300, 56, -20, .45, 3, '.7'))
    return w, h, wrap(w, h, p, b64, '    ' + '\n    '.join(body))

# ---------------- 卡片 2：喜欢的句子 ----------------
def card_quotes(theme):
    p = PAL[theme]
    w, h = 860, 470
    b64 = subset_b64(''.join(QUOTE_A) + ''.join(QUOTE_B))
    body = []
    body.append(f'<circle cx="430" cy="90" r="280" fill="url(#glow)"/>')
    for ang in range(0, 360, 72):
        body.append(f'<g transform="translate(430,74) rotate({ang})"><use href="#petal" fill="{p["pink2"]}" transform="translate(0,-11) rotate(180) scale(.5)" opacity=".9"/></g>')
    body.append(f'<circle cx="430" cy="74" r="3.5" fill="{p["pink"]}"/>')
    body.append(f'<line x1="210" y1="74" x2="360" y2="74" stroke="{p["pink"]}" stroke-opacity=".35" stroke-width="1.5"/>')
    body.append(f'<line x1="500" y1="74" x2="650" y2="74" stroke="{p["pink"]}" stroke-opacity=".35" stroke-width="1.5"/>')
    y = 162
    for ln in QUOTE_A:
        body.append(tline(430, y, [(ln, None)], 27, p['text']))
        y += 46
    body.append(f'<line x1="330" y1="330" x2="405" y2="330" stroke="{p["pink"]}" stroke-opacity=".4" stroke-width="1.5"/>')
    body.append(petal_use(p, 430, 331, 10, .6, 1))
    body.append(f'<line x1="455" y1="330" x2="530" y2="330" stroke="{p["pink"]}" stroke-opacity=".4" stroke-width="1.5"/>')
    y = 386
    for ln in QUOTE_B:
        body.append(tline(430, y, [(ln, None)], 27, p['text']))
        y += 46
    body.append(petal_use(p, 96, 180, 40, .6, 2))
    body.append(petal_use(p, 760, 150, -20, .55, 3))
    body.append(petal_use(p, 110, 400, -55, .5, 0))
    body.append(petal_use(p, 748, 398, 35, .6, 1))
    return w, h, wrap(w, h, p, b64, '    ' + '\n    '.join(body))

# ---------------- 卡片 3：妹控二十条（挂轴）----------------
def card_rule20(theme):
    p = PAL[theme]
    w, h = 780, 1040
    b64 = subset_b64('「」妹控二十条' + ''.join(RULE20) + ''.join(chr(0x2460 + i) for i in range(20)))
    body = []
    body.append(f'<circle cx="390" cy="210" r="300" fill="url(#glow)"/>')
    for ybar in (26, 982):
        body.append(f'<rect x="70" y="{ybar}" width="640" height="18" rx="9" fill="{p["roller"]}"/>')
        body.append(f'<circle cx="70" cy="{ybar+9}" r="14" fill="{p["knob"]}"/><circle cx="70" cy="{ybar+9}" r="6" fill="{p["knob_in"]}"/>')
        body.append(f'<circle cx="710" cy="{ybar+9}" r="14" fill="{p["knob"]}"/><circle cx="710" cy="{ybar+9}" r="6" fill="{p["knob_in"]}"/>')
    body.append(f'<rect x="62" y="54" width="656" height="908" rx="16" fill="url(#panel)" stroke="{p["panel_stroke"]}" stroke-width="1.5"/>')
    body.append(f'<rect x="70" y="62" width="640" height="892" rx="12" fill="none" stroke="{p["pink"]}" stroke-opacity=".22" stroke-width="1"/>')
    body.append(tline(360, 138, [('「妹控二十条」', 'url(#ttl)')], 40, p['text'], ls=4))
    body.append(f'<rect x="562" y="100" width="46" height="46" rx="9" fill="{p["stamp"]}" opacity=".93"/>')
    body.append(f'<rect x="567" y="105" width="36" height="36" rx="6" fill="none" stroke="#fff4f8" stroke-width="1.5" opacity=".8"/>')
    body.append(f'<text x="585" y="133" font-size="27" fill="#fff4f8" text-anchor="middle">妹</text>')
    y = 206
    for i, txt in enumerate(RULE20):
        body.append(f'<text x="110" y="{y}" font-size="21" fill="{p["pink"]}">{chr(0x2460 + i)}</text>')
        body.append(f'<text x="138" y="{y}" font-size="21" fill="{p["text"]}">{txt}</text>')
        y += 39
    body.append(petal_use(p, 92, 240, 35, .55, 2))
    body.append(petal_use(p, 690, 320, -25, .5, 3))
    body.append(petal_use(p, 88, 700, -60, .5, 0))
    body.append(petal_use(p, 692, 760, 25, .55, 1))
    body.append(petal_use(p, 200, 936, 60, .5, 3, '.7'))
    body.append(petal_use(p, 560, 940, -35, .55, 2, '.7'))
    return w, h, wrap(w, h, p, b64, '    ' + '\n    '.join(body))

os.makedirs(OUTDIR, exist_ok=True)
for theme in ('dark', 'light'):
    for name, fn in (('rule6', card_rule6), ('quotes', card_quotes), ('rule20', card_rule20)):
        w, h, svg = fn(theme)
        path = os.path.join(OUTDIR, f'{name}-{theme}.svg')
        with open(path, 'w') as f:
            f.write(svg)
        print(f'written {path}  ({os.path.getsize(path)/1024:.1f} KB)')
