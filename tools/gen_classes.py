#!/usr/bin/env python3
"""Ronin site: right-side menu (General + Classes) and one page per class.
Run from the repo root: python3 tools/gen_classes.py
- injects the menu (CSS, button, drawer, script) into public/index.html between markers
- adds the class tiles to the Classes section of index.html
- writes public/class/<slug>.html and updates public/sitemap.xml
Emblems are original Ronin drawings (SVG) in the official class colours."""
import re, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
INDEX = os.path.join(PUB, 'index.html')
TODAY = datetime.date.today().isoformat()

T, D, H = 'TANK', 'DPS', 'HEAL'
# slug, name, colour, tagline, retail [(role, text)], forever [(role, text)]
CLASSES = [
    ('death-knight', 'Death Knight', '#C41E3A', 'Runes, plague and a wall that never falls.',
     [(T, 'Blood'), (D, 'Unholy · Frost')], []),
    ('demon-hunter', 'Demon Hunter', '#A330C9', 'Fast, fierce and always in the fight.',
     [(T, 'Vengeance'), (D, 'Havoc · Devourer')], []),
    ('druid', 'Druid', '#FF7C0A', 'Four forms. One key.',
     [(T, 'Guardian'), (D, 'Balance · Feral'), (H, 'Restoration')],
     [(T, 'Bear'), (D, 'Cat · Balance'), (H, 'Restoration')]),
    ('hunter', 'Hunter', '#AAD372', 'Your pet, your bow, one button.',
     [(D, 'Beast Mastery · Marksmanship · Survival')], [(D, 'Hunter')]),
    ('mage', 'Mage', '#3FC7EB', 'Pure burst. Clean rotation.',
     [(D, 'Arcane · Fire · Frost')], [(D, 'Arcane · Fire · Frost')]),
    ('monk', 'Monk', '#00FF98', 'Tank, heal or strike, always in balance.',
     [(T, 'Brewmaster'), (D, 'Windwalker'), (H, 'Mistweaver')], []),
    ('paladin', 'Paladin', '#F48CBA', 'The Light in every role.',
     [(T, 'Protection'), (D, 'Retribution'), (H, 'Holy')],
     [(T, 'Protection'), (D, 'Retribution'), (H, 'Holy')]),
    ('priest', 'Priest', '#D9D9E6', 'Shadow and Light on WoW: Forever.',
     [], [(D, 'Shadow'), (H, 'Holy')]),
    ('shaman', 'Shaman', '#0070DD', 'The elements on one key.',
     [(D, 'Elemental · Enhancement'), (H, 'Restoration')],
     [(D, 'Elemental · Enhancement'), (H, 'Restoration')]),
    ('warlock', 'Warlock', '#8788EE', 'DoTs, demons and chaos, perfectly timed.',
     [(D, 'Affliction · Demonology · Destruction')], [(D, 'Affliction · Demonology · Destruction')]),
    ('warrior', 'Warrior', '#C69B6D', 'Rage, steel and nothing else.',
     [(T, 'Protection'), (D, 'Arms · Fury')], [(T, 'Protection'), (D, 'Arms · Fury')]),
]

S = 'fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
F = 'fill="currentColor"'
GLYPH = {
    'death-knight': f'<path {S} d="M32 13v38M17 22l30 20M47 22L17 42M27 15l5 5 5-5M27 49l5-5 5 5"/>',
    'demon-hunter': f'<path {S} d="M23 51c-6-12-4-27 5-38M41 51c6-12 4-27-5-38M26 38h12"/>',
    'druid': f'<path {S} d="M17 47c0-20 12-31 31-31 0 19-11 31-31 31zM17 47l21-21"/>',
    'hunter': f'<path {S} d="M17 47L45 19M34 19h11v11M17 47v-8M17 47h8"/>',
    'mage': f'<path {F} d="M32 11l4.2 16.8L53 32l-16.8 4.2L32 53l-4.2-16.8L11 32l16.8-4.2z"/>',
    'monk': f'<circle cx="32" cy="32" r="17" {S}/><path {S} d="M32 15a8.5 8.5 0 0 1 0 17 8.5 8.5 0 0 0 0 17"/><circle cx="32" cy="23.5" r="2.4" {F}/><circle cx="32" cy="40.5" r="2.4" {F}/>',
    'paladin': f'<path {S} d="M32 25v26"/><rect x="21" y="13" width="22" height="12" rx="2.5" {S}/>',
    'priest': f'<circle cx="32" cy="32" r="9" {S}/><path {S} d="M32 12v6M32 46v6M12 32h6M46 32h6M18 18l4 4M42 42l4 4M46 18l-4 4M22 42l-4 4"/>',
    'shaman': f'<path {F} d="M36 10L19 36h12l-4 18 18-28H33z"/>',
    'warlock': f'<path {F} d="M32 11c8 10 14 16 12 27-1 8-6 14-12 14s-11-6-11-13c0-7 5-11 7-17 2 6 4 8 6 8 0-6-1-12-2-19z"/>',
    'warrior': f'<path {S} d="M18 46L46 18M46 46L18 18M21 38l5 5M38 43l5-5"/>',
}

def emblem(slug, colour, size=56):
    gid = 'g-' + slug
    return (f'<svg class="emb" width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" style="color:{colour}">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{colour}" stop-opacity=".38"/>'
            f'<stop offset="1" stop-color="{colour}" stop-opacity=".08"/></linearGradient></defs>'
            f'<path d="M32 3l25 14.5v29L32 61 7 46.5v-29z" fill="url(#{gid})" stroke="{colour}" stroke-width="2"/>'
            f'{GLYPH[slug]}</svg>')

MENU_CSS = '''
/*MENU-CSS*/
.menu-btn{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:10px;width:38px;height:38px;cursor:pointer;font-size:1.15rem;line-height:1}
.drawer-bg{position:fixed;inset:0;background:rgba(5,4,12,.55);opacity:0;pointer-events:none;transition:opacity .2s;z-index:20}
.drawer{position:fixed;top:0;right:0;height:100%;width:min(340px,88vw);background:var(--bg);border-left:1px solid var(--line);z-index:21;
  transform:translateX(100%);transition:transform .25s ease;overflow-y:auto;padding:18px 18px 40px;box-shadow:-20px 0 60px rgba(0,0,0,.25)}
.menu-open .drawer{transform:none}.menu-open .drawer-bg{opacity:1;pointer-events:auto}
.drawer-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.drawer h4{font:600 .72rem "Chakra Petch";letter-spacing:.22em;color:var(--mute);margin:22px 0 4px;text-transform:uppercase}
.drawer a.it{display:flex;align-items:center;gap:12px;padding:11px 6px;border-bottom:1px solid var(--line);color:var(--fg);text-decoration:none;font-weight:500}
.drawer a.it:hover{color:var(--violet)}
.drawer a.it .emb{flex:none}
.drawer a.it small{margin-left:auto;color:var(--mute);font-size:.75rem;letter-spacing:.08em}
.ctiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:0 0 18px}
.ctile{display:flex;align-items:center;gap:10px;padding:12px;border-radius:14px;border:1px solid var(--line);background:var(--panel);color:var(--fg);text-decoration:none;font-weight:600}
.ctile:hover{transform:translateY(-1px);border-color:var(--violet)}
.chero{display:flex;align-items:center;gap:22px;padding:40px 0 10px}
.chero p{margin:.2em 0 0;color:var(--mute);font-size:1.1rem}
@media (max-width:560px){.chero{flex-direction:column;align-items:flex-start;gap:12px}}
.crumb{font-size:.9rem;margin-top:18px}.crumb a{color:var(--mute);text-decoration:none}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]) .emb{filter:brightness(.7) saturate(1.5)}}
:root[data-theme="light"] .emb{filter:brightness(.7) saturate(1.5)}
/*/MENU-CSS*/
'''

MENU_JS = '''<script>/*MENU-JS*/
(function(){var r=document.documentElement,b=document.getElementById('menuBtn'),c=document.getElementById('menuClose'),bg=document.getElementById('drawerBg'),d=document.getElementById('drawer');
if(!b||!d)return;function set(o){r.classList.toggle('menu-open',o);b.setAttribute('aria-expanded',o?'true':'false');d.setAttribute('aria-hidden',o?'false':'true');if(o){c.focus();}}
b.addEventListener('click',function(){set(!r.classList.contains('menu-open'));});c.addEventListener('click',function(){set(false);b.focus();});bg.addEventListener('click',function(){set(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&r.classList.contains('menu-open')){set(false);b.focus();}});
d.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){set(false);});});})();
/*/MENU-JS*/</script>'''

def role_count(c):
    roles = sorted({r for r, _ in c[4] + c[5]}, key=[T, D, H].index)
    return ' · '.join(roles)

def drawer(prefix):
    gen = [('Home', '#top'), ('What you get', '#what'), ('Always up to date', '#uptodate'), ('Classes', '#specs'),
           ('Keys', '#keys'), ('How to start', '#start'), ('Questions', '#faq'), ('Feedback', '#join')]
    g = ''.join(f'<a class="it" href="{prefix}{h}">{n}</a>' for n, h in gen)
    cl = ''.join(f'<a class="it" href="/class/{c[0]}.html">{emblem(c[0], c[2], 30)}{c[1]}<small>{role_count(c)}</small></a>' for c in CLASSES)
    return ('<!--MENU-->\n<div class="drawer-bg" id="drawerBg"></div>\n'
            '<aside class="drawer" id="drawer" aria-hidden="true" aria-label="Menu">'
            '<div class="drawer-head"><a class="logo" href="/"><img src="/assets/logo-256.png" alt="" width="30" height="30">RONIN</a>'
            '<button class="menu-btn" id="menuClose" type="button" aria-label="Close menu">✕</button></div>'
            f'<h4>General</h4>{g}<h4>Classes</h4>{cl}'
            '<a class="it" href="/downloads/Ronin.zip" download style="color:var(--retail);font-weight:700">⬇ Download Ronin</a></aside>\n<!--/MENU-->')

def tiles():
    t = ''.join(f'<a class="ctile" href="/class/{c[0]}.html">{emblem(c[0], c[2], 34)}{c[1]}</a>' for c in CLASSES)
    return f'<!--TILES--><div class="ctiles">{t}</div><!--/TILES-->'

def strip(s, a, b):
    return re.sub(re.escape(a) + r'.*?' + re.escape(b), '', s, flags=re.S)

def patch_index():
    s = open(INDEX, encoding='utf-8').read()
    s = strip(s, '/*MENU-CSS*/', '/*/MENU-CSS*/\n')
    s = strip(s, '<script>/*MENU-JS*/', '/*/MENU-JS*/</script>')
    s = strip(s, '<!--MENU-->', '<!--/MENU-->')
    s = strip(s, '<!--TILES-->', '<!--/TILES-->')
    s = s.replace('\n\n</style>', '\n</style>')
    s = s.replace('</style>', MENU_CSS.lstrip('\n') + '</style>', 1)
    if 'id="menuBtn"' not in s:
        s = s.replace('<button class="theme" id="theme" type="button" aria-label="Switch light / dark">◐</button>',
                      '<button class="theme" id="theme" type="button" aria-label="Switch light / dark">◐</button>'
                      '<button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">☰</button>', 1)
    s = s.replace('<h2>GSE macros for every class and spec</h2>', '<h2>GSE macros for every class and spec</h2>\n  ' + tiles(), 1)
    s = s.replace('</body>', drawer('/') + '\n' + MENU_JS + '\n</body>', 1)
    s = s.replace('@media (max-width:720px){.links{display:none}.theme{margin-left:auto}}',
                  '@media (max-width:720px){.links{display:none}.theme{margin-left:auto}}', 1)
    open(INDEX, 'w', encoding='utf-8').write(s)
    return s

def section(title, colour, rows, note):
    if not rows:
        return ''
    cls = {T: 't', D: 'd', H: 'h'}
    li = ''.join(f'<li><b class="{cls[r]}">{r}</b> {txt}</li>' for r, txt in rows)
    return (f'<div class="panel card"><h3><span class="dot" style="background:var({colour})"></span>{title}</h3>'
            f'<ul class="roles">{li}</ul><p>{note}</p></div>')

def class_page(c, style, theme_js):
    slug, name, colour, tag, ret, fov = c
    worlds = ' + '.join(w for w, x in (('Retail', ret), ('WoW: Forever', fov)) if x)
    title = f'{name} GSE Macros · {worlds} · Ronin'
    desc = f'Free {name} GSE macros by Ronin for {worlds}. {tag}'
    retail = section('Retail (Midnight)', '--retail', ret, 'Mythic+, Raid, Delve, Beginner and Leveling versions. DPS: single target + AoE.')
    forever = section('WoW: Forever', '--forever', fov, 'Level ranges 1-10, 10-40 and 40-60.')
    keys = []
    if ret:
        keys.append('<tr><td><b>Retail</b></td><td><kbd>Shift</kbd> heal · <kbd>Alt</kbd> crowd control · interrupt on its own key</td></tr>')
    if fov:
        keys.append('<tr><td><b>Forever</b></td><td><kbd>Shift</kbd> heal · <kbd>Ctrl</kbd> interrupt · <kbd>Alt</kbd> class extra</td></tr>')
    open_in = ' or '.join(w for w, x in (('Retail', ret), ('Forever', fov)) if x)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ron1n.cc/class/{slug}.html">
<link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="{name} GSE Macros · Ronin"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta property="og:url" content="https://ron1n.cc/class/{slug}.html"><meta property="og:image" content="https://ron1n.cc/assets/og.png"><meta name="theme-color" content="#0e0c18">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Inter:wght@400;500;600&display=swap">
{style}
</head>
<body>
<nav><div class="wrap">
  <a class="logo" href="/"><img src="/assets/logo-256.png" alt="" width="34" height="34">RONIN<small>GSE SUITE</small></a>
  <div class="links"><a href="/#what">What you get</a><a href="/#specs">Classes</a><a href="/#keys">Keys</a><a href="/#start">Start</a></div>
  <button class="theme" id="theme" type="button" aria-label="Switch light / dark">◐</button><button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer">☰</button>
</div></nav>
<main class="wrap" id="top">
  <div class="crumb"><a href="/">Ronin</a> › <a href="/#specs">Classes</a> › {name}</div>
  <header class="chero">{emblem(slug, colour, 104)}<div><h1 style="margin:0">{name}</h1><p>{tag}</p></div></header>
  <section><div class="grid2">{retail}{forever}</div></section>
  <section><div class="panel"><h3>Your keys</h3><table class="keys">{''.join(keys)}</table></div></section>
  <section class="join"><div class="panel">
    <h2>Get the {name} macros</h2>
    <p class="ver">Install GSE and Ronin, type <kbd>/ronin</kbd>, pick {open_in} and your role. Free, always up to date.</p>
    <div class="cta"><a class="btn primary" href="/downloads/Ronin.zip" download>⬇ Download Ronin</a>
    <a class="btn" href="https://www.curseforge.com/wow/addons/ronin" target="_blank" rel="noopener">CurseForge</a></div>
  </div></section>
</main>
<footer><div class="wrap">Ronin - GSE SUITE · <a href="/">ron1n.cc</a> · Made by Ron1n</div></footer>
{drawer('/')}
{theme_js}
{MENU_JS}
</body></html>
'''

def main():
    s = patch_index()
    style = re.search(r'<style>.*?</style>', s, re.S).group(0)
    m = re.search(r'<script>\s*\(function\(\)\{\s*var root=document.documentElement, btn=document.getElementById\(\'theme\'\);.*?</script>', s, re.S)
    theme_js = re.sub(r"\s*document\.querySelectorAll\('\[data-copy\]'\).*?\}\);\n  \}\);", '', m.group(0), flags=re.S)
    os.makedirs(os.path.join(PUB, 'class'), exist_ok=True)
    for c in CLASSES:
        open(os.path.join(PUB, 'class', c[0] + '.html'), 'w', encoding='utf-8').write(class_page(c, style, theme_js))
    urls = ['https://ron1n.cc/'] + [f'https://ron1n.cc/class/{c[0]}.html' for c in CLASSES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        pr = '1.0' if u.endswith('/') else '0.8'
        sm += f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n'
    open(os.path.join(PUB, 'sitemap.xml'), 'w').write(sm + '</urlset>\n')
    print('index patched,', len(CLASSES), 'class pages')

if __name__ == '__main__':
    main()
