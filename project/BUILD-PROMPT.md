# 008009.com — Phase-Wise Master Build Prompt

Paste each phase into Claude (or any capable AI coding agent) in order. Each phase is self-contained and builds on the one before it. Phases 0–7 are **already implemented** in this repository. Phases 8–10 are the expansion roadmap.

---

## GLOBAL CONTEXT (prepend to every phase)

> You are building **008009.com — The Global Lucky Numbers Hub**, a static, SEO-first website hosted free on **GitHub Pages** (repo `WEBWORKSA1/008009-com`, no server, no database, no paid services required).
> **Concept:** free Chinese-numerology tools and content drive traffic. The **Lucky Number Exchange** (valuations, pattern alerts, buyer/seller matching for lucky phone numbers, licence plates and numeric domains) converts that traffic into high-value leads.
> **Name meaning:** 00 (wholeness) · 8 (八 ≈ 发, prosperity) · 00 · 9 (九 ≈ 久, longevity) = "prosperity that lasts".
> **Hard rules:**
> 1. Every page's top bar must read "Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership", linked to `https://web.works/contact`.
> 2. The only contact email is the owner's private inbox. It must NEVER appear in HTML, text, meta, sitemap or readable JS. Store it XOR-encoded as char codes and decode it at runtime only to build the FormSubmit AJAX endpoint or a click-to-email `mailto:`. Links show only labels like "Email us".
> 3. All forms POST via `fetch` to `https://formsubmit.co/ajax/<decoded>`, with a honeypot, `_subject`, `_template=table` and `_replyto`. Fall back to `mailto:` if the POST fails.
> 4. Avoid trademark or copyright conflicts: the site is not affiliated with any brand using "008009", there are no Bond/"007"-style references, graphics are original SVG/CSS, and videos are embedded only via YouTube's official player. Publish a Trademark & Copyright Disclosure page and a footer disclaimer.
> 5. Content is cultural/educational/entertainment. It is not financial advice.
> 6. The site is responsive at 360px with no horizontal scroll, supports dark mode, meets WCAG AA contrast, and loads fast (no frameworks; vanilla JS; Google Fonts only).
> **Design system:** lacquer red `#B3131B` (primary CTAs only), antique gold `#C9A227` (scores/badges), jade `#1f8a5b` (good results), ink `#1b1714`, paper `#fbf8f3`. Headings use Noto Serif SC, the UI uses Inter, and numbers use a monospace font.

---

## PHASE 0 — Research & positioning ✅
Research what 008009 means (digits, homophones, 00 prefix, 发久) and the economics of lucky numbers (record phone, plate and numeric-domain sales, with citations). Score 4+ business ideas on traffic, RPM, lead value and fit with the name, and pick one. Visit 25+ comparable sites (astrology, numerology, Chinese zodiac, feng shui, vanity phone numbers, plates, numeric domains, calculators, donation platforms) and extract features, forms, ad placements and design patterns. **Output:** `project/RESEARCH.md`.

## PHASE 1 — Architecture & design system ✅
Create a Python static generator (`build/build.py`, `build/layout.py`, `build/data.py`, `build/guides.py`) that writes plain HTML to the repo root with **relative links** (so it works at `/008009-com/` and at a custom domain). Shared layout: top interest bar, sticky header (brand, nav, "Free valuation" CTA, dark-mode toggle, mobile drawer), footer (newsletter, 4 link columns, legal disclaimer), cookie-consent banner, exit-intent valuation modal, sticky mobile CTA. Write `assets/css/style.css` with design tokens, a light/dark theme and components (cards, chips, dial, digit tiles, multi-step form, tables, pricing, countdown, ad slots). **Acceptance:** Lighthouse ≥ 90 on mobile, no horizontal overflow at 390px.

## PHASE 2 — Numerology engine & tools ✅
`assets/js/numerology.js`: digit weights (8 +10, 9 +7, 6 +6, 2 +3, 3 +2, 0/1 +1, 7 0, 5 −1, 4 −10, scaled for length), combination rules (168, 518, 888, 520, 1314, 89… positive; 14, 24, 74, 44, 250 negative; 4 inside 1314 exempt), ending bonus/penalty, patterns (repeats, ABAB, ascending, palindrome, no-4), logistic mapping to 1–99, tiers, `suggest()` for luckier variants, `generate()`, and the lunar calendar via `Intl` `ca-chinese` with a verified CNY override table.
`assets/js/tools.js` provides the tools:
- **Analyzer**: type chips, score dial, digit tiles, breakdown, luckier variations, a canvas **share card** PNG, WhatsApp/X/Facebook/copy, and an Exchange CTA.
- **Compare two numbers**.
- **Zodiac finder** (lunar-accurate) and **compatibility** (trines, six harmonies, clashes).
- **Lucky date checker**: Ghost Month, 8/8, Double Nine, 5/20.
- **Red envelope & lucky price** generator.
- **Lucky number generator**.
- **Kua number**: Li Chun boundary; East/West groups; 4 directions.
- **Lucky Number of the Day**.

## PHASE 3 — Programmatic SEO content ✅
- `numbers/{n}.html` for 0–99 plus ~45 curated specials (00, 88, 168, 518, 520, 1314, 5201314, 250, 666, 888, 999, 8888, 9420, 008009…). Each page has its meaning, a digit table, an embedded pre-filled analyzer, an Exchange CTA (swap offer for unlucky numbers, pattern alert for lucky ones), a 3-question FAQ with FAQPage schema, related links, share buttons and breadcrumbs.
- `zodiac/{animal}.html` ×12: traits, lucky numbers and colours, matches, clash, a year table from 1924–2044 with elements, FAQ.
- `guides/*.html` ×8 long-form articles with sources, a table of contents style, Article + FAQ schema and an in-article ad after the 2nd H2.
- `sitemap.xml`, `robots.txt`, canonical, Open Graph and Twitter cards, WebSite SearchAction, Organization, WebApplication, Service, Event and JobPosting schema.

## PHASE 4 — Lead generation (the money engine) ✅
- `exchange/index.html`: hero value list plus a **3-step form**. Step 1 is intent (buy/sell/valuation/alert) and auto-advances. Step 2 asks for asset, region, number/pattern, budget and timeline. Step 3 asks for name, email, phone/WhatsApp, preferred contact channel (WhatsApp/WeChat), message and consent. It has a progress bar, trust microcopy, query-string prefill (`?intent=&asset=&number=`), pattern tiers, a 4-step "how it works" and an FAQ with schema.
- Lead capture everywhere: exit-intent modal ("What is your lucky number worth?"), sticky mobile CTA, CTAs on analyzer results and every number page, newsletter in the footer, consultations booking form (`consult.html`).
- Track `generate_lead`, `lead_step`, `analyze_number`, `share`, `video_play` in GA4 once configured.

## PHASE 5 — Monetization surfaces ✅
- `assets/js/config.js` is a single switchboard: `adsenseClient`, `adSlots`, `ga4Id`, `youtubeChannelUrl`, `payments.{stripe,paypal,kofi,buymeacoffee,githubSponsors}`, `social.*`.
- Ad slots: labelled, reserved height (no layout shift), never on the Exchange, legal or donate pages. Rotating **house ads** show until AdSense is approved. Loading is consent-aware (non-personalised ads on "Essential only").
- `videos.html`: 12 oEmbed-verified YouTube videos behind click-to-load facades (youtube-nocookie) and a channel subscribe button.
- `advertise.html`: 4 priced packages, plus video, affiliate and contest partnerships, plus a media-kit inquiry form.
- `donate.html`: preset amounts ($8/18/38/88/168/888), five payment buttons (they fall back to the pledge form until links are configured), a use-of-funds breakdown (operations 30%, promotions/marketing 25%, hiring 25%, contests/prizes 20%), perk tiers and a pledge form. States clearly that the site is not a charity.
- `contests.html`: 4 categories, a US$888 target prize pool funded by sponsors, an entry form with rules consent, and summary official rules ("no purchase necessary").
- `careers.html`: 6 remote roles with JobPosting schema and an application form.

## PHASE 6 — Trust, legal & compliance ✅
`about.html` (method and independence), `contact.html` (topic router plus a hidden-email click link), `privacy.html` (FormSubmit, Google AdSense/Analytics cookie disclosures and opt-out links, GDPR/PIPEDA/CCPA rights), `terms.html` (Exchange, contests, donations), `disclaimer.html` (**Trademark & Copyright Disclosure**), `404.html` (absolute paths), `ads.txt` template, PWA `manifest.webmanifest`, icons, OG image, and a `sw.js` offline cache.

## PHASE 7 — QA & deploy ✅
Playwright checks: every page returns 200, no console errors, no horizontal overflow at 390px, the top bar links to web.works/contact, tools produce results, the multi-step form posts to the decoded endpoint (network mocked), and a grep confirms the email never appears. Push the sources to `main`. The GitHub Actions workflow (`.github/workflows/deploy.yml`) runs `build/images.py` and `build/build.py`, then publishes the output to the `gh-pages` branch, which GitHub Pages serves (free plan, public repo). Confirm the site is live at https://webworksa1.github.io/008009-com/.

---

## PHASE 8 — Owner go-live checklist (manual, ~30 minutes)
1. **Activate forms:** submit any form once on the live site. FormSubmit sends a one-time activation email to the private inbox. Click **Activate**.
2. **Custom domain:** point 008009.com DNS to GitHub Pages (A records 185.199.108.153, .109.153, .110.153, .111.153; CNAME `www` → `webworksa1.github.io`). Add the domain in repo Settings → Pages, tick "Enforce HTTPS", then add a `CNAME` file containing `008009.com` to `main`. CI then rebuilds with that base URL, which updates canonicals and the sitemap.
3. **AdSense:** apply, paste `ca-pub-…` into `config.js`, update `ads.txt`, add a Google-certified CMP for EEA/UK traffic.
4. **Payments:** create Stripe Payment Links / Ko-fi / BMC. Paste the URLs into `config.js`.
5. **Search Console + Bing Webmaster:** verify the site and submit `sitemap.xml`.
6. **GA4:** paste the ID into `config.js`.

## PHASE 9 — Growth expansion (next build prompt)
> Extend the generator with:
> - (a) `numbers/100-999` programmatic pages (900 more), each with a computed score shown in HTML (port the engine to Python so scores are in the static HTML for SEO).
> - (b) `born-in/{1924..2035}.html` birth-year pages.
> - (c) `compatibility/{a}-and-{b}.html` (78 pairs).
> - (d) `chinese-new-year/{yyyy}.html` with countdown.
> - (e) Simplified and Traditional Chinese versions (`/zh-hans/`, `/zh-hant/`) with hreflang.
> - (f) a JSON "listings" file and a filterable Exchange inventory grid (pattern, price band, region, score) with "Make offer" on each card.
> - (g) a daily auto-rotating "Lucky Number of the Day" via a GitHub Action cron that rebuilds and commits.
> - (h) a supporter wall rendered from `data/supporters.json`.
> - (i) a contest gallery from `data/entries.json`.
> - (j) an RSS feed for guides.
> Keep every hard rule from the Global Context.

## PHASE 10 — Scale & monetization upgrades
- Move forms to a serverless backend (Cloudflare Workers free tier) with a CRM export (Google Sheets / Airtable) and automatic lead scoring (budget × asset × intent).
- Stripe Checkout for consultations. Escrow partner integration for Exchange deals over $2,000.
- A membership tier (ad-free, monthly lucky-numbers PDF) via Memberful, Ko-fi or GitHub Sponsors.
- A YouTube Shorts pipeline: one short per number page, embedded back on that page.
- Programmatic `vanity-numbers/{city}` and `plates/{region}` pages linked to Exchange demand.
- A/B test the hero headline and form step order. Target: ≥ 3% visitor → lead on the Exchange, ≥ 0.5% site-wide.
