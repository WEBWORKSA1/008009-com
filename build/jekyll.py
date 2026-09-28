#!/usr/bin/env python3
"""Export 008009.com as a compact Jekyll source tree for GitHub Pages (branch deploy, no Actions needed).

GitHub Pages builds it with Jekyll: shared chrome lives in _layouts/, number pages are
front-matter stubs rendered by _layouts/number.html, and absolute URLs come from
_config.yml (absolute_base) so a custom domain is a one-line change.

Usage:  python3 build/jekyll.py [outdir]      (default: _jk/)
"""
import os, sys, json, re, shutil
sys.path.insert(0, os.path.dirname(__file__))
import layout as L

LIQ_BASE = "{{ site.absolute_base }}"
L.BASE_URL = LIQ_BASE                      # every absolute URL becomes Liquid
import build as B                           # noqa: E402  (imports use patched BASE_URL)
B.BASE = LIQ_BASE

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(B.ROOT, "_jk"))
WR = []

def w(path, content):
    content = content.replace("assets/img/icon-512.png", "assets/img/favicon.svg")
    from urllib.parse import quote
    import html as _h
    content = re.sub(r'href="\?role=([^"#]+)#apply"', lambda m: 'href="?role=' + quote(_h.unescape(m.group(1))) + '#apply"', content)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    WR.append(path)

def fm(d):
    """YAML front matter using JSON scalars (valid YAML)."""
    return "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in d.items()) + "---\n"

# ---------------------------------------------------------------- page() replacement
def jk_page(*, path, title, desc, body, depth, active="", schema=None, scripts=(), og_type="website", extra_head="", modal=True, sticky=True, noindex=False):
    r = L.rel(depth)
    full_title = title if L.SITE in title else f"{title} | {L.SITE}"
    cpath = "" if path == "index.html" else path.replace("index.html", "")
    schemas = [{"@context": "https://schema.org", "@type": "WebSite", "name": L.SITE, "url": LIQ_BASE,
                "potentialAction": {"@type": "SearchAction", "target": LIQ_BASE + "tools/number-analyzer.html?n={search_term_string}", "query-input": "required name=search_term_string"}}] if path == "index.html" else []
    if schema:
        schemas += schema if isinstance(schema, list) else [schema]
    schema_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    meta = {"layout": "default", "title": full_title, "description": desc, "r": r, "cpath": cpath, "active": active,
            "scripts": list(scripts), "og_type": og_type, "modal": modal, "sticky": sticky, "noindex": noindex}
    return fm(meta) + schema_html + extra_head + "\n" + body + "\n"

B.page = jk_page
B.write = w

_orig_score = B.num_score_py
def _tile_class(n):
    """Curated category wins over the rough digit heuristic (e.g. 1314 is lucky, 250 is not)."""
    sp = B.SPECIAL.get(n)
    if sp:
        return "bad" if sp[2] == "avoid" else ("great" if _orig_score(n) == "great" else "good")
    return _orig_score(n)
B.num_score_py = _tile_class

# ---------------------------------------------------------------- number pages as stubs
def numbers_stubs():
    # keep the index page (rendered normally)
    orig_write = B.write
    captured = {}
    def cap(path, content):
        if path == "numbers/index.html": orig_write(path, content)
        else: captured[path] = True
    B.write = cap
    B.numbers_pages()
    B.write = orig_write
    for n in B.NUMS:
        sp = B.SPECIAL.get(n)
        if n in B.DIGITS and len(n) == 1:
            cn, py, short, long_, _ = B.DIGITS[n]; headline = f"{n} ({cn}, {py}) — {short}"; intro = long_
        elif sp:
            headline = f"{n} — {sp[0]}"; intro = sp[1]
        else:
            headline = f"Meaning of {n} in Chinese numerology"
            intro = f"{n} combines " + " and ".join(f"{d} ({B.DIGITS[d][0]}, {B.DIGITS[d][2].lower()})" for d in dict.fromkeys(n)) + ". " + (
                "It contains a 4, which many people avoid." if "4" in n else "It contains no 4, so there is nothing traditionally unlucky in it.")
        try:
            iv = int(n); rel_nums = [str(x) for x in (iv - 1, iv + 1) if 0 <= x < 100 and str(x) in B.NUMS]
        except ValueError:
            rel_nums = []
        rel_nums += [k for k in ["8", "9", "88", "168", "518", "888", "520", "1314", "4", "14"] if k != n][:8]
        avoid = bool(sp and sp[2] == "avoid")
        if avoid and "4" not in n:
            lucky_override = "No — it is traditionally avoided in prices, gifts and phone numbers (see the meaning above)."
        else:
            lucky_override = None
        lucky_ans = ("Traditionally it is considered unlucky because it contains or sounds like death (4)." if ("4" in n and n not in ("1314", "9420", "5201314", "1314520"))
                     else f"{n} is generally considered positive or neutral. Use the analyzer on this page for a detailed score.")
        title = f"{n} Meaning in Chinese — {sp[0] if sp else (B.DIGITS[n][2] if n in B.DIGITS else 'Lucky or Unlucky?')}"
        meta = {"n": n, "title": f"{title} | {L.SITE}", "description": f"What does {n} mean in Chinese culture? {intro[:120]}",
                "headline": headline, "intro": intro, "lucky": lucky_override or lucky_ans, "avoid": avoid, "rel": list(dict.fromkeys(rel_nums)),
                "cpath": f"numbers/{n}.html"}
        generic = not sp and not (n in B.DIGITS and len(n) == 1)
        if generic:
            meta = {"n": n, "title": meta["title"], "description": meta["description"], "cpath": meta["cpath"]}
        w(f"numbers/{n}.html", fm(meta))

NUMBER_LAYOUT = """---
layout: default
---
{% assign ds = page.n | split: "" | uniq %}{% if page.intro %}{% assign intro = page.intro %}{% else %}{% capture intro %}{{ page.n }} combines {% for d in ds %}{% assign D = site.data.digits[d] %}{{ d }} ({{ D[0] }}, {{ D[2] | downcase }}){% unless forloop.last %} and {% endunless %}{% endfor %}. {% if page.n contains "4" %}It contains a 4, which many people avoid.{% else %}It contains no 4, so there is nothing traditionally unlucky in it.{% endif %}{% endcapture %}{% endif %}{% if page.lucky %}{% assign lucky = page.lucky %}{% elsif page.n contains "4" %}{% assign lucky = "Traditionally it is considered unlucky because it contains or sounds like death (4)." %}{% else %}{% capture lucky %}{{ page.n }} is generally considered positive or neutral. Use the analyzer on this page for a detailed score.{% endcapture %}{% endif %}{% capture headline %}{{ page.headline | default: "" }}{% endcapture %}{% if headline == "" %}{% capture headline %}Meaning of {{ page.n }} in Chinese numerology{% endcapture %}{% endif %}{% if page.rel %}{% assign rel = page.rel %}{% else %}{% assign iv = page.n | plus: 0 %}{% assign lo = iv | minus: 1 %}{% assign hi = iv | plus: 1 %}{% capture relstr %}{% if lo >= 0 %}{{ lo }},{% endif %}{% if hi < 100 %}{{ hi }},{% endif %}{% assign k = 0 %}{% assign fixed = "8,9,88,168,518,888,520,1314,4,14" | split: "," %}{% for f in fixed %}{% if f != page.n and k < 8 %}{{ f }},{% assign k = k | plus: 1 %}{% endif %}{% endfor %}{% endcapture %}{% assign rel = relstr | split: "," | uniq %}{% endif %}
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":{{ page.n | prepend: "What does " | append: " mean in Chinese?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ intro | jsonify }} } },{"@type":"Question","name":{{ page.n | prepend: "Is " | append: " a lucky number?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ lucky | jsonify }} } },{"@type":"Question","name":{{ page.n | prepend: "Can I buy a phone number or plate with " | append: "?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ page.n | prepend: "Yes — post a request on our Lucky Number Exchange and we’ll alert you when a number containing " | append: " becomes available." | jsonify }} } }]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"{{ site.absolute_base }}"},{"@type":"ListItem","position":2,"name":"Number meanings","item":"{{ site.absolute_base }}numbers/"},{"@type":"ListItem","position":3,"name":{{ page.n | jsonify }},"item":"{{ site.absolute_base }}numbers/{{ page.n }}.html"}]}</script>
<nav class="breadcrumb container" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="../numbers/index.html">Number meanings</a> › <span aria-current="page">{{ page.n }}</span></nav>
<section class="page-hero" style="padding-bottom:0"><div class="container narrow"><span class="eyebrow">Number meaning</span><h1><span class="mono">{{ headline | escape }}</span></h1><p class="lead">{{ intro | escape }}</p></div></section>
<section style="padding-top:18px"><div class="container narrow">
<div class="card"><h2 style="font-size:1.3rem">Luck score for {{ page.n }}</h2>__ANALYZER__</div>
<h2 style="margin-top:32px">Digit by digit</h2><div class="table-wrap"><table><thead><tr><th>Digit</th><th>Chinese</th><th>Meaning</th></tr></thead><tbody>{% for d in ds %}{% assign D = site.data.digits[d] %}<tr><td class="mono"><b>{{ d }}</b></td><td>{{ D[0] }} {{ D[1] }}</td><td>{{ D[2] | escape }}</td></tr>{% endfor %}</tbody></table></div>
__AD__
{% if page.avoid %}<div class="notice"><b>Looking for a number with “{{ page.n }}”?</b> Phone numbers, plates and numeric domains containing {{ page.n }} are rarely wanted — but we can help you swap one away. <a href="../exchange/index.html?number={{ page.n }}&intent=sell#lead">Get help swapping it →</a></div>{% else %}<div class="notice"><b>Looking for a number with “{{ page.n }}”?</b> Phone numbers, plates and numeric domains containing {{ page.n }} are in demand. <a href="../exchange/index.html?number={{ page.n }}&intent=alert#lead">Set a free pattern alert →</a></div>{% endif %}
<h2 style="margin-top:32px">FAQ</h2><div class="faq"><details><summary>What does {{ page.n }} mean in Chinese?</summary><p>{{ intro }}</p></details><details><summary>Is {{ page.n }} a lucky number?</summary><p>{{ lucky }}</p></details><details><summary>Can I buy a phone number or plate with {{ page.n }}?</summary><p>Yes — post a request on our Lucky Number Exchange and we’ll alert you when a number containing {{ page.n }} becomes available.</p></details></div>
<h3 style="margin-top:28px">Related numbers</h3><ul class="pill-list">{% for x in rel %}{% if x != "" %}<li><a href="{{ x }}.html">{{ x }}</a></li>{% endif %}{% endfor %}</ul>
<div class="share-row" style="margin-top:20px"><button class="btn btn-ghost btn-sm" data-share="whatsapp" data-text="What {{ page.n }} means in Chinese culture">Share on WhatsApp</button><button class="btn btn-ghost btn-sm" data-share="x" data-text="What {{ page.n }} means in Chinese culture">Share on X</button><button class="btn btn-ghost btn-sm" data-share="copy">Copy link</button></div>
</div></section>
"""

ZODIAC_LAYOUT = """---
layout: default
---
{% assign els = "Wood,Wood,Fire,Fire,Earth,Earth,Metal,Metal,Water,Water" | split: "," %}<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":{{ page.animal | prepend: "What are the lucky numbers for the " | append: "?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ page.nums | prepend: " are " | prepend: page.animal | prepend: "Commonly cited lucky numbers for the " | append: "." | jsonify }} } },{"@type":"Question","name":{{ page.animal | prepend: "Who is the " | append: " most compatible with?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ page.compat | jsonify }} } },{"@type":"Question","name":{{ page.animal | prepend: "Which years are " | append: " years?" | jsonify }},"acceptedAnswer":{"@type":"Answer","text":{{ page.recent | append: " (check exact lunar new year dates for January/February birthdays)." | jsonify }} } }]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"{{ site.absolute_base }}"},{"@type":"ListItem","position":2,"name":"Zodiac","item":"{{ site.absolute_base }}zodiac/"},{"@type":"ListItem","position":3,"name":{{ page.animal | jsonify }},"item":"{{ site.absolute_base }}{{ page.cpath }}"}]}</script>
<nav class="breadcrumb container" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="../zodiac/index.html">Zodiac</a> › <span aria-current="page">{{ page.animal }}</span></nav>
<section class="page-hero" style="padding-bottom:0"><div class="container narrow"><span class="eyebrow">Chinese zodiac</span><h1>Year of the {{ page.animal }} <span style="color:var(--red)">{{ page.cn }}</span></h1><p class="lead">{{ page.traits }}</p></div></section>
<section style="padding-top:18px"><div class="container narrow">
<div class="grid g2"><div class="card"><h3>Lucky guide</h3><ul class="breakdown"><li><span>Lucky numbers</span><b>{{ page.nums }}</b></li><li><span>Lucky colours</span><b>{{ page.colors }}</b></li><li><span>Best matches</span><b>{{ page.best }}</b></li><li><span>Clashes with</span><b>{{ page.clash }}</b></li></ul></div>
<div class="card"><h3>Is your number lucky for a {{ page.animal }}?</h3>__ANALYZER__</div></div>
__AD__
<h2>{{ page.animal }} years</h2><div class="table-wrap"><table><thead><tr><th>Year*</th><th>Element & sign</th></tr></thead><tbody>{% for y in page.years %}{% assign e = y | minus: 4 | modulo: 10 %}<tr><td>{{ y }}</td><td>{{ els[e] }} {{ page.animal }}</td></tr>{% endfor %}</tbody></table></div><p class="form-note">*Each zodiac year begins at Chinese New Year (between 21 Jan and 20 Feb).</p>
<h2>FAQ</h2><div class="faq"><details><summary>What are the lucky numbers for the {{ page.animal }}?</summary><p>Commonly cited lucky numbers for the {{ page.animal }} are {{ page.nums }}.</p></details><details><summary>Who is the {{ page.animal }} most compatible with?</summary><p>{{ page.compat }}</p></details><details><summary>Which years are {{ page.animal }} years?</summary><p>{{ page.recent }} (check exact lunar new year dates for January/February birthdays).</p></details></div>
<ul class="pill-list" style="margin-top:20px">{% for z in site.data.zodiac %}{% if z[0] != page.animal %}<li><a href="{{ z[0] | downcase }}.html">{{ z[1] }} {{ z[0] }}</a></li>{% endif %}{% endfor %}</ul>
</div></section>
"""

def zodiac_stubs():
    orig = B.write
    def cap(path, content):
        if path == "zodiac/index.html": orig(path, content)
    B.write = cap
    B.zodiac_pages()
    B.write = orig
    for i, z in enumerate(B.ZODIAC):
        name, cn, traits, nums, colors, best, clash = z
        years = [y for y in range(1924, 2045) if (y - 4) % 12 == i]
        meta = {"layout": "zodiac", "title": f"Year of the {name} ({cn}) — Personality, Lucky Numbers & Compatibility | {L.SITE}",
                "description": f"Chinese zodiac {name}: personality, lucky numbers {nums}, lucky colours, best matches ({best}) and years.",
                "r": "../", "cpath": f"zodiac/{name.lower()}.html", "active": "zodiac/index.html", "scripts": ["tools.js"], "og_type": "article",
                "modal": True, "sticky": True, "noindex": False, "animal": name, "cn": cn, "traits": traits, "nums": nums, "colors": colors,
                "best": best, "clash": clash, "compat": f"The {name} gets on best with the {best}, and clashes most with the {clash}.",
                "recent": ", ".join(map(str, years[-6:])), "years": years}
        w(f"zodiac/{name.lower()}.html", fm(meta))

def default_layout():
    r = "{{ r }}"
    nav = "".join(f'<li><a href="{r}{h}"{{% if page.active == "{h}" %}} aria-current="page"{{% endif %}}>{L.esc(lbl)}</a></li>' for h, lbl in L.NAV)
    return f'''{{% assign r = page.r %}}{{% if page.abs %}}{{% assign r = site.baseurl | append: "/" %}}{{% endif %}}<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{{{ page.title | escape }}}}</title>
<meta name="description" content="{{{{ page.description | escape }}}}">
<link rel="canonical" href="{{{{ site.absolute_base }}}}{{{{ page.cpath }}}}">
{{% if page.noindex %}}<meta name="robots" content="noindex">{{% else %}}<meta name="robots" content="index,follow,max-image-preview:large">{{% endif %}}
<meta name="theme-color" content="#B3131B">
<meta property="og:type" content="{{{{ page.og_type | default: 'website' }}}}">
<meta property="og:site_name" content="{L.SITE}">
<meta property="og:title" content="{{{{ page.title | escape }}}}">
<meta property="og:description" content="{{{{ page.description | escape }}}}">
<meta property="og:url" content="{{{{ site.absolute_base }}}}{{{{ page.cpath }}}}">
<meta property="og:image" content="{{{{ site.absolute_base }}}}assets/img/og-image.svg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/favicon.svg">
<link rel="manifest" href="{r}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css?v={L.VERSION}">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})()</script>
</head>
<body data-base="{r}" data-origin="{{{{ site.absolute_base }}}}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar" role="note">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="{L.INTEREST_URL}" data-interest target="_blank" rel="noopener">Contact us →</a></div>
<header class="site-header">
  <nav class="container nav" aria-label="Main">
    <a class="brand" href="{r}index.html" aria-label="008009.com home">{L.LOGO_SVG}<span><span class="b-num">008<em>·</em>009</span><small>LUCKY NUMBERS HUB</small></span></a>
    <ul class="menu" id="menu">{nav}<li><a href="{r}donate.html"{{% if page.active == "donate.html" %}} aria-current="page"{{% endif %}}>❤ Support</a></li></ul>
    <div class="nav-actions">
      <a class="btn btn-primary btn-sm" href="{r}exchange/index.html#lead">Free valuation</a>
      <button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
      <button class="icon-btn menu-toggle" data-menu-toggle aria-controls="menu" aria-expanded="false" aria-label="Open menu"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </nav>
</header>
<main id="main">
{{{{ content }}}}
</main>
{L.footer(r)}
{{% if page.modal %}}{L.lead_modal(r)}{{% endif %}}
{{% if page.sticky %}}<div class="sticky-cta"><a class="btn btn-primary" href="{r}exchange/index.html#lead">🏮 Value or find a lucky number</a></div>{{% endif %}}
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie consent">
  <b>Cookies & ads</b><p style="margin:.3em 0 0">We use cookies for analytics and to show ads that keep our tools free. Choose “Accept all” for personalised ads or “Essential only” for non-personalised ads. <a href="{r}privacy.html#cookies">Learn more</a></p>
  <div class="btns"><button class="btn btn-primary btn-sm" data-consent="all">Accept all</button><button class="btn btn-ghost btn-sm" data-consent="essential">Essential only</button></div>
</div>
<script src="{r}assets/js/config.js?v={L.VERSION}" defer></script>
<script src="{r}assets/js/numerology.js?v={L.VERSION}" defer></script>
<script src="{r}assets/js/main.js?v={L.VERSION}" defer></script>
{{% for s in page.scripts %}}<script src="{r}assets/js/{{{{ s }}}}?v={L.VERSION}" defer></script>{{% endfor %}}
</body>
</html>
'''

OG_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8E0E15"/><stop offset="1" stop-color="#B3131B"/></linearGradient></defs><rect width="1200" height="630" fill="url(#g)"/><rect x="24" y="24" width="1152" height="582" fill="none" stroke="#C9A227" stroke-width="6"/><text x="600" y="250" text-anchor="middle" font-family="Menlo,Consolas,monospace" font-weight="800" font-size="150" fill="#fff">008 · 009</text><text x="600" y="345" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="52" fill="#C9A227" letter-spacing="6">LUCKY NUMBERS HUB</text><text x="600" y="440" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="#fde7e8">Free Chinese numerology tools · Number meanings</text><text x="600" y="490" text-anchor="middle" font-family="Arial,sans-serif" font-size="34" fill="#fde7e8">Lucky Number Exchange: phones · plates · domains</text><text x="600" y="570" text-anchor="middle" font-family="Menlo,Consolas,monospace" font-weight="700" font-size="40" fill="#C9A227">008009.com</text></svg>'''

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    # pages
    B.home(); B.tools_hub(); B.tools_all(); numbers_stubs(); zodiac_stubs(); B.exchange(); B.consult(); B.videos(); B.guides_pages()
    B.contests(); B.careers(); B.advertise(); B.donate(); B.about(); B.contact(); B.legal()
    # 404 — served at any path, so links are absolute via site.baseurl
    body404 = ('<section class="page-hero"><div class="container narrow center"><p class="mono" style="font-size:5rem;color:var(--red);margin:0">404</p>'
               '<h1>This number doesn’t exist (yet)</h1><p class="lead">In Chinese, 404 is doubly unlucky — let’s get you somewhere better.</p>'
               '<p><a class="btn btn-primary" href="{{ site.baseurl }}/index.html">Go home</a> <a class="btn btn-ghost" href="{{ site.baseurl }}/tools/number-analyzer.html">Check a number</a></p></div></section>')
    w("404.html", fm({"layout": "default", "title": "Page not found | 008009.com", "description": "Page not found.", "r": "", "abs": True, "cpath": "404.html",
                      "active": "", "scripts": [], "og_type": "website", "modal": False, "sticky": False, "noindex": True, "permalink": "/404.html"}) + body404 + "\n")
    # layouts & data
    w("_layouts/default.html", default_layout())
    an = B.analyzer_form("../", prefill="{{ page.n }}")
    w("_layouts/number.html", NUMBER_LAYOUT.replace("__ANALYZER__", an).replace("__AD__", L.ad("inArticle")))
    w("_layouts/zodiac.html", ZODIAC_LAYOUT.replace("__ANALYZER__", B.analyzer_form("../")).replace("__AD__", L.ad("inArticle")))
    w("_data/zodiac.json", json.dumps([[z[0], z[1]] for z in B.ZODIAC], ensure_ascii=False))
    w("_data/digits.json", json.dumps({d: [v[0], v[1], v[2]] for d, v in B.DIGITS.items()}, ensure_ascii=False))
    w("_config.yml", "# 008009.com — Jekyll config for GitHub Pages\n"
      "# Custom domain: set absolute_base to \"https://008009.com/\", baseurl to \"\", and add a CNAME file.\n"
      "title: 008009.com\n"
      "absolute_base: \"https://webworksa1.github.io/008009-com/\"\n"
      "baseurl: \"/008009-com\"\n"
      "exclude: [README.md, build, project, pages-check.txt]\n"
      "include: [.well-known]\n"
      "defaults:\n"
      "  - scope: {path: \"numbers\"}\n"
      "    values: {layout: \"number\", r: \"../\", active: \"numbers/index.html\", scripts: [\"tools.js\"], og_type: \"article\", modal: true, sticky: true, noindex: false}\n")
    # sitemap / robots / manifest / sw / assets
    w("sitemap.xml", "---\nlayout: null\n---\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
      "{% for p in site.html_pages %}{% unless p.noindex %}<url><loc>{{ site.absolute_base }}{{ p.cpath }}</loc><lastmod>{{ site.time | date: '%Y-%m-%d' }}</lastmod></url>\n{% endunless %}{% endfor %}</urlset>\n")
    w("robots.txt", "---\nlayout: null\n---\nUser-agent: *\nAllow: /\n\nSitemap: {{ site.absolute_base }}sitemap.xml\n")
    w("manifest.webmanifest", json.dumps({"name": "008009 — Lucky Numbers Hub", "short_name": "008009", "start_url": "./index.html", "display": "standalone", "background_color": "#fbf8f3", "theme_color": "#B3131B",
                                          "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"}]}, indent=1))
    w("sw.js", "/* 008009.com service worker — offline tools */\nconst C='008009-v%s';const CORE=['./','./index.html','./tools/number-analyzer.html','./assets/css/style.css','./assets/js/config.js','./assets/js/numerology.js','./assets/js/main.js','./assets/js/tools.js'];\n"
      "self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});\n"
      "self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});\n"
      "self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;\n"
      "e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))))});\n" % (L.VERSION + "-" + B.TODAY))
    w("ads.txt", open(os.path.join(B.ROOT, "ads.txt"), encoding="utf-8").read())
    w("assets/img/favicon.svg", L.LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ''))
    w("assets/img/og-image.svg", OG_SVG)
    for f in ["assets/css/style.css", "assets/js/config.js", "assets/js/numerology.js", "assets/js/main.js", "assets/js/tools.js"]:
        w(f, open(os.path.join(B.ROOT, f), encoding="utf-8").read())
    # sanity: no stray Liquid in page bodies except intended
    print(f"Jekyll tree: {len(WR)} files → {OUT}")

if __name__ == "__main__":
    main()
