"""Build book.html (page-turn edition) from index.html content."""
import re, html, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from vignettes import vignette

SRC = os.path.join(ROOT, 'index.html')
s = open(SRC, encoding='utf-8').read()
s = re.sub(r'\s*<div style="margin-top:1.2rem"><figure class="vignette">.*?</figure></div>', '', s, flags=re.S)
s = re.sub(r'\s*<figure class="vignette">.*?</figure>', '', s, flags=re.S)
lines = s.split('\n')

style = s[s.index('<style>') + 7: s.index('</style>')]
script = s[s.index('<script>') + 8: s.rindex('</script>')]


def section_inner(sid):
    start = s.index(f'id="{sid}"')
    start = s.index('<div class="shell">', start) + len('<div class="shell">')
    end = s.index('</section>', start)
    end = s.rindex('</div>', start, end)
    return s[start:end]


def article(aid):
    start = s.rindex('<article', 0, s.index(f'id="{aid}"'))
    end = s.index('</article>', start) + len('</article>')
    return s[start:end]


def between(text, a, b=None):
    i = text.index(a)
    j = text.index(b, i) if b else len(text)
    return text[i:j]


# ---- split content ----
overview = section_inner('overview')
weather = section_inner('weather')
clothing = section_inner('clothing')
food = section_inner('food')
tips = section_inner('tips')
hs = section_inner('huangshan')
hs_head = hs[:hs.index('<h3 style="font-size:1.3rem;margin:0 0 .8rem">11/27 会有多少人？</h3>')]
hs_crowd = between(hs, '<h3 style="font-size:1.3rem;margin:0 0 .8rem">11/27 会有多少人？</h3>', '<div class="route-wrap"')
hs_route = between(hs, '<div class="route-wrap"', '<h3 style="font-size:1.3rem;margin:2.2rem 0 .8rem">两种走法怎么选</h3>')
hs_more = between(hs, '<h3 style="font-size:1.3rem;margin:2.2rem 0 .8rem">两种走法怎么选</h3>')

d = {k: article(k) for k in ['d1', 'd2', 'd3', 'd4', 'd5']}
# move the Tangmo lantern plans out of day 4 into their own page
lp_start = d['d4'].index('      <div class="grid grid-2" style="margin-top:1rem">')
lp_end = d['d4'].index('      <div class="note">\n        <p><b>山顶风：</b>')
lantern = d['d4'][lp_start:lp_end]
d['d4'] = d['d4'][:lp_start] + '      <p class="see-also">晚上怎么看鳌鱼灯，见 <a href="#p-lantern">「唐模鳌鱼灯」</a> 一页。</p>\n' + d['d4'][lp_end:]
for k in d:  # strip the outer card wrapper: pages are already paper
    d[k] = d[k].replace('class="card day"', 'class="day"')

foot = s[s.index('<footer class="sources">'):s.index('</footer>')]
sources = foot[foot.index('<div class="shell">') + len('<div class="shell">'):foot.rindex('</div>')]
sources = sources.replace('<h2>资料来源</h2>', '<div class="section-head"><p class="eyebrow">SOURCES</p><h2>资料来源</h2></div>')

def head(eyebrow, title, sub=''):
    return (f'<div class="section-head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2>'
            + (f'<p>{sub}</p>' if sub else '') + '</div>')

COVER = '''
<div class="cover">
  <div class="slip" lang="zh-Hans">
    <h1>粉墙黛瓦<br>一山松云</h1>
  </div>
  <div class="cover-meta">
    <p class="cover-date">2026.11.25 — 11.29</p>
    <p>厦门 · 宏村 · 黄山 · 唐模</p>
    <p class="cover-hint">向左滑动翻页 →</p>
  </div>
</div>'''

PAGES = [
    ('cover', '封面', COVER),
    ('contents', '目录', None),
    ('overview', '行程总览', overview),
    ('d1', '11/25 去宏村', d['d1']),
    ('d2', '11/26 宏村', d['d2']),
    ('d3', '11/27 上黄山', d['d3']),
    ('d4', '11/28 下山 · 唐模', d['d4']),
    ('d5', '11/29 回厦门', d['d5']),
    ('weather', '天气', weather),
    ('clothing', '穿衣', clothing),
    ('hs-crowd', '黄山 · 人流', hs_head + hs_crowd),
    ('hs-route', '黄山 · 路线', head('HUANGSHAN ROUTE', '两天的路线') + hs_route),
    ('hs-more', '黄山 · 费用与预案', head('HUANGSHAN ROUTE', '走法、费用与预案') + hs_more),
    ('lantern', '唐模鳌鱼灯', head('TANGMO', '唐模鳌鱼灯怎么看', '11/28 周六 18:18 开场。住在唐模，散场后不用抢车。') + lantern),
    ('food', '吃什么', food),
    ('tips', '出发前清单', tips),
    ('sources', '资料来源', sources),
    ('back', '封底', None),
]
N = len(PAGES)
assert N % 2 == 0

toc_items = ''.join(
    f'<li><a href="#p-{pid}"><span>{title}</span><i aria-hidden="true"></i><b>{i + 1}</b></a></li>'
    for i, (pid, title, _) in enumerate(PAGES) if pid not in ('cover', 'contents', 'back'))
CONTENTS = head('CONTENTS', '目录') + f'<ol class="toc-list">{toc_items}</ol>'
BACK = '''
<div class="cover back">
  <div class="back-meta">
    <p>厦门北 → 黄山北 → 厦门北</p>
    <p>G1611 · 11/29 10:12 黄山北发车</p>
    <p class="back-note">时间和价格只用于规划，以景区公告、12306 和实时导航为准。</p>
    <p><a href="./index.html">切换到长页面版</a></p>
  </div>
</div>'''

PEAK = {'d3', 'd4', 'hs-crowd', 'hs-route', 'hs-more'}
body_pages = []
for i, (pid, title, content) in enumerate(PAGES):
    if pid == 'contents':
        content = CONTENTS
    if pid == 'back':
        content = BACK
    kind = ' page--cover' if pid in ('cover', 'back') else (' page--peak' if pid in PEAK else '')
    book_name = '黄山 · 海拔约 1630 米' if pid in PEAK else '徽州五日'
    if pid in PEAK:
        content = re.sub(r'<b>(日[出落]约 \d\d:\d\d)</b>', r'<b class="sun">\1</b>', content)
    runhead = '' if 'cover' in kind else f'<p class="runhead" aria-hidden="true"><span>{book_name}</span><span>{title}</span></p>'
    folio = '' if 'cover' in kind else f'<p class="folio" aria-hidden="true">{i + 1}</p>'
    body_pages.append(
        f'<article class="page{kind}" id="p-{pid}" tabindex="-1" role="group" aria-roledescription="页" '
        f'aria-label="第 {i + 1} 页，共 {N} 页：{title}" data-title="{title}">\n'
        f'<div class="sheet">{runhead}<div class="sheet-body">{vignette(pid)}{content}</div>{folio}</div>\n</article>')

BOOK_CSS = open(os.path.join(HERE, 'book.css'), encoding='utf-8').read()
BOOK_JS = open(os.path.join(HERE, 'book.js'), encoding='utf-8').read()

out = f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="2026年11月25日至29日 厦门—宏村—黄山—唐模 五日亲子行程，翻页书版。">
  <meta name="theme-color" content="#34424d">
  <title>粉墙黛瓦，一山松云｜翻页书版</title>
  <style>{style}
/* ================= book edition ================= */
{BOOK_CSS}
  </style>
</head>
<body class="book-body">
<nav class="bar" aria-label="翻页">
  <button type="button" class="bar-btn" data-dir="prev" aria-label="上一页">‹</button>
  <a class="bar-toc" href="#p-contents">目录</a>
  <p class="bar-pos" aria-hidden="true"><b id="posNum">1</b> / {N}<span id="posTitle">封面</span></p>
  <button type="button" class="bar-btn" data-dir="next" aria-label="下一页">›</button>
</nav>
<main class="book" id="book" tabindex="0" role="region" aria-roledescription="书" aria-label="徽州五日行程书">
{chr(10).join(body_pages)}
</main>
<p class="visually-hidden" role="status" aria-live="polite" id="pageStatus"></p>
<script>{script}</script>
<script type="module">{BOOK_JS}</script>
</body>
</html>
'''
open(os.path.join(ROOT, 'book.html'), 'w', encoding='utf-8').write(out)
print('pages', N, 'bytes', len(out))
