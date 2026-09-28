#!/usr/bin/env python3
"""Static site generator for 008009.com.
Usage:  python3 build/build.py [--base https://008009.com/]
Writes HTML into the repository root (served as-is by GitHub Pages)."""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(__file__))
import layout as L
from layout import esc, ad, page, breadcrumb, breadcrumb_schema, faq_schema, faq_html, honey, consent_box
from data import DIGITS, SPECIAL, ZODIAC, VIDEOS
from guides import GUIDES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if "--base" in sys.argv:
    L.BASE_URL = sys.argv[sys.argv.index("--base") + 1].rstrip("/") + "/"
BASE = L.BASE_URL
TODAY = datetime.date.today().isoformat()
WRITTEN = []

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    WRITTEN.append(path)

# ------------------------------------------------------------------ helpers
def num_score_py(n):
    """Rough server-side tier for tile colouring (JS engine is canonical)."""
    s = sum(DIGITS[d][4] for d in n) + (5 if n[-1] in "896" else 0) - (6 if n[-1] == "4" else 0)
    return "great" if s >= 12 else "good" if s >= 3 else "bad" if s < -3 else ""

def analyzer_form(r, prefill="", update_url=False, big=True):
    chips = [("Phone", "e.g. 138 8888 1688"), ("Plate", "e.g. 8898"), ("Price", "e.g. 1688"), ("Address", "e.g. 88"), ("Domain", "e.g. 008009"), ("Date", "e.g. 20270206")]
    ch = "".join(f'<button type="button" class="chip" data-kind="{k}" data-ph="{esc(p)}" aria-pressed="{"true" if i == 0 else "false"}">{k}</button>' for i, (k, p) in enumerate(chips))
    return f'''<form class="analyzer" data-analyzer="#an-out" {"data-update-url" if update_url else ""} {f'data-prefill="{esc(prefill)}"' if prefill else ""} role="search" aria-label="Lucky number analyzer">
  <div class="chips" role="group" aria-label="Number type">{ch}</div>
  <div class="num-input"><label class="sr-only" for="an-n">Enter any number</label><input id="an-n" name="n" inputmode="numeric" autocomplete="off" placeholder="e.g. 138 8888 1688" maxlength="48"><button class="btn btn-primary" type="submit">Check my luck</button></div>
  <p class="form-note" style="margin-top:8px">Free · instant · no sign-up. Works for phone numbers, plates, prices, addresses, domains and dates.</p>
</form><div class="result" id="an-out" aria-live="polite"></div>'''

def lead_form(r, subject="Lucky Number Exchange lead", compact=False):
    """High-converting 3-step form for the Exchange."""
    return f'''<form class="lead-box form" id="lead-form" data-lead="{esc(subject)}" data-multistep data-success="🎉 Request received! A specialist will reply within 24 hours (often sooner).">
  {honey()}
  <div class="steps" aria-hidden="true"><span></span><span></span><span></span></div>
  <p class="muted" style="margin:-8px 0 0;font-size:.85rem" data-step-label>Step 1 of 3</p>
  <fieldset class="step" style="border:0;padding:0;margin:0">
    <legend><h3 style="margin:0">What would you like to do?</h3></legend>
    <div class="opt-grid">
      <label class="opt"><input type="radio" name="intent" value="buy" required><span>🔎 Buy a lucky number<small>Phone, plate or domain</small></span></label>
      <label class="opt"><input type="radio" name="intent" value="sell"><span>💰 Sell my number<small>Reach serious buyers</small></span></label>
      <label class="opt"><input type="radio" name="intent" value="valuation"><span>📈 Free valuation<small>What’s it worth?</small></span></label>
      <label class="opt"><input type="radio" name="intent" value="alert"><span>🔔 Pattern alert<small>Notify me when it lists</small></span></label>
    </div>
  </fieldset>
  <fieldset class="step" style="border:0;padding:0;margin:0">
    <legend><h3 style="margin:0">Tell us about the number</h3></legend>
    <div class="row">
      <div><label for="lf-asset">Type</label><select id="lf-asset" name="asset" required><option value="">Choose…</option><option value="phone">Mobile / phone number</option><option value="plate">Licence plate</option><option value="domain">Numeric domain name</option><option value="other">Other (address, account, ID)</option></select></div>
      <div><label for="lf-region">Country / region</label><input id="lf-region" name="region" required placeholder="e.g. Hong Kong, China, Canada, UAE"></div>
    </div>
    <div><label for="lf-num">Number or pattern</label><input id="lf-num" name="number" required placeholder="e.g. 8888 · *168 · AABB · no 4s · 3-digit .com"></div>
    <div class="row">
      <div><label for="lf-budget">Budget / asking price (USD)</label><select id="lf-budget" name="budget"><option value="">Prefer not to say</option><option>Under $500</option><option>$500 – $2,000</option><option>$2,000 – $10,000</option><option>$10,000 – $50,000</option><option>$50,000+</option></select></div>
      <div><label for="lf-time">Timeline</label><select id="lf-time" name="timeline"><option>As soon as possible</option><option>Within 1 month</option><option>1–3 months</option><option>Just exploring</option></select></div>
    </div>
    <div class="step-nav"><button class="btn btn-ghost" data-prev>← Back</button><button class="btn btn-primary" data-next>Continue →</button></div>
  </fieldset>
  <fieldset class="step" style="border:0;padding:0;margin:0">
    <legend><h3 style="margin:0">Where should we send the results?</h3></legend>
    <div class="row">
      <div><label for="lf-name">Name</label><input id="lf-name" name="name" required autocomplete="name" placeholder="Your name"></div>
      <div><label for="lf-email">Email</label><input id="lf-email" type="email" name="email" required autocomplete="email" placeholder="you@example.com"></div>
    </div>
    <div class="row">
      <div><label for="lf-phone">Phone / WhatsApp (optional)</label><input id="lf-phone" type="tel" name="phone" autocomplete="tel" placeholder="+1 …"></div>
      <div><label for="lf-pref">Preferred contact</label><select id="lf-pref" name="preferred_contact"><option>Email</option><option>WhatsApp</option><option>WeChat</option><option>Phone call</option></select></div>
    </div>
    <div><label for="lf-msg">Anything else? (optional)</label><textarea id="lf-msg" name="message" placeholder="Details, links, story behind the number…"></textarea></div>
    {consent_box(r)}
    <div class="step-nav"><button class="btn btn-ghost" data-prev>← Back</button><button class="btn btn-primary" type="submit">Send my request →</button></div>
  </fieldset>
  <div class="assure"><span>Private & confidential</span><span>No obligation</span><span>Reply within 24h</span><span>Escrow for high-value deals</span></div>
</form>'''

def simple_form(r, subject, fields, button, success=None, extra=""):
    """fields: list of (name, label, type, required, placeholder|options)"""
    rows = []
    for f in fields:
        name, label, typ, req, ph = f
        rq = " required" if req else ""
        fid = "f-" + "".join(c for c in subject.lower() if c.isalnum())[:8] + "-" + name
        if typ == "select":
            opts = "".join(f"<option>{esc(o)}</option>" for o in ph)
            rows.append(f'<div><label for="{fid}">{label}</label><select id="{fid}" name="{name}"{rq}>{opts}</select></div>')
        elif typ == "textarea":
            rows.append(f'<div><label for="{fid}">{label}</label><textarea id="{fid}" name="{name}"{rq} placeholder="{esc(ph)}"></textarea></div>')
        elif typ == "row":
            rows.append('<div class="row">' + "".join(
                (f'<div><label for="{fid}-{n2}">{l2}</label><select id="{fid}-{n2}" name="{n2}"{" required" if r2 else ""}>' + "".join(f"<option>{esc(o)}</option>" for o in p2) + "</select></div>") if t2 == "select" else
                f'<div><label for="{fid}-{n2}">{l2}</label><input id="{fid}-{n2}" type="{t2}" name="{n2}"{" required" if r2 else ""} placeholder="{esc(p2)}"{AUTO_EMAIL if t2 == "email" else ""}></div>'
                for n2, l2, t2, r2, p2 in ph) + '</div>')
        else:
            rows.append(f'<div><label for="{fid}">{label}</label><input id="{fid}" type="{typ}" name="{name}"{rq} placeholder="{esc(ph)}"></div>')
    return f'''<form class="form card" data-lead="{esc(subject)}"{f' data-success="{esc(success)}"' if success else ""}>
{honey()}{"".join(rows)}{extra}{consent_box(r)}
<button class="btn btn-primary btn-block" type="submit">{button}</button>
<p class="form-note">We reply within 1–2 business days. Your details stay private.</p>
</form>'''

AUTO_EMAIL = ' autocomplete="email"'
NAME_EMAIL = ("_ne", "", "row", True, [("name", "Name", "text", True, "Your name"), ("email", "Email", "email", True, "you@example.com")])

def zodiac_js():
    data = [{"traits": z[2], "nums": z[3], "colors": z[4], "best": z[5], "clash": z[6]} for z in ZODIAC]
    return f"<script>window.ZODIAC_DATA={json.dumps(data, ensure_ascii=False)};</script>"

def video_card(v):
    vid, title, ch, topic = v
    return f'''<div><div class="video" data-id="{vid}" data-title="{esc(title)}" role="button" tabindex="0" aria-label="Play video: {esc(title)}">
<img loading="lazy" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" width="480" height="360"><div class="play"><span>▶</span></div></div>
<div class="v-meta"><span class="tag gold">{esc(topic)}</span><b>{esc(title)}</b><span class="muted">{esc(ch)} · YouTube</span></div></div>'''

# number list
NUMS = list(dict.fromkeys([str(i) for i in range(0, 100)] + list(SPECIAL)))

# ============================================================ PAGES
def home():
    r = ""
    tools = [("🔢", "Lucky Number Analyzer", "Score any phone number, plate, price or address from 0–100.", "tools/number-analyzer.html"),
             ("🐉", "Chinese Zodiac Finder", "Your animal, element, lucky numbers & colours — lunar-accurate.", "tools/chinese-zodiac.html"),
             ("📅", "Lucky Date Checker", "Check wedding, moving or launch dates, including Ghost Month.", "tools/lucky-date.html"),
             ("🧧", "Red Envelope & Price", "Lucky gift amounts and prices for any budget.", "tools/red-envelope.html"),
             ("🎲", "Lucky Number Generator", "Generate high-scoring numbers with no 4s.", "tools/number-generator.html"),
             ("🧭", "Kua Number", "Feng shui directions for wealth, health and love.", "tools/kua-number.html")]
    tool_cards = "".join(f'<a class="card" href="{h}"><div class="ico">{i}</div><h3>{t}</h3><p class="muted" style="margin:0">{d}</p></a>' for i, t, d, h in tools)
    featured = ["8", "9", "4", "88", "168", "518", "520", "1314", "888", "999", "28", "14", "250", "666", "8888", "008009"]
    tiles = "".join(f'<a class="num-tile {num_score_py(n)}" href="numbers/{n}.html"><b>{n}</b><small>{esc((SPECIAL.get(n) or (DIGITS[n][2],))[0][:22]) if (SPECIAL.get(n) or n in DIGITS) else ""}</small></a>' for n in featured)
    zrow = "".join(f'<a class="z-tile" href="zodiac/{z[0].lower()}.html"><span class="zc">{z[1]}</span>{z[0]}</a>' for z in ZODIAC)
    vids = "".join(video_card(v) for v in VIDEOS[:3])
    guides = "".join(f'<a class="card" href="guides/{g[0]}.html"><span class="tag">{g[3]}</span><h3 style="margin-top:10px">{esc(g[1])}</h3><p class="muted" style="margin:0">{esc(g[2])}</p></a>' for g in GUIDES[:6])
    faqs = [("Is this site free?", "Yes. All calculators, guides and videos are free, supported by advertising, sponsors and donations."),
            ("How is the luck score calculated?", f'We weigh each digit by its traditional meaning (8 prosperity, 9 longevity, 4 avoided), then add points for famous combinations such as 168 and 518, strong endings and collectible patterns. <a href="{r}about.html#method">Read the method</a>.'),
            ("Can you help me buy or sell a lucky number?", f'Yes — the <a href="{r}exchange/index.html">Lucky Number Exchange</a> offers free valuations, pattern alerts and private buyer–seller matching.'),
            ("Is this financial advice?", "No. Number symbolism is a cultural tradition; our tools are for education and entertainment.")]
    body = f'''
<section class="hero"><div class="container hero-grid">
  <div>
    <span class="cn">零零八 · 零零九 &nbsp;·&nbsp; 发 · 久</span>
    <h1>Find the <span class="hl">lucky numbers</span> that bring prosperity that lasts.</h1>
    <p class="lead">Free Chinese-numerology tools, meanings of every number, zodiac insights — and a trusted exchange for premium phone numbers, licence plates and numeric domains.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-primary" href="#check">Check a number free</a><a class="btn btn-ghost" href="exchange/index.html">Buy / sell lucky numbers</a></div>
    <div class="trust-row"><span>No sign-up</span><span>Lunar-calendar accurate</span><span>Private valuations</span></div>
  </div>
  <div class="hero-card" id="check">
    <h2 style="font-size:1.4rem">How lucky is your number?</h2>
    {analyzer_form(r)}
  </div>
</div></section>
{ad("top")}
<section class="alt"><div class="container">
  <div class="stats">
    <div class="stat"><b>¥<span data-count="2330000">2,330,000</span></b><span>paid for phone no. 8888-8888 (2003)</span></div>
    <div class="stat"><b>HK$<span data-count="18100000">18,100,000</span></b><span>for plate “28” (2016)</span></div>
    <div class="stat"><b>US$<span data-count="2300000">2,300,000</span></b><span>for 55.com numeric domain (2011)</span></div>
    <div class="stat"><b><span data-count="130">130</span>+</b><span>number meanings decoded</span></div>
  </div>
  <p class="center muted" style="margin-top:14px;font-size:.85rem">Figures from public reports — see <a href="guides/lucky-number-economy.html">The lucky number economy</a>.</p>
</div></section>
<section><div class="container">
  <div class="section-head"><span class="eyebrow">Free tools</span><h2>Everything you need to choose luckier numbers</h2><p class="lead">Built on traditional Chinese number symbolism — explained, not mysterious.</p></div>
  <div class="grid g3">{tool_cards}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><span class="eyebrow">Number meanings</span><h2>What your numbers really say</h2></div>
  <div class="num-grid">{tiles}</div>
  <p class="center" style="margin-top:20px"><a class="btn btn-ghost" href="numbers/index.html">Browse all 130+ numbers →</a></p>
</div></section>
<section><div class="container">
  <div class="cta-band">
    <div><span class="eyebrow" style="color:var(--gold)">Lucky Number Exchange</span><h2>Own a number full of 8s? It may be worth more than you think.</h2><p>Get a free private valuation, list it for serious buyers, or set an alert for the exact pattern you want — phone numbers, plates and numeric domains.</p></div>
    <div style="display:grid;gap:10px"><a class="btn btn-gold btn-block" href="exchange/index.html?intent=valuation#lead">Get a free valuation</a><a class="btn btn-ghost btn-block" style="color:#fff;border-color:rgba(255,255,255,.4)" href="exchange/index.html?intent=buy#lead">Find a lucky number</a></div>
  </div>
</div></section>
<section class="alt"><div class="container">
  <div class="grid g2" style="align-items:center">
    <div><span class="eyebrow">Chinese New Year countdown</span><h2>The next lunar new year</h2><p class="muted" data-cd-label></p><div class="countdown" data-countdown></div>
      <p style="margin-top:18px"><a href="tools/chinese-zodiac.html">Find your zodiac animal →</a></p></div>
    <div><span class="eyebrow">Lucky number of the day</span><div class="card"><div data-lnotd></div><p class="form-note" style="margin:10px 0 0">Get it in your inbox every morning — subscribe in the footer. Sponsor this slot: <a href="advertise.html">advertise</a>.</p></div></div>
  </div>
  <h3 style="margin-top:36px">The 12 zodiac animals</h3>
  <div class="zodiac-row">{zrow}</div>
</div></section>
{ad("inArticle")}
<section><div class="container">
  <div class="section-head"><span class="eyebrow">Watch</span><h2>Videos on lucky numbers & Chinese culture</h2></div>
  <div class="grid g3">{vids}</div>
  <p class="center" style="margin-top:20px"><a class="btn btn-ghost" href="videos.html">Open the video library →</a></p>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><span class="eyebrow">Guides & research</span><h2>Learn the culture — and the market</h2></div>
  <div class="grid g3">{guides}</div>
</div></section>
<section><div class="container">
  <div class="grid g3">
    <a class="card" href="contests.html"><div class="ico">🏆</div><h3>Contests & prizes</h3><p class="muted" style="margin:0">Share your lucky-number story or photo and win. Sponsor-funded prize pool.</p></a>
    <a class="card" href="donate.html"><div class="ico">❤️</div><h3>Support 008009</h3><p class="muted" style="margin:0">Keep the tools free, fund contests and help us hire bilingual creators.</p></a>
    <a class="card" href="advertise.html"><div class="ico">📣</div><h3>Advertise & partner</h3><p class="muted" style="margin:0">Reach an audience that cares about prosperity, weddings, property and luck.</p></a>
  </div>
</div></section>
<section class="alt"><div class="container narrow"><div class="section-head"><h2>Frequently asked questions</h2></div>{faq_html(faqs)}</div></section>
'''
    write("index.html", page(path="index.html", title="008009.com — Lucky Numbers, Chinese Numerology & Lucky Number Exchange",
          desc="Check how lucky any number is in Chinese culture, learn what 8, 9, 168, 520 and 130+ numbers mean, find your zodiac, and buy or sell premium lucky phone numbers, plates and numeric domains.",
          body=body, depth=0, schema=[faq_schema([(q, a) for q, a in faqs]), {"@context": "https://schema.org", "@type": "Organization", "name": "008009.com", "url": BASE, "logo": BASE + "assets/img/icon-512.png"}]))

def tools_hub():
    r = "../"
    items = [("number-analyzer", "🔢", "Lucky Number Analyzer", "Score phone numbers, plates, prices and more."),
             ("chinese-zodiac", "🐉", "Chinese Zodiac Finder", "Animal, element, lucky numbers & compatibility."),
             ("lucky-date", "📅", "Lucky Date Checker", "Rate wedding, moving and opening dates."),
             ("red-envelope", "🧧", "Red Envelope & Lucky Price", "Auspicious amounts for gifts and pricing."),
             ("number-generator", "🎲", "Lucky Number Generator", "Create high-scoring numbers with no 4s."),
             ("kua-number", "🧭", "Kua Number Calculator", "Your feng shui directions.")]
    cards = "".join(f'<a class="card" href="{s}.html"><div class="ico">{i}</div><h3>{t}</h3><p class="muted" style="margin:0">{d}</p></a>' for s, i, t, d in items)
    body = f'''{breadcrumb(r, [("Tools", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Free tools</span><h1>Lucky number tools</h1><p class="lead">Fast, private calculators based on Chinese number symbolism. Nothing is stored — everything runs in your browser.</p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g3">{cards}</div></div></section>
{ad("inArticle")}
<section class="alt" id="compare"><div class="container narrow">
  <div class="section-head"><h2>Compare two numbers</h2><p class="muted">Choosing between two phone numbers, plates or prices? See which is luckier.</p></div>
  <form class="card form" id="compare-form"><div class="row"><div><label for="ca">Number A</label><input id="ca" name="a" inputmode="numeric" required placeholder="e.g. 13800138000"></div><div><label for="cb">Number B</label><input id="cb" name="b" inputmode="numeric" required placeholder="e.g. 13888881688"></div></div><button class="btn btn-primary" type="submit">Compare</button></form>
  <div class="result" id="compare-out"></div>
</div></section>'''
    write("tools/index.html", page(path="tools/index.html", title="Free Lucky Number Tools & Chinese Numerology Calculators", desc="Free lucky number analyzer, Chinese zodiac finder, lucky date checker, red envelope amounts, lucky number generator and Kua number calculator.", body=body, depth=1, active="tools/index.html", scripts=["tools.js"], schema=breadcrumb_schema([("Tools", "tools/")])))

def tool_page(slug, title, h1, desc, inner, faqs, extra_head="", howto=None):
    r = "../"
    body = f'''{breadcrumb(r, [("Tools", "tools/index.html"), (h1, None)])}
<section class="page-hero" style="padding-bottom:0"><div class="container narrow"><span class="eyebrow">Free tool</span><h1>{h1}</h1><p class="lead">{desc}</p></div></section>
<section style="padding-top:18px"><div class="container narrow">{inner}</div></section>
{ad("inArticle")}
<section class="alt"><div class="container narrow">{howto or ""}<h2>FAQ</h2>{faq_html(faqs)}
<div class="notice" style="margin-top:24px"><b>Need a human expert?</b> Book a numerology, naming or date consultation. <a href="{r}consult.html">See consultations →</a></div></div></section>
<section><div class="container"><h2 class="center">More free tools</h2><ul class="pill-list" style="justify-content:center">
<li><a href="number-analyzer.html">Analyzer</a></li><li><a href="chinese-zodiac.html">Zodiac</a></li><li><a href="lucky-date.html">Lucky date</a></li><li><a href="red-envelope.html">Red envelope</a></li><li><a href="number-generator.html">Generator</a></li><li><a href="kua-number.html">Kua number</a></li><li><a href="index.html#compare">Compare</a></li></ul></div></section>'''
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": h1, "url": BASE + f"tools/{slug}.html", "applicationCategory": "LifestyleApplication", "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
    write(f"tools/{slug}.html", page(path=f"tools/{slug}.html", title=title, desc=desc, body=body, depth=1, active="tools/index.html", scripts=["tools.js"], extra_head=extra_head,
          schema=[app, faq_schema(faqs), breadcrumb_schema([("Tools", "tools/"), (h1, f"tools/{slug}.html")])]))

def tools_all():
    r = "../"
    method = '''<h2>How the score works</h2><ol><li><b>Digits</b> — 8 (+10), 9 (+7), 6 (+6), 2 (+3), 3 (+2), 0/1 (+1), 7 (0), 5 (−1), 4 (−10), scaled for length.</li><li><b>Combinations</b> — 168, 518, 888, 520, 1314 add points; 14, 24, 74, 250 subtract.</li><li><b>Ending</b> — ending on 8, 9 or 6 adds; ending on 4 subtracts.</li><li><b>Patterns</b> — repeats, ABAB, ascending runs and palindromes add memorability.</li><li><b>Normalisation</b> — the total is mapped to a 1–99 score.</li></ol>'''
    tool_page("number-analyzer", "Lucky Number Analyzer — Is My Phone Number Lucky?", "Lucky Number Analyzer",
              "Enter any phone number, licence plate, price, address or domain and get an instant Chinese-numerology luck score with a digit-by-digit explanation and luckier alternatives.",
              analyzer_form(r, update_url=True),
              [("Is my phone number lucky?", "Enter it above. Numbers rich in 8, 9 and 6, without 4, ending on 8 or 9, and containing combinations like 168 or 518 score highest."),
               ("What is the luckiest phone number?", "Solid runs of 8s (e.g. 8888-8888) are considered the luckiest in Chinese culture; one sold for ¥2.33 million in 2003."),
               ("Does the analyzer store my number?", "No. It runs entirely in your browser.")], howto=method)
    tool_page("chinese-zodiac", "Chinese Zodiac Finder — What Is My Chinese Zodiac Sign?", "Chinese Zodiac Finder",
              "Enter your birth date to find your Chinese zodiac animal and element — correctly adjusted for the lunar new year — plus lucky numbers, colours and compatibility.",
              f'''<form class="card form" id="zodiac-form"><div><label for="zd">Birth date</label><input id="zd" type="date" name="dob" required min="1900-01-01" max="2099-12-31"></div><button class="btn btn-primary" type="submit">Find my animal</button></form><div class="result" id="zodiac-out" aria-live="polite"></div>
<h2 style="margin-top:36px">Zodiac compatibility</h2><form class="card form" id="compat-form"><div class="row"><div><label for="za">Your sign</label><select id="za" name="a">{"".join(f'<option value="{i}">{z[0]} {z[1]}</option>' for i, z in enumerate(ZODIAC))}</select></div><div><label for="zb">Partner’s sign</label><select id="zb" name="b">{"".join(f'<option value="{i}">{z[0]} {z[1]}</option>' for i, z in enumerate(ZODIAC))}</select></div></div><button class="btn btn-primary" type="submit">Check compatibility</button></form><div class="result" id="compat-out"></div>''',
              [("Why is my zodiac different from the year I was born?", "The zodiac year starts at Chinese New Year (21 Jan–20 Feb), so January and early-February birthdays belong to the previous animal."),
               ("What is the 2027 zodiac?", "2027 is the Year of the Fire Goat, beginning 6 February 2027.")], extra_head=zodiac_js())
    tool_page("lucky-date", "Lucky Date Checker — Auspicious Wedding & Opening Dates", "Lucky Date Checker",
              "Rate any date for weddings, moves, launches or signings using Chinese number symbolism and the lunar calendar — including Ghost Month warnings.",
              '<form class="card form" id="date-form"><div><label for="dd">Date</label><input id="dd" type="date" name="date" required></div><button class="btn btn-primary" type="submit">Check this date</button></form><div class="result" id="date-out" aria-live="polite"></div>',
              [("What dates are lucky for a wedding in Chinese culture?", "Dates with 8, 9 or 6, love codes like 5/20 and 5/21, and dates outside the 7th lunar month (Ghost Month)."),
               ("Is this a full almanac (通书)?", "No — it scores number symbolism and lunar markers. For a full almanac reading, request a consultation.")])
    tool_page("red-envelope", "Red Envelope (Hongbao) Amount & Lucky Price Generator", "Red Envelope & Lucky Price",
              "Get auspicious amounts for weddings, Chinese New Year, birthdays and business gifts — or lucky retail prices — within your budget.",
              '<form class="card form" id="envelope-form"><div class="row"><div><label for="emin">Minimum</label><input id="emin" type="number" name="min" value="100" min="1" required></div><div><label for="emax">Maximum</label><input id="emax" type="number" name="max" value="1000" min="1" required></div></div><div><label for="eocc">Occasion</label><select id="eocc" name="occasion"><option value="wedding">Wedding</option><option value="newyear">Chinese New Year</option><option value="birthday">Birthday (elder)</option><option value="business">Business opening</option><option value="price">Retail price</option></select></div><button class="btn btn-primary" type="submit">Show lucky amounts</button></form><div class="result" id="envelope-out" aria-live="polite"></div>',
              [("How much money goes in a red envelope?", "Any amount without a 4; even amounts for weddings and New Year. 88, 168, 288, 520 and 888 are favourites."),
               ("Why avoid odd amounts at weddings?", "Pairs symbolise union — ‘good things come in pairs’ — so even amounts are customary.")])
    tool_page("number-generator", "Lucky Number Generator — Create Auspicious Numbers", "Lucky Number Generator",
              "Generate high-scoring lucky numbers of any length — for choosing phone numbers, PINs, plates, product codes or just for fun.",
              '<form class="card form" id="gen-form"><div class="row"><div><label for="glen">Length</label><input id="glen" type="number" name="len" min="1" max="16" value="8" required></div><div><label for="gpre">Must start with (optional)</label><input id="gpre" name="prefix" inputmode="numeric" placeholder="e.g. 138"></div></div><label class="check"><input type="checkbox" name="nofour" checked> Exclude the number 4</label><button class="btn btn-primary" type="submit">Generate</button></form><div class="result" id="gen-out" aria-live="polite"></div>',
              [("Can I use these as lottery numbers?", "They’re for fun and cultural inspiration only — they don’t change the odds of any game."),
               ("How do I get one of these as a real phone number?", "Ask your carrier for premium numbers, or post a pattern alert on our Exchange.")])
    tool_page("kua-number", "Kua Number Calculator — Feng Shui Lucky Directions", "Kua Number Calculator",
              "Find your personal Kua number and your four favourable feng shui directions for wealth, health, love and personal growth.",
              '<form class="card form" id="kua-form"><div class="row"><div><label for="kd">Birth date</label><input id="kd" type="date" name="dob" required></div><div><label for="ks">Sex (traditional formula)</label><select id="ks" name="sex"><option value="f">Female</option><option value="m">Male</option></select></div></div><button class="btn btn-primary" type="submit">Calculate Kua</button></form><div class="result" id="kua-out" aria-live="polite"></div>',
              [("What is a Kua number?", "A feng shui number (1–9, never 5) based on birth year and sex that places you in the East or West group."),
               ("Why does my birthday in January change the result?", "Feng shui uses the solar year starting around 4 February (Li Chun).")])

def numbers_pages():
    r = "../"
    cats = {"wealth": "Wealth & prosperity", "love": "Love & romance", "luck": "Good luck", "avoid": "Numbers to avoid", "pattern": "Patterns & codes"}
    groups = {k: [] for k in cats}
    for n in NUMS:
        sp = SPECIAL.get(n)
        if sp: groups[sp[2]].append(n)
    blocks = ""
    for k, label in cats.items():
        blocks += f'<h2 style="margin-top:32px">{label}</h2><div class="num-grid">' + "".join(f'<a class="num-tile {num_score_py(n)}" href="{n}.html"><b>{n}</b><small>{esc(SPECIAL[n][0][:24])}</small></a>' for n in groups[k]) + "</div>"
    singles = '<h2>Single digits 0–9</h2><div class="num-grid">' + "".join(f'<a class="num-tile {num_score_py(d)}" href="{d}.html"><b>{d}</b><small>{DIGITS[d][0]} · {esc(DIGITS[d][2][:20])}</small></a>' for d in "0123456789") + "</div>"
    two = '<h2 style="margin-top:32px">Every number 10–99</h2><div class="num-grid">' + "".join(f'<a class="num-tile {num_score_py(str(i))}" href="{i}.html"><b>{i}</b></a>' for i in range(10, 100)) + "</div>"
    body = f'''{breadcrumb(r, [("Number meanings", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Encyclopedia</span><h1>Number meanings in Chinese culture</h1><p class="lead">What every digit and famous combination means — from 8 (prosperity) and 9 (longevity) to 520 (“I love you”) and 250 (“idiot”).</p>
<form class="num-input" onsubmit="event.preventDefault();var v=this.q.value.replace(/\\D/g,'');if(v)location.href='../tools/number-analyzer.html?n='+v;" style="max-width:560px"><label class="sr-only" for="nq">Look up a number</label><input id="nq" name="q" inputmode="numeric" placeholder="Look up any number…"><button class="btn btn-primary">Analyze</button></form></div></section>
<section style="padding-top:0"><div class="container">{singles}{ad("inArticle")}{blocks}{two}</div></section>'''
    write("numbers/index.html", page(path="numbers/index.html", title="Chinese Number Meanings A–Z — Lucky & Unlucky Numbers", desc="Meanings of 130+ numbers in Chinese culture: lucky 8, 9, 6, 168, 518, 888; love codes 520 and 1314; unlucky 4, 14, 250 — with scores and examples.", body=body, depth=1, active="numbers/index.html", schema=breadcrumb_schema([("Number meanings", "numbers/")])))

    for n in NUMS:
        sp = SPECIAL.get(n)
        if n in DIGITS and len(n) == 1:
            cn, py, short, long_, w = DIGITS[n]
            headline = f"{n} ({cn}, {py}) — {short}"
            intro = long_
        elif sp:
            headline = f"{n} — {sp[0]}"
            intro = sp[1]
        else:
            headline = f"Meaning of {n} in Chinese numerology"
            intro = f"{n} combines " + " and ".join(f"{d} ({DIGITS[d][0]}, {DIGITS[d][2].lower()})" for d in dict.fromkeys(n)) + ". " + (
                "It contains a 4, which many people avoid." if "4" in n else "It contains no 4, so there is nothing traditionally unlucky in it.")
        digit_rows = "".join(f'<tr><td class="mono"><b>{d}</b></td><td>{DIGITS[d][0]} {DIGITS[d][1]}</td><td>{esc(DIGITS[d][2])}</td></tr>' for d in dict.fromkeys(n))
        # related
        try:
            iv = int(n); rel_nums = [str(x) for x in (iv - 1, iv + 1) if 0 <= x < 100 and str(x) in NUMS]
        except ValueError:
            rel_nums = []
        rel_nums += [k for k in ["8", "9", "88", "168", "518", "888", "520", "1314", "4", "14"] if k != n][:8]
        rel_links = "".join(f'<li><a href="{x}.html">{x}</a></li>' for x in dict.fromkeys(rel_nums))
        cat_word = {"avoid": "avoid", "love": "love"}.get(sp[2] if sp else "", "")
        faqs = [(f"What does {n} mean in Chinese?", intro),
                (f"Is {n} a lucky number?", "Traditionally it is considered unlucky because it contains or sounds like death (4)." if ("4" in n and n not in ("1314", "9420", "5201314", "1314520")) else f"{n} is generally considered positive or neutral. Use the analyzer on this page for a detailed score."),
                (f"Can I buy a phone number or plate with {n}?", f"Yes — post a request on our Lucky Number Exchange and we’ll alert you when a number containing {n} becomes available.")]
        body = f'''{breadcrumb(r, [("Number meanings", "numbers/index.html"), (n, None)])}
<section class="page-hero" style="padding-bottom:0"><div class="container narrow"><span class="eyebrow">Number meaning</span><h1><span class="mono">{esc(headline)}</span></h1><p class="lead">{esc(intro)}</p></div></section>
<section style="padding-top:18px"><div class="container narrow">
<div class="card"><h2 style="font-size:1.3rem">Luck score for {n}</h2>{analyzer_form(r, prefill=n)}</div>
<h2 style="margin-top:32px">Digit by digit</h2><div class="table-wrap"><table><thead><tr><th>Digit</th><th>Chinese</th><th>Meaning</th></tr></thead><tbody>{digit_rows}</tbody></table></div>
{ad("inArticle")}
<div class="notice"><b>Looking for a number with “{n}”?</b> Phone numbers, plates and numeric domains containing {n} are {"rarely wanted — but we can help you swap one away." if cat_word == "avoid" else "in demand."} <a href="../exchange/index.html?number={n}&intent={"sell" if cat_word == "avoid" else "alert"}#lead">{"Get help swapping it" if cat_word == "avoid" else "Set a free pattern alert"} →</a></div>
<h2 style="margin-top:32px">FAQ</h2>{faq_html(faqs)}
<h3 style="margin-top:28px">Related numbers</h3><ul class="pill-list">{rel_links}</ul>
<div class="share-row" style="margin-top:20px"><button class="btn btn-ghost btn-sm" data-share="whatsapp" data-text="What {n} means in Chinese culture">Share on WhatsApp</button><button class="btn btn-ghost btn-sm" data-share="x" data-text="What {n} means in Chinese culture">Share on X</button><button class="btn btn-ghost btn-sm" data-share="copy">Copy link</button></div>
</div></section>'''
        title = f"{n} Meaning in Chinese — {sp[0] if sp else (DIGITS[n][2] if n in DIGITS else 'Lucky or Unlucky?')}"
        write(f"numbers/{n}.html", page(path=f"numbers/{n}.html", title=title, desc=f"What does {n} mean in Chinese culture? {intro[:120]}", body=body, depth=1, active="numbers/index.html", scripts=["tools.js"], og_type="article",
              schema=[faq_schema(faqs), breadcrumb_schema([("Number meanings", "numbers/"), (n, f"numbers/{n}.html")])]))

def zodiac_pages():
    r = "../"
    cards = "".join(f'<a class="card" href="{z[0].lower()}.html"><span style="font-family:var(--serif);font-size:2.4rem;color:var(--red)">{z[1]}</span><h3>{z[0]}</h3><p class="muted" style="margin:0">Lucky numbers {z[3]} · {z[4]}</p></a>' for z in ZODIAC)
    body = f'''{breadcrumb(r, [("Zodiac", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Chinese zodiac · 生肖</span><h1>The 12 Chinese zodiac animals</h1><p class="lead">Personality, lucky numbers, colours and compatibility for every sign. Not sure of yours? <a href="../tools/chinese-zodiac.html">Use the finder</a>.</p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g4">{cards}</div></div></section>{ad("inArticle")}'''
    write("zodiac/index.html", page(path="zodiac/index.html", title="Chinese Zodiac Animals — Personality, Lucky Numbers & Compatibility", desc="All 12 Chinese zodiac animals explained: personality traits, lucky numbers, lucky colours, best matches and clashes.", body=body, depth=1, active="zodiac/index.html", schema=breadcrumb_schema([("Zodiac", "zodiac/")])))
    for i, z in enumerate(ZODIAC):
        name, cn, traits, nums, colors, best, clash = z
        years = [y for y in range(1924, 2045) if (y - 4) % 12 == i]
        els = ["Wood", "Wood", "Fire", "Fire", "Earth", "Earth", "Metal", "Metal", "Water", "Water"]
        yrows = "".join(f"<tr><td>{y}</td><td>{els[(y - 4) % 10]} {name}</td></tr>" for y in years)
        faqs = [(f"What are the lucky numbers for the {name}?", f"Commonly cited lucky numbers for the {name} are {nums}."),
                (f"Who is the {name} most compatible with?", f"The {name} gets on best with the {best}, and clashes most with the {clash}."),
                (f"Which years are {name} years?", ", ".join(map(str, years[-6:])) + " (check exact lunar new year dates for January/February birthdays).")]
        body = f'''{breadcrumb(r, [("Zodiac", "zodiac/index.html"), (name, None)])}
<section class="page-hero" style="padding-bottom:0"><div class="container narrow"><span class="eyebrow">Chinese zodiac</span><h1>Year of the {name} <span style="color:var(--red)">{cn}</span></h1><p class="lead">{traits}</p></div></section>
<section style="padding-top:18px"><div class="container narrow">
<div class="grid g2"><div class="card"><h3>Lucky guide</h3><ul class="breakdown"><li><span>Lucky numbers</span><b>{nums}</b></li><li><span>Lucky colours</span><b>{colors}</b></li><li><span>Best matches</span><b>{best}</b></li><li><span>Clashes with</span><b>{clash}</b></li></ul></div>
<div class="card"><h3>Is your number lucky for a {name}?</h3>{analyzer_form(r)}</div></div>
{ad("inArticle")}
<h2>{name} years</h2><div class="table-wrap"><table><thead><tr><th>Year*</th><th>Element & sign</th></tr></thead><tbody>{yrows}</tbody></table></div><p class="form-note">*Each zodiac year begins at Chinese New Year (between 21 Jan and 20 Feb).</p>
<h2>FAQ</h2>{faq_html(faqs)}
<ul class="pill-list" style="margin-top:20px">{"".join(f'<li><a href="{x[0].lower()}.html">{x[1]} {x[0]}</a></li>' for x in ZODIAC if x[0] != name)}</ul>
</div></section>'''
        write(f"zodiac/{name.lower()}.html", page(path=f"zodiac/{name.lower()}.html", title=f"Year of the {name} ({cn}) — Personality, Lucky Numbers & Compatibility", desc=f"Chinese zodiac {name}: personality, lucky numbers {nums}, lucky colours, best matches ({best}) and years.", body=body, depth=1, active="zodiac/index.html", scripts=["tools.js"], og_type="article",
              schema=[faq_schema(faqs), breadcrumb_schema([("Zodiac", "zodiac/"), (name, f"zodiac/{name.lower()}.html")])]))

def exchange():
    r = "../"
    tiers = [("Imperial", "AAAAAA · 888888 · 8888-8888", "Solid runs of 8 or 9. Collector-grade; rare.", "gold"),
             ("Prosperity", "*168 · *518 · *1688 · 8899", "Famous wealth combinations and endings.", "gold"),
             ("Harmony", "AABB · ABAB · mirror numbers", "Rhythmic, memorable patterns.", "jade"),
             ("Clean", "No 4s · ends in 8/9", "Everyday lucky numbers at accessible prices.", "jade")]
    tiles = "".join(f'<div class="card"><span class="tag {c}">{t}</span><p class="mono" style="font-size:1.2rem;margin:12px 0 6px">{p}</p><p class="muted" style="margin:0">{d}</p></div>' for t, p, d, c in tiers)
    faqs = [("How does the Exchange work?", "Tell us what you want to buy, sell or value. A specialist reviews it, researches comparable sales and connects serious buyers and sellers privately. Transfers follow the rules of your carrier, licensing authority or domain registrar."),
            ("How much does it cost?", "Valuations and alerts are free. When we broker a completed sale we charge a success commission agreed in advance — nothing if it doesn’t sell."),
            ("Do you handle licence plate transfers?", "Plate rules differ by jurisdiction (e.g. Hong Kong’s Transport Department auctions special marks). We guide you through the official process and never bypass it."),
            ("Is my information kept private?", "Yes. Your contact details are never published or sold; buyers only see what you approve."),
            ("Can I buy the domain 008009.com itself?", 'For inquiries about this website or domain, use the <a href="https://web.works/contact" target="_blank" rel="noopener">contact link</a> at the top of every page.')]
    body = f'''{breadcrumb(r, [("Lucky Number Exchange", None)])}
<section class="hero" style="padding-top:28px"><div class="container hero-grid">
  <div>
    <span class="eyebrow">Lucky Number Exchange · 靓号交易</span>
    <h1>Buy, sell & value <span class="hl">lucky numbers</span> — privately.</h1>
    <p class="lead">Premium phone numbers, licence plates and numeric domains are real assets. We help owners get fair value and help buyers find the exact pattern they want.</p>
    <ul class="breakdown" style="max-width:520px"><li><span>📈 Free, no-obligation valuations</span><b class="pos">Free</b></li><li><span>🔔 Pattern alerts (e.g. *888, no 4s)</span><b class="pos">Free</b></li><li><span>🤝 Private buyer–seller matching</span><b>Success fee only</b></li><li><span>🔒 Escrow for high-value deals</span><b>Available</b></li></ul>
    <div class="trust-row"><span>Confidential</span><span>Reply within 24h</span><span>Official transfer processes only</span></div>
  </div>
  <div id="lead">{lead_form(r)}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><span class="eyebrow">What we trade</span><h2>Three markets, one trusted desk</h2></div>
  <div class="grid g3">
    <div class="card"><div class="ico">📱</div><h3>Phone numbers</h3><p class="muted">Mobile and business numbers with 8s, 9s, repeats and power endings like 168 and 518.</p><a href="?asset=phone&intent=buy#lead">Request a phone number →</a></div>
    <div class="card"><div class="ico">🚗</div><h3>Licence plates</h3><p class="muted">Personalised and numeric plates — guidance for official auctions and legal transfers.</p><a href="?asset=plate&intent=buy#lead">Request a plate →</a></div>
    <div class="card"><div class="ico">🌐</div><h3>Numeric domains</h3><p class="muted">Short numeric .com and country domains prized by Chinese-language brands.</p><a href="?asset=domain&intent=buy#lead">Request a domain →</a></div>
  </div>
</div></section>
<section><div class="container">
  <div class="section-head"><span class="eyebrow">Pattern tiers</span><h2>How we grade lucky numbers</h2><p class="muted">Every request is scored with our <a href="../tools/number-analyzer.html">analyzer</a> plus comparable-sales research.</p></div>
  <div class="grid g4">{tiles}</div>
</div></section>
<section class="alt"><div class="container">
  <div class="section-head"><span class="eyebrow">How it works</span><h2>From request to transfer in 4 steps</h2></div>
  <div class="grid g4">
    <div class="card"><b class="mono" style="color:var(--red);font-size:1.6rem">01</b><h3>Tell us</h3><p class="muted" style="margin:0">Two-minute form. Buy, sell, value or alert.</p></div>
    <div class="card"><b class="mono" style="color:var(--red);font-size:1.6rem">02</b><h3>We research</h3><p class="muted" style="margin:0">Luck score, scarcity and comparable sales.</p></div>
    <div class="card"><b class="mono" style="color:var(--red);font-size:1.6rem">03</b><h3>We match</h3><p class="muted" style="margin:0">Private introductions to verified parties.</p></div>
    <div class="card"><b class="mono" style="color:var(--red);font-size:1.6rem">04</b><h3>Secure transfer</h3><p class="muted" style="margin:0">Escrow and official transfer processes.</p></div>
  </div>
</div></section>
<section><div class="container narrow"><h2>Exchange FAQ</h2>{faq_html(faqs)}
<p style="margin-top:24px"><a class="btn btn-primary" href="#lead">Start my request</a> <a class="btn btn-ghost" href="../guides/lucky-number-economy.html">Read market prices</a></p></div></section>'''
    write("exchange/index.html", page(path="exchange/index.html", title="Lucky Number Exchange — Buy, Sell & Value Lucky Phone Numbers, Plates & Numeric Domains", desc="Free valuations, pattern alerts and private matching for premium lucky phone numbers, licence plates and numeric domain names.", body=body, depth=1, active="exchange/index.html", sticky=False, modal=False,
          schema=[faq_schema([(q, a) for q, a in faqs]), {"@context": "https://schema.org", "@type": "Service", "name": "Lucky Number Exchange", "provider": {"@type": "Organization", "name": "008009.com"}, "areaServed": "Worldwide", "serviceType": "Premium number brokerage and valuation"}, breadcrumb_schema([("Lucky Number Exchange", "exchange/")])]))

def consult():
    r = ""
    services = [("naming", "🏷️", "Business number & name audit", "Phone, address, pricing and brand-name review for Chinese-speaking markets.", "from US$188"),
                ("date", "📅", "Auspicious date selection", "Weddings, openings, moves and signings — with almanac guidance.", "from US$88"),
                ("fengshui", "🧭", "Home / office feng shui referral", "Matched with a vetted practitioner in your city or online.", "quote"),
                ("personal", "🔢", "Personal lucky numbers report", "Birth-date based numbers, colours and directions — PDF report.", "from US$38")]
    cards = "".join(f'<div class="card"><div class="ico">{i}</div><h3>{t}</h3><p class="muted">{d}</p><p class="price" style="font-size:1.3rem">{p}</p><a class="btn btn-ghost btn-sm" href="?service={s}#book">Choose</a></div>' for s, i, t, d, p in services)
    form = simple_form(r, "Consultation booking", [
        ("service", "Service", "select", True, ["Business number & name audit", "Auspicious date selection", "Home / office feng shui referral", "Personal lucky numbers report", "Something else"]),
        NAME_EMAIL,
        ("_d", "", "row", False, [("birthdate", "Birth date (optional)", "date", False, ""), ("preferred_date", "Preferred consultation date", "date", False, "")]),
        ("goal", "What do you want to achieve?", "textarea", True, "e.g. choose an opening date in March for our restaurant in Vancouver")],
        "Request my consultation", "Thanks! We’ll confirm availability and pricing within 1–2 business days.")
    body = f'''{breadcrumb("", [("Consultations", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Consultations</span><h1>Expert guidance on numbers, dates & names</h1><p class="lead">For families and businesses entering Chinese-speaking markets — practical, respectful, and explained in plain English.</p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g4">{cards}</div><p class="form-note" style="margin-top:10px">Indicative launch pricing; final quote confirmed before any payment.</p></div></section>
<section class="alt" id="book"><div class="container narrow"><div class="section-head"><h2>Book a consultation</h2></div>{form}</div></section>'''
    write("consult.html", page(path="consult.html", title="Chinese Numerology, Lucky Date & Feng Shui Consultations", desc="Book a business number and name audit, auspicious date selection, feng shui referral or personal lucky numbers report.", body=body, depth=0,
          schema={"@context": "https://schema.org", "@type": "Service", "name": "Numerology & auspicious date consultations", "provider": {"@type": "Organization", "name": "008009.com"}}))

def videos():
    r = ""
    cards = "".join(video_card(v) for v in VIDEOS)
    body = f'''{breadcrumb(r, [("Videos", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Video library</span><h1>Lucky numbers & Chinese culture on video</h1><p class="lead">Hand-picked explainers from educators and broadcasters. Videos load only when you press play (privacy-enhanced mode).</p>
<p><a class="btn btn-primary btn-sm" data-yt-channel hidden target="_blank" rel="noopener">▶ Subscribe to our YouTube channel</a> <a class="btn btn-ghost btn-sm" href="contact.html?topic=video">Suggest a video</a></p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g3">{cards}</div></div></section>
{ad("inArticle")}
<section class="alt"><div class="container narrow center"><h2>Create with us</h2><p class="lead">We’re hiring bilingual video creators and hosts. Revenue share on sponsored episodes.</p><a class="btn btn-primary" href="careers.html">See roles</a> <a class="btn btn-ghost" href="advertise.html#video">Sponsor an episode</a>
<p class="form-note" style="margin-top:16px">All videos are embedded via YouTube’s official player and remain the property of their creators.</p></div></section>'''
    vs = [{"@context": "https://schema.org", "@type": "VideoObject", "name": v[1], "description": v[1] + " — " + v[2], "thumbnailUrl": f"https://i.ytimg.com/vi/{v[0]}/hqdefault.jpg", "embedUrl": f"https://www.youtube-nocookie.com/embed/{v[0]}", "uploadDate": "2020-01-01"} for v in VIDEOS[:0]]
    write("videos.html", page(path="videos.html", title="Videos: Lucky Numbers, Chinese Zodiac & Feng Shui", desc="Watch the best explainers on lucky number 8, unlucky 4, the Chinese zodiac, Chinese New Year and feng shui.", body=body, depth=0, active="videos.html"))

def guides_pages():
    r = "../"
    cards = "".join(f'<a class="card" href="{g[0]}.html"><span class="tag">{g[3]}</span> <span class="muted" style="font-size:.85rem">{g[4]} min read</span><h3 style="margin-top:10px">{esc(g[1])}</h3><p class="muted" style="margin:0">{esc(g[2])}</p></a>' for g in GUIDES)
    body = f'''{breadcrumb(r, [("Guides", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Guides & research</span><h1>Guides to lucky numbers, culture & markets</h1><p class="lead">Well-sourced explainers — from why 8 is lucky to what lucky numbers sell for.</p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g3">{cards}</div></div></section>{ad("inArticle")}'''
    write("guides/index.html", page(path="guides/index.html", title="Guides: Chinese Lucky Numbers, Zodiac, Feng Shui & the Lucky Number Market", desc="In-depth guides on Chinese number symbolism, lucky number prices, red envelope etiquette, zodiac and feng shui.", body=body, depth=1, active="guides/index.html", schema=breadcrumb_schema([("Guides", "guides/")])))
    for slug, title, desc, cat, mins, html_, faqs in GUIDES:
        # insert an ad after the 2nd h2
        parts = html_.split("<h2", 3)
        if len(parts) > 3:
            html_ = parts[0] + "<h2" + parts[1] + "<h2" + parts[2] + ad("inArticle") + "<h2" + parts[3]
        others = "".join(f'<li><a href="{g[0]}.html">{esc(g[1])}</a></li>' for g in GUIDES if g[0] != slug)
        body = f'''{breadcrumb(r, [("Guides", "guides/index.html"), (title, None)])}
<article class="container"><div class="article">
<header class="page-hero" style="padding-bottom:0"><span class="tag">{cat}</span><h1 style="margin-top:12px">{esc(title)}</h1><p class="lead">{esc(desc)}</p>
<div class="byline"><span>By the 008009 Editorial Team</span><span>·</span><span>Updated {TODAY}</span><span>·</span><span>{mins} min read</span></div></header>
{html_}
<h2>FAQ</h2>{faq_html(faqs)}
<div class="share-row" style="margin:24px 0"><button class="btn btn-ghost btn-sm" data-share="whatsapp" data-text="{esc(title)}">WhatsApp</button><button class="btn btn-ghost btn-sm" data-share="x" data-text="{esc(title)}">X</button><button class="btn btn-ghost btn-sm" data-share="facebook">Facebook</button><button class="btn btn-ghost btn-sm" data-share="linkedin">LinkedIn</button><button class="btn btn-ghost btn-sm" data-share="copy">Copy link</button></div>
<div class="cta-band" style="margin:30px 0"><div><h2 style="font-size:1.5rem">Put it to work</h2><p>Score your own number, or get a free valuation of a lucky number you own.</p></div><div style="display:grid;gap:10px"><a class="btn btn-gold" href="../tools/number-analyzer.html">Check my number</a><a class="btn btn-ghost" style="color:#fff;border-color:rgba(255,255,255,.4)" href="../exchange/index.html#lead">Free valuation</a></div></div>
<h3>More guides</h3><ul>{others}</ul>
</div></article>'''
        art = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@type": "Organization", "name": "008009 Editorial Team"}, "publisher": {"@type": "Organization", "name": "008009.com", "logo": {"@type": "ImageObject", "url": BASE + "assets/img/icon-512.png"}}, "mainEntityOfPage": BASE + f"guides/{slug}.html"}
        write(f"guides/{slug}.html", page(path=f"guides/{slug}.html", title=title, desc=desc, body=body, depth=1, active="guides/index.html", og_type="article",
              schema=[art, faq_schema(faqs), breadcrumb_schema([("Guides", "guides/"), (title, f"guides/{slug}.html")])]))

def contests():
    r = ""
    form = simple_form(r, "Contest entry", [
        ("contest", "Contest", "select", True, ["Lucky Number Story", "Lucky Plate & Number Photo", "Best Lucky Business Name", "Video Challenge"]),
        NAME_EMAIL,
        ("country", "Country", "text", True, "e.g. Canada"),
        ("entry_link", "Link to your entry (photo, video, or document)", "url", False, "https://…"),
        ("story", "Your entry / story (max ~300 words)", "textarea", True, "Tell us the story behind your lucky number…")],
        "Submit my entry", "Entry received — good luck! 🏮 Finalists are announced on this page and by email.",
        extra=f'<label class="check"><input type="checkbox" name="rules" value="accepted" required> I am 18+ (or have guardian consent) and accept the <a href="#rules">official rules</a>.</label>')
    body = f'''{breadcrumb(r, [("Contests", None)])}
<section class="hero" style="padding-top:28px"><div class="container hero-grid">
  <div><span class="eyebrow">Season 1 · Contests & prizes</span><h1>Share your <span class="hl">lucky number</span> story. Win prizes.</h1>
  <p class="lead">Every number has a story — the plate you waited years for, the phone number that brought you luck, the date you married. Tell us yours.</p>
  <div class="grid g2" style="margin-top:14px"><div class="stat"><b>US$888</b><span>target prize pool</span></div><div class="stat"><b>4</b><span>categories</span></div></div>
  <p class="form-note" style="margin-top:10px">Prize pool funded by sponsors and supporters — <a href="advertise.html#contest">sponsor a prize</a> or <a href="donate.html">contribute</a>.</p></div>
  <div class="hero-card" id="enter"><h2 style="font-size:1.4rem">Enter now — free</h2>{form}</div>
</div></section>
<section class="alt"><div class="container"><div class="section-head"><h2>Categories</h2></div><div class="grid g4">
<div class="card"><div class="ico">📖</div><h3>Lucky Number Story</h3><p class="muted" style="margin:0">A true story about a number that shaped your life or business.</p></div>
<div class="card"><div class="ico">📸</div><h3>Photo</h3><p class="muted" style="margin:0">Your best lucky plate, address or number photo (your own photo only).</p></div>
<div class="card"><div class="ico">🏷️</div><h3>Lucky Business Name</h3><p class="muted" style="margin:0">Invent a brand name + lucky number combo for a new business.</p></div>
<div class="card"><div class="ico">🎬</div><h3>Video Challenge</h3><p class="muted" style="margin:0">A 60-second video explaining a lucky number. Top entries featured on our channel.</p></div>
</div></div></section>
{ad("inArticle")}
<section id="rules"><div class="container narrow article"><h2>Official rules (summary)</h2><ol>
<li><b>No purchase necessary.</b> Free to enter. Void where prohibited.</li><li>Open to entrants worldwide aged 18+, or with guardian consent where permitted by law.</li>
<li>Entries must be original and owned by the entrant. By entering you grant 008009.com a non-exclusive licence to display the entry with credit.</li>
<li>Judging: 50% originality, 30% cultural insight, 20% community votes. Judges’ decisions are final.</li>
<li>Prizes (cash, gift cards or sponsor products) are confirmed when each season’s pool is funded; winners are notified by email and announced here.</li>
<li>We may disqualify entries that are offensive, infringing or fraudulent. Full terms: <a href="terms.html">Terms of Use</a>.</li></ol></div></section>'''
    write("contests.html", page(path="contests.html", title="Lucky Number Contests & Prizes", desc="Enter free contests — share your lucky number story, photo, business name or video and win prizes from our sponsor-funded prize pool.", body=body, depth=0, active="contests.html",
          schema={"@context": "https://schema.org", "@type": "Event", "name": "008009 Lucky Number Contest — Season 1", "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled", "startDate": TODAY, "location": {"@type": "VirtualLocation", "url": BASE + "contests.html"}, "organizer": {"@type": "Organization", "name": "008009.com", "url": BASE}}))

def careers():
    r = ""
    roles = [("Bilingual content writer (EN / 中文)", "Remote · Freelance", "Write guides and number pages; native-level Chinese and English."),
             ("Video creator / host", "Remote · Revenue share", "Short explainers for YouTube, TikTok and Reels."),
             ("Numerology & feng shui consultant", "Remote · Per session", "Deliver client consultations; experience required."),
             ("Growth & SEO marketer", "Remote · Part-time", "Programmatic SEO, newsletters and partnerships."),
             ("Front-end developer", "Remote · Contract", "Build new tools and features on our static stack."),
             ("Brand ambassador / community lead", "Remote · Commission", "Grow our community in your city or on WeChat, WhatsApp and Discord.")]
    cards = "".join(f'<div class="card"><span class="tag jade">{esc(t2)}</span><h3 style="margin-top:10px">{esc(t)}</h3><p class="muted">{esc(d)}</p><a class="btn btn-ghost btn-sm" href="?role={esc(t)}#apply">Apply</a></div>' for t, t2, d in roles)
    form = simple_form(r, "Job application", [
        ("role", "Role", "select", True, [x[0] for x in roles] + ["Open application"]),
        NAME_EMAIL,
        ("_l", "", "row", False, [("location", "Location / time zone", "text", True, "e.g. Toronto, UTC−5"), ("languages", "Languages", "text", False, "e.g. English, Mandarin, Cantonese")]),
        ("portfolio", "Portfolio / LinkedIn / CV link", "url", False, "https://…"),
        ("pitch", "Why you — and one idea for 008009.com", "textarea", True, "A few sentences…")],
        "Send application", "Application received — thank you! We review every application and reply within two weeks.")
    body = f'''{breadcrumb(r, [("Careers", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Careers & talent</span><h1>Build the world’s home for lucky numbers</h1><p class="lead">Remote-first, bilingual, and culture-driven. We’re looking for writers, creators, consultants and builders.</p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g3">{cards}</div></div></section>
<section class="alt" id="apply"><div class="container narrow"><div class="section-head"><h2>Apply</h2><p class="muted">Don’t see your role? Send an open application.</p></div>{form}</div></section>'''
    jobs = [{"@context": "https://schema.org", "@type": "JobPosting", "title": t, "description": d, "datePosted": TODAY, "validThrough": (datetime.date.today() + datetime.timedelta(days=90)).isoformat(), "employmentType": "CONTRACTOR", "jobLocationType": "TELECOMMUTE", "applicantLocationRequirements": {"@type": "Country", "name": "Worldwide"}, "hiringOrganization": {"@type": "Organization", "name": "008009.com", "sameAs": BASE}} for t, t2, d in roles]
    write("careers.html", page(path="careers.html", title="Careers — Writers, Video Creators, Consultants & Developers", desc="Join 008009.com: remote roles for bilingual writers, video creators, numerology consultants, marketers and developers.", body=body, depth=0, active="careers.html", schema=jobs))

def advertise():
    r = ""
    packs = [("Lucky Number of the Day", "US$88", "/ week", ["Logo + link on homepage module", "Mention in daily email", "Social post"], False, "lnotd"),
             ("Tool sponsor", "US$388", "/ month", ["“Presented by” on one tool", "Branded result-card footer", "Monthly performance report"], True, "tool"),
             ("Category exclusive", "US$888", "/ month", ["Own a category (e.g. weddings, property)", "Sponsored guide", "Exclusive ad placements"], False, "category"),
             ("Contest / prize sponsor", "Custom", "", ["Naming rights for a season", "Prize showcase", "Entrant opt-in leads (with consent)"], False, "contest")]
    cards = "".join(f'<div class="card plan{" featured" if f else ""}"><h3>{t}</h3><p class="price">{p}<small> {per}</small></p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="btn {"btn-primary" if f else "btn-ghost"} btn-block" href="?package={k}#inquire">Choose</a></div>' for t, p, per, li, f, k in packs)
    form = simple_form(r, "Advertising / sponsorship / partnership inquiry", [
        ("package", "Interest", "select", True, ["Lucky Number of the Day", "Tool sponsor", "Category exclusive", "Contest / prize sponsor", "Video sponsorship", "Affiliate / partnership", "Buy or invest in this website/domain", "Other"]),
        NAME_EMAIL,
        ("_c", "", "row", False, [("company", "Company", "text", True, "Company name"), ("website", "Website", "url", False, "https://…")]),
        ("budget", "Monthly budget", "select", False, ["Not sure yet", "Under $500", "$500 – $2,000", "$2,000 – $10,000", "$10,000+"]),
        ("message", "Goals & audience", "textarea", True, "What would you like to promote, and to whom?")],
        "Send inquiry", "Thanks! Our partnerships team will send a media kit within 1–2 business days.")
    body = f'''{breadcrumb(r, [("Advertise", None)])}
<section class="page-hero"><div class="container"><span class="eyebrow">Advertise · Sponsor · Partner</span><h1>Reach people who care about prosperity</h1><p class="lead">Our audience plans weddings, buys property, launches businesses and chooses phone numbers — high-intent moments for jewellers, banks, real-estate, telecom, travel and Asian-market brands.</p>
<p><a class="btn btn-primary" href="#inquire">Request media kit</a> <a class="btn btn-ghost" href="https://web.works/contact" data-interest target="_blank" rel="noopener">Acquire / invest in this site</a></p></div></section>
<section style="padding-top:0"><div class="container"><div class="grid g4">{cards}</div><p class="form-note" style="margin-top:10px">Launch pricing — lucky, and subject to change. All sponsored content is clearly labelled.</p></div></section>
<section class="alt" id="partner"><div class="container"><div class="grid g3">
<div class="card" id="video"><div class="ico">🎬</div><h3>Video sponsorship</h3><p class="muted" style="margin:0">Integrated mentions in explainers and shorts across YouTube and social.</p></div>
<div class="card"><div class="ico">🤝</div><h3>Affiliate & referral</h3><p class="muted" style="margin:0">Carriers, plate dealers, domain registrars, feng shui retailers, language schools and travel.</p></div>
<div class="card" id="contest"><div class="ico">🏆</div><h3>Contest partners</h3><p class="muted" style="margin:0">Fund a prize, get naming rights and consented leads.</p></div>
</div></div></section>
<section id="inquire"><div class="container narrow"><div class="section-head"><h2>Start a partnership</h2></div>{form}</div></section>'''
    write("advertise.html", page(path="advertise.html", title="Advertise, Sponsor & Partner with 008009.com", desc="Sponsorship packages, video sponsorships, affiliate partnerships and contest partnerships on 008009.com.", body=body, depth=0, active="advertise.html"))

def donate():
    r = ""
    uses = [("Operations & hosting", 30), ("Promotions & marketing", 25), ("Hiring bilingual talent", 25), ("Contests & prizes", 20)]
    bars = "".join(f'<div style="display:flex;justify-content:space-between"><span>{u}</span><b>{p}%</b></div><div class="bar"><i style="width:{p}%"></i></div>' for u, p in uses)
    amts = "".join(f'<button type="button" class="chip" data-amount-pick="{a}" aria-pressed="false">${a}</button>' for a in (8, 18, 38, 88, 168, 888))
    form = simple_form(r, "Donation pledge", [
        ("_a", "", "row", True, [("amount", "Amount (USD)", "number", True, "88"), ("frequency", "Frequency", "select", True, ["One-time", "Monthly", "Yearly"])]),
        ("method", "Preferred method", "select", True, ["stripe", "paypal", "kofi", "buymeacoffee", "bank transfer", "crypto", "other"]),
        NAME_EMAIL,
        ("purpose", "Direct my support to (optional)", "select", False, ["Where it’s needed most", "Operations & hosting", "Promotions & marketing", "Hiring talent", "Contests & prizes"]),
        ("message", "Message (optional)", "textarea", False, "Say something nice…"),
        ("public_name", "Show my name on the supporter wall?", "select", False, ["Yes, show my name", "No, keep me anonymous"])],
        "Send pledge — we’ll email a secure payment link", "Thank you! 🧧 We’ll email you a secure payment link within 24 hours.")
    form = form.replace('<form class="form card"', '<form class="form card" id="pledge"', 1)
    body = f'''{breadcrumb(r, [("Support", None)])}
<section class="hero" style="padding-top:28px"><div class="container hero-grid">
  <div><span class="eyebrow">Support 008009</span><h1>Help keep lucky-number tools <span class="hl">free</span> for everyone.</h1>
  <p class="lead">Your support funds hosting, bilingual content, promotions, new hires and the prize pool for community contests.</p>
  <div class="chips" style="margin-top:14px">{amts}</div>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">
    <a class="btn btn-primary" href="#pledge" data-pay="stripe" data-amount="88">💳 Card (Stripe)</a>
    <a class="btn btn-ghost" href="#pledge" data-pay="paypal" data-amount="38">PayPal</a>
    <a class="btn btn-ghost" href="#pledge" data-pay="kofi" data-amount="18">☕ Ko-fi</a>
    <a class="btn btn-ghost" href="#pledge" data-pay="buymeacoffee" data-amount="8">Buy us a coffee</a>
    <a class="btn btn-ghost" href="#pledge" data-pay="githubSponsors" data-amount="18">GitHub Sponsors</a>
  </div>
  <p class="form-note" style="margin-top:10px">008009.com is an independent website, not a registered charity; contributions are not tax-deductible.</p></div>
  <div class="hero-card"><h2 style="font-size:1.3rem">Where your support goes</h2>{bars}
  <h3 style="margin-top:18px">Supporter perks</h3><ul class="breakdown"><li><span>🧧 $8+ — Supporter wall + thank-you card</span></li><li><span>🏮 $38+/mo — Ad-free experience & early tool access</span></li><li><span>🐉 $168+/mo — Monthly lucky numbers PDF + Q&A</span></li><li><span>👑 $888 — Founding patron: name on About page</span></li></ul></div>
</div></section>
<section class="alt"><div class="container narrow"><div class="section-head"><h2>Make a pledge</h2><p class="muted">Choose any method — we’ll send a secure payment link. No card details are collected on this site.</p></div>{form}</div></section>'''
    write("donate.html", page(path="donate.html", title="Support 008009.com — Donate", desc="Support free lucky-number tools and culture guides. Donations fund operations, promotions, marketing, hiring talent and contest prizes.", body=body, depth=0, active="donate.html", sticky=False))

def about():
    r = ""
    body = f'''{breadcrumb(r, [("About", None)])}
<section class="page-hero"><div class="container narrow article"><span class="eyebrow">About</span><h1>About 008009.com</h1>
<p class="lead">008009.com is an independent website about lucky numbers in Chinese culture — how they work, why they matter, and what they’re worth.</p>
<h2>Our name</h2><p>Read by sound, <b class="mono">008009</b> is a blessing: zeros for wholeness, <b>8</b> for prosperity (发) and <b>9</b> for longevity (久) — <em>complete prosperity that lasts</em>. <a href="guides/meaning-of-008009.html">Read the full breakdown</a>.</p>
<h2>What we do</h2><ul><li><b>Free tools</b> that explain the luck in any number.</li><li><b>Guides</b> grounded in culture and real market data.</li><li><b>The Lucky Number Exchange</b> — valuations, alerts and private matching for phone numbers, plates and numeric domains.</li><li><b>Community</b> contests, videos and a daily lucky number.</li></ul>
<h2 id="method">Editorial standards & method</h2><p>Meanings are based on widely documented Mandarin and Cantonese homophones and customs. Market figures cite public reports. Luck scores are transparent formulas (<a href="tools/number-analyzer.html#main">see the method</a>) — for culture and entertainment, never guarantees.</p>
<h2>Revenue & independence</h2><p>We’re funded by advertising, sponsorships (always labelled), affiliate partnerships, consultations, Exchange commissions and supporters. Sponsors never influence meanings or scores.</p>
<p><a class="btn btn-primary" href="contact.html">Contact us</a> <a class="btn btn-ghost" href="https://web.works/contact" data-interest target="_blank" rel="noopener">Domain / partnership inquiries</a></p></div></section>'''
    write("about.html", page(path="about.html", title="About 008009.com", desc="About 008009.com — an independent guide to lucky numbers in Chinese culture and a trusted lucky number exchange.", body=body, depth=0))

def contact():
    r = ""
    form = simple_form(r, "General contact", [
        ("topic", "Topic", "select", True, ["General question", "Lucky Number Exchange", "Consultation", "Advertising / sponsorship", "Partnership", "Buy / invest in this website or domain", "Press", "Correction", "Video suggestion", "Other"]),
        NAME_EMAIL,
        ("message", "Message", "textarea", True, "How can we help?")], "Send message")
    body = f'''{breadcrumb(r, [("Contact", None)])}
<section class="page-hero"><div class="container narrow"><span class="eyebrow">Contact</span><h1>Get in touch</h1><p class="lead">Questions, corrections, partnerships or press — we read every message.</p>
<div class="grid g3" style="margin:20px 0">
<a class="card" href="exchange/index.html#lead"><h3>Exchange</h3><p class="muted" style="margin:0">Buy, sell or value a number →</p></a>
<a class="card" href="advertise.html#inquire"><h3>Advertising</h3><p class="muted" style="margin:0">Media kit & sponsorships →</p></a>
<a class="card" href="https://web.works/contact" data-interest target="_blank" rel="noopener"><h3>This domain</h3><p class="muted" style="margin:0">Acquisition & partnership →</p></a></div>
{form}
<p class="form-note" style="margin-top:14px">Prefer email? <a href="#" data-email-link="Inquiry via 008009.com">Click here to email us</a> (opens your mail app).</p></div></section>'''
    write("contact.html", page(path="contact.html", title="Contact 008009.com", desc="Contact 008009.com about the Lucky Number Exchange, consultations, advertising, partnerships or press.", body=body, depth=0, modal=False))

def legal():
    r = ""
    upd = TODAY
    privacy = f'''<h1>Privacy Policy</h1><p class="muted">Last updated {upd}</p>
<p>This policy explains what 008009.com (“we”) collects and why.</p>
<h2>What we collect</h2><ul><li><b>Form submissions</b> (name, email, optional phone and message) — only what you enter, used to answer your request. Submissions are relayed by our form-processing provider (FormSubmit) to our private inbox.</li><li><b>Tool inputs</b> — numbers and dates you enter into calculators are processed in your browser and are not sent to us.</li><li><b>Cookies & similar technologies</b> — see below.</li></ul>
<h2 id="cookies">Cookies, analytics & advertising</h2><p>With your consent we may use Google Analytics and Google AdSense. Google and its partners use cookies to serve ads based on your prior visits to this and other websites. You can opt out of personalised advertising at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. If you choose “Essential only”, we request non-personalised ads. We store your consent choice and theme preference in your browser’s local storage. See <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses data from partner sites</a>.</p>
<h2>Embedded content</h2><p>Videos are embedded from YouTube in privacy-enhanced mode and load only when you press play. YouTube’s own policies then apply.</p>
<h2>Sharing</h2><p>We never sell personal information. We share it only with service providers needed to operate the site, or when required by law. For Exchange requests, we introduce parties only with your approval.</p>
<h2>Retention & your rights</h2><p>We keep inquiries for as long as needed to handle them and meet legal obligations. Depending on where you live (e.g. GDPR, UK GDPR, PIPEDA, CCPA/CPRA), you may request access, correction or deletion of your data — use the <a href="contact.html">contact form</a>.</p>
<h2>Children</h2><p>This site is not directed at children under 13, and we do not knowingly collect their data.</p>
<h2>Changes</h2><p>We’ll post updates on this page with a new date.</p>'''
    terms = f'''<h1>Terms of Use</h1><p class="muted">Last updated {upd}</p>
<h2>1. Acceptance</h2><p>By using 008009.com you agree to these terms.</p>
<h2>2. Information only</h2><p>All content, scores and tools are for cultural, educational and entertainment purposes. They are not financial, investment, legal, medical or professional advice, and no outcome is guaranteed.</p>
<h2>3. Lucky Number Exchange</h2><p>We provide introductions, research and valuation opinions. Valuations are estimates, not appraisals. Every transfer must follow the rules of the relevant carrier, licensing authority or domain registrar. Commission terms are agreed in writing before any brokered sale. We do not trade numbers where transfer is prohibited.</p>
<h2>4. Contests</h2><p>Contests are free to enter and subject to their posted rules. Void where prohibited.</p>
<h2>5. Donations</h2><p>Contributions are voluntary, support the operation of this website, and are generally non-refundable. 008009.com is not a registered charity; contributions are not tax-deductible.</p>
<h2>6. User submissions</h2><p>You confirm you own what you submit and grant us a non-exclusive licence to use it for the purpose you submitted it.</p>
<h2>7. Intellectual property</h2><p>See our <a href="disclaimer.html">Trademark & Copyright disclosure</a>.</p>
<h2>8. Limitation of liability</h2><p>The site is provided “as is”. To the extent permitted by law, we are not liable for decisions made based on its content.</p>
<h2>9. Contact</h2><p>Use the <a href="contact.html">contact form</a>.</p>'''
    disclaimer = f'''<h1>Trademark & Copyright Disclosure</h1><p class="muted">Last updated {upd}</p>
<h2>Use of “008009”</h2><p>“008009” is a string of digits used on this website solely as a <b>descriptive numeric domain name</b> (008009.com) and as a reference to its cultural reading (prosperity and longevity). 008009.com is <b>not affiliated with, sponsored by, or endorsed by</b> any company, product, service, telephone operator, government body, film, game, or trademark owner that uses the same or similar numbers, codes or dialling prefixes (including international call prefixes such as “00” and country code “86”). No claim to any third party’s trademark is made or implied.</p>
<h2>Third-party marks</h2><p>Names of companies, websites, carriers, registrars, platforms (e.g. YouTube, Google, WeChat, WhatsApp) and brands mentioned are trademarks of their respective owners and are used for identification and commentary only (nominative fair use).</p>
<h2>Copyright</h2><p>Original text, tools, code, graphics and the 008·009 logo mark on this site are © {datetime.date.today().year} 008009.com. All rights reserved. Cultural facts, number meanings and public-domain traditions are not claimed as proprietary.</p>
<h2>Embedded & cited content</h2><p>Videos are embedded using YouTube’s official embed player; all rights remain with their creators and YouTube. Market figures and facts are cited to their original publishers with links; quotations are brief and used for commentary and education.</p>
<h2>No images copied</h2><p>Graphics on this site are original SVG/CSS artwork or thumbnails served directly by YouTube for embedded videos.</p>
<h2>Report a concern</h2><p>If you believe content on this site infringes your rights, please use the <a href="contact.html?topic=Other">contact form</a> with details and we will review and respond promptly (including removal where appropriate).</p>
<h2>Not advice</h2><p>Number symbolism is presented as cultural tradition and entertainment, not as financial or professional advice.</p>'''
    for slug, title, content, desc in [("privacy", "Privacy Policy", privacy, "How 008009.com handles personal data, cookies, analytics and advertising."),
                                       ("terms", "Terms of Use", terms, "Terms of use for 008009.com, the Lucky Number Exchange, contests and donations."),
                                       ("disclaimer", "Trademark & Copyright Disclosure", disclaimer, "Trademark and copyright disclosure: 008009.com is an independent descriptive numeric domain, not affiliated with any brand.")]:
        body = f'{breadcrumb(r, [(title, None)])}<section class="page-hero"><div class="container article">{content}</div></section>'
        write(f"{slug}.html", page(path=f"{slug}.html", title=title, desc=desc, body=body, depth=0, modal=False, sticky=False))

def notfound():
    body = '''<section class="page-hero"><div class="container narrow center"><p class="mono" style="font-size:5rem;color:var(--red);margin:0">404</p><h1>This number doesn’t exist (yet)</h1><p class="lead">In Chinese, 404 is doubly unlucky — let’s get you somewhere better.</p>
<p><a class="btn btn-primary" href="/008009-com/index.html">Go home</a> <a class="btn btn-ghost" href="/008009-com/tools/number-analyzer.html">Check a number</a></p></div></section>'''
    html_ = page(path="404.html", title="Page not found", desc="Page not found.", body=body, depth=0, noindex=True, modal=False, sticky=False)
    # 404 is served from any path — use absolute base paths
    from urllib.parse import urlparse
    prefix = urlparse(BASE).path  # e.g. /008009-com/
    html_ = html_.replace('href="assets/', f'href="{prefix}assets/').replace('src="assets/', f'src="{prefix}assets/').replace('href="manifest', f'href="{prefix}manifest').replace('data-base=""', f'data-base="{prefix}"')
    for p in ["index.html", "tools/", "numbers/", "zodiac/", "exchange/", "videos.html", "guides/", "contests.html", "advertise.html", "careers.html", "donate.html", "about.html", "contact.html", "privacy.html", "terms.html", "disclaimer.html", "consult.html"]:
        html_ = html_.replace(f'href="{p}', f'href="{prefix}{p}')
    html_ = html_.replace("/008009-com/", prefix)
    write("404.html", html_)

def extras():
    urls = [p for p in WRITTEN if p.endswith(".html") and p != "404.html"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(urls):
        loc = BASE + ("" if p == "index.html" else p.replace("index.html", ""))
        pr = "1.0" if p == "index.html" else "0.8" if p.count("/") == 0 or p.endswith("index.html") else "0.6"
        sm.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    write("manifest.webmanifest", json.dumps({"name": "008009 — Lucky Numbers Hub", "short_name": "008009", "start_url": "./index.html", "display": "standalone", "background_color": "#fbf8f3", "theme_color": "#B3131B",
                                               "icons": [{"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=1))
    sw = """/* 008009.com service worker — offline tools */
const C='008009-v%s';const CORE=['./','./index.html','./tools/number-analyzer.html','./assets/css/style.css','./assets/js/config.js','./assets/js/numerology.js','./assets/js/main.js','./assets/js/tools.js'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(e.request.method!=='GET'||u.origin!==location.origin)return;
e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./index.html'))))});
""" % (L.VERSION + "-" + TODAY)
    write("sw.js", sw)
    if not os.path.exists(os.path.join(ROOT, "ads.txt")):
        write("ads.txt", "# Replace pub-0000000000000000 with your AdSense publisher ID, then uncomment:\n# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
    write(".nojekyll", "")

if __name__ == "__main__":
    home(); tools_hub(); tools_all(); numbers_pages(); zodiac_pages(); exchange(); consult(); videos(); guides_pages()
    contests(); careers(); advertise(); donate(); about(); contact(); legal(); notfound(); extras()
    print(f"Built {len(WRITTEN)} files → {ROOT}  (base {BASE})")
