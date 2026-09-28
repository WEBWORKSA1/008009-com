"""Shared layout for 008009.com static pages."""
import html, json

SITE = "008009.com"
INTEREST_URL = "https://web.works/contact"
BASE_URL = "https://webworksa1.github.io/008009-com/"  # overridden by build.py --base
VERSION = "1"
AC = ' aria-current="page"'

LOGO_SVG = ('<svg viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#C9A227"/><stop offset="1" stop-color="#a8861a"/></linearGradient></defs>'
            '<rect x="2" y="2" width="60" height="60" rx="16" fill="#B3131B"/>'
            '<circle cx="32" cy="22" r="10" fill="none" stroke="url(#lg)" stroke-width="5"/>'
            '<circle cx="32" cy="43" r="12" fill="none" stroke="url(#lg)" stroke-width="5"/>'
            '<circle cx="32" cy="32" r="28" fill="none" stroke="#C9A227" stroke-width="1.5" stroke-dasharray="3 4"/></svg>')

NAV = [
    ("tools/index.html", "Tools"),
    ("numbers/index.html", "Meanings"),
    ("zodiac/index.html", "Zodiac"),
    ("exchange/index.html", "Exchange"),
    ("videos.html", "Videos"),
    ("guides/index.html", "Guides"),
    ("contests.html", "Contests"),
    ("advertise.html", "Advertise"),
]

def esc(s):
    return html.escape(str(s), quote=True)

def rel(depth):
    return "../" * depth

def ad(slot="inArticle", fmt="auto"):
    return f'<div class="ad-slot container" data-slot="{slot}" data-format="{fmt}" aria-label="Advertisement"></div>'

def lead_modal(r):
    return f'''
<div class="modal" id="lead-modal" role="dialog" aria-modal="true" aria-labelledby="lm-title">
  <div class="box">
    <button class="icon-btn x" data-close aria-label="Close">✕</button>
    <span class="eyebrow">Free · 60 seconds</span>
    <h2 id="lm-title">What is your lucky number worth?</h2>
    <p class="muted">Phone numbers, licence plates and numeric domains with 8s and 9s can sell for a premium. Get a free, no-obligation valuation.</p>
    <form class="form" data-lead="Valuation request (popup)" data-success="Got it! We’ll email your valuation within 48 hours.">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
      <div><label for="lm-n">Your number / plate / domain</label><input id="lm-n" name="number" required placeholder="e.g. 138 8888 1688 or 8899.com"></div>
      <div><label for="lm-e">Email</label><input id="lm-e" type="email" name="email" required autocomplete="email" placeholder="you@example.com"></div>
      <button class="btn btn-primary btn-block" type="submit">Get my free valuation</button>
      <p class="form-note">No spam. Your details are never sold. <a href="{r}privacy.html">Privacy</a></p>
    </form>
  </div>
</div>'''

def page(*, path, title, desc, body, depth, active="", schema=None, scripts=(), og_type="website", extra_head="", modal=True, sticky=True, noindex=False):
    r = rel(depth)
    canonical = BASE_URL + ("" if path == "index.html" else path.replace("index.html", ""))
    full_title = title if SITE in title else f"{title} | {SITE}"
    nav_items = "".join(
        f'<li><a href="{r}{href}"{AC if active == href else ""}>{esc(label)}</a></li>' for href, label in NAV)
    schemas = [{
        "@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE_URL,
        "potentialAction": {"@type": "SearchAction", "target": BASE_URL + "tools/number-analyzer.html?n={search_term_string}", "query-input": "required name=search_term_string"}
    }] if path == "index.html" else []
    if schema:
        schemas += schema if isinstance(schema, list) else [schema]
    schema_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    script_tags = "".join(f'<script src="{r}assets/js/{s}?v={VERSION}" defer></script>' for s in scripts)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta name="theme-color" content="#B3131B">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/img/icon-192.png">
<link rel="manifest" href="{r}manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css?v={VERSION}">
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})()</script>
{schema_html}
{extra_head}
</head>
<body data-base="{r}" data-origin="{BASE_URL}">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar" role="note">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="{INTEREST_URL}" data-interest target="_blank" rel="noopener">Contact us →</a></div>
<header class="site-header">
  <nav class="container nav" aria-label="Main">
    <a class="brand" href="{r}index.html" aria-label="008009.com home">{LOGO_SVG}<span><span class="b-num">008<em>·</em>009</span><small>LUCKY NUMBERS HUB</small></span></a>
    <ul class="menu" id="menu">{nav_items}<li><a href="{r}donate.html"{AC if active == "donate.html" else ""}>❤ Support</a></li></ul>
    <div class="nav-actions">
      <a class="btn btn-primary btn-sm" href="{r}exchange/index.html#lead">Free valuation</a>
      <button class="icon-btn" data-theme-toggle aria-label="Toggle dark mode"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
      <button class="icon-btn menu-toggle" data-menu-toggle aria-controls="menu" aria-expanded="false" aria-label="Open menu"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </nav>
</header>
<main id="main">
{body}
</main>
{footer(r)}
{lead_modal(r) if modal else ""}
{f'<div class="sticky-cta"><a class="btn btn-primary" href="{r}exchange/index.html#lead">🏮 Value or find a lucky number</a></div>' if sticky else ""}
<div class="cookie" id="cookie" role="dialog" aria-label="Cookie consent">
  <b>Cookies & ads</b><p style="margin:.3em 0 0">We use cookies for analytics and to show ads that keep our tools free. Choose “Accept all” for personalised ads or “Essential only” for non-personalised ads. <a href="{r}privacy.html#cookies">Learn more</a></p>
  <div class="btns"><button class="btn btn-primary btn-sm" data-consent="all">Accept all</button><button class="btn btn-ghost btn-sm" data-consent="essential">Essential only</button></div>
</div>
<script src="{r}assets/js/config.js?v={VERSION}" defer></script>
<script src="{r}assets/js/numerology.js?v={VERSION}" defer></script>
<script src="{r}assets/js/main.js?v={VERSION}" defer></script>
{script_tags}
</body>
</html>'''

def footer(r):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{r}index.html" style="color:#fff">{LOGO_SVG}<span><span class="b-num">008<em>·</em>009</span><small style="color:#a2968b">PROSPERITY · LONGEVITY</small></span></a>
        <p style="margin-top:14px;font-size:.94rem">Free tools and guides on lucky numbers in Chinese culture — plus a trusted exchange for premium phone numbers, plates and numeric domains.</p>
        <form class="newsletter" data-lead="Newsletter signup" data-success="You’re in! Watch for your Lucky Number of the Day.">
          <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
          <label class="sr-only" for="nl-email">Email</label>
          <input id="nl-email" type="email" name="email" required placeholder="Lucky Number of the Day by email">
          <input type="hidden" name="list" value="lucky-number-daily">
          <button class="btn btn-gold btn-sm" type="submit">Subscribe</button>
        </form>
        <p style="margin-top:12px;display:flex;gap:12px;flex-wrap:wrap;font-size:.9rem">
          <a data-social="youtube" hidden>YouTube</a><a data-social="x" hidden>X</a><a data-social="instagram" hidden>Instagram</a><a data-social="facebook" hidden>Facebook</a><a data-social="tiktok" hidden>TikTok</a><a data-social="linkedin" hidden>LinkedIn</a>
        </p>
      </div>
      <div><h4>Free tools</h4><ul>
        <li><a href="{r}tools/number-analyzer.html">Lucky Number Analyzer</a></li>
        <li><a href="{r}tools/chinese-zodiac.html">Chinese Zodiac Finder</a></li>
        <li><a href="{r}tools/lucky-date.html">Lucky Date Checker</a></li>
        <li><a href="{r}tools/red-envelope.html">Red Envelope & Price</a></li>
        <li><a href="{r}tools/number-generator.html">Lucky Number Generator</a></li>
        <li><a href="{r}tools/kua-number.html">Kua Number (Feng Shui)</a></li>
      </ul></div>
      <div><h4>Explore</h4><ul>
        <li><a href="{r}numbers/index.html">Number Meanings A–Z</a></li>
        <li><a href="{r}zodiac/index.html">12 Zodiac Animals</a></li>
        <li><a href="{r}guides/index.html">Guides & Research</a></li>
        <li><a href="{r}videos.html">Video Library</a></li>
        <li><a href="{r}contests.html">Contests & Prizes</a></li>
      </ul></div>
      <div><h4>Business</h4><ul>
        <li><a href="{r}exchange/index.html">Lucky Number Exchange</a></li>
        <li><a href="{r}consult.html">Consultations</a></li>
        <li><a href="{r}advertise.html">Advertise & Sponsor</a></li>
        <li><a href="{r}advertise.html#partner">Partnerships</a></li>
        <li><a href="{r}careers.html">Careers & Talent</a></li>
        <li><a href="{r}donate.html">Support Us</a></li>
      </ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{r}about.html">About</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
        <li><a href="{r}privacy.html">Privacy Policy</a></li>
        <li><a href="{r}terms.html">Terms of Use</a></li>
        <li><a href="{r}disclaimer.html">Trademark & Copyright</a></li>
        <li><a href="{INTEREST_URL}" data-interest target="_blank" rel="noopener">Buy / partner on this domain</a></li>
      </ul></div>
    </div>
    <div class="legal">
      <p>© <span data-year>2026</span> 008009.com. All rights reserved. “008009” is used here solely as a descriptive numeric domain name; this website is independent and not affiliated with, endorsed by, or connected to any company, product, service, or trademark that uses the same or similar numbers. All third-party names, logos and videos belong to their respective owners. Content is for cultural, educational and entertainment purposes only — not financial, legal or investment advice. <a href="{r}disclaimer.html">Full disclosure</a>.</p>
    </div>
  </div>
</footer>'''

def breadcrumb(r, items):
    parts = [f'<a href="{r}index.html">Home</a>'] + [f'<a href="{r}{h}">{esc(t)}</a>' if h else f'<span aria-current="page">{esc(t)}</span>' for t, h in items]
    return '<nav class="breadcrumb container" aria-label="Breadcrumb">' + " › ".join(parts) + "</nav>"

def breadcrumb_schema(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL}]
    for i, (t, h) in enumerate(items, start=2):
        e = {"@type": "ListItem", "position": i, "name": t}
        if h: e["item"] = BASE_URL + h
        lst.append(e)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in faqs) + "</div>"

def honey():
    return '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'

def consent_box(r):
    return f'<label class="check"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted about this request and accept the <a href="{r}privacy.html">Privacy Policy</a>.</label>'
