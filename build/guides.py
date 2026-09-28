"""Long-form guides (slug, title, description, category, minutes, html body, faqs)."""

SRC = {
    "olympics": ("2008 Summer Olympics opening ceremony — Wikipedia", "https://en.wikipedia.org/wiki/2008_Summer_Olympics_opening_ceremony"),
    "gwr": ("The bizarre story of the world’s most expensive phone number — Guinness World Records", "https://www.guinnessworldrecords.com/news/2026/2/the-bizarre-story-of-the-worlds-most-expensive-phone-number"),
    "kwik": ("The Most Valuable License Plates in Hong Kong — Kwiksure", "https://www.kwiksure.com/blog/top-priced-car-plate-number-hong-kong/"),
    "w": ("HK$26M splurged on “W” vanity plate — TransitJam", "https://transitjam.com/2021/03/08/hk26m-splurged-on-w-vanity-plate-smashing-hk-record/"),
    "mo": ("Numeric domain value in Chinese culture — MediaOptions", "https://mediaoptions.com/blog/understanding-numeric-domain-value-in-chinese-culture/"),
    "cli": ("Chinese Numerology — CLI", "https://studycli.org/chinese-culture/chinese-numerology/"),
    "cnn": ("Hong Kong’s vanity car plates — CNN", "https://www.cnn.com/style/article/hong-kong-auctioned-vanity-car-plates-intl-hnk/index.html"),
    "td": ("Vehicle registration marks — Hong Kong Transport Department", "https://www.td.gov.hk/en/public_services/vehicle_registration_mark/index.html"),
    "ch": ("Chinese New Year dates — China Highlights", "https://www.chinahighlights.com/travelguide/festivals/when-chinese-new-year.htm"),
}

def sources(*keys):
    return '<h2>Sources</h2><ol>' + "".join(f'<li><a href="{SRC[k][1]}" target="_blank" rel="noopener nofollow">{SRC[k][0]}</a></li>' for k in keys) + '</ol>'

GUIDES = [
("meaning-of-008009", "What does 008009 mean? Prosperity that lasts", "Breaking down 008009 through Chinese number symbolism: zeros for wholeness, 8 for prosperity, 9 for longevity — and why it makes a memorable global brand.", "Culture", 6, """
<p>At first glance <b class="mono">008009</b> looks like a code. Read the way a Chinese speaker reads numbers — by sound and symbol — it becomes a short blessing: <b>complete prosperity that lasts</b>.</p>
<h2 id="parts">Reading it piece by piece</h2>
<div class="table-wrap"><table><thead><tr><th>Part</th><th>Character</th><th>Sounds like / symbol</th><th>Meaning</th></tr></thead><tbody>
<tr><td class="mono">00</td><td>零零</td><td>圆满 wholeness; 00 is mainland China’s international call prefix</td><td>Completeness, a gateway to the world</td></tr>
<tr><td class="mono">8</td><td>八 bā</td><td>发 fā — “to prosper, get rich”</td><td>Wealth and success</td></tr>
<tr><td class="mono">00</td><td>零零</td><td>Wholeness again — symmetry</td><td>Balance</td></tr>
<tr><td class="mono">9</td><td>九 jiǔ</td><td>久 jiǔ — “long-lasting”</td><td>Longevity, eternity</td></tr>
</tbody></table></div>
<p>Put 8 and 9 side by side and you get <b>发久</b> — “prosper for a long time”. The paired zeros frame each blessing like the setting around a gem, which makes the number symmetrical and easy to remember: <span class="mono">008 · 009</span>.</p>
<h2 id="why">Why numbers matter so much in Chinese culture</h2>
<p>Mandarin has relatively few syllables, so many words sound alike. Numbers borrow meaning from the words they resemble. That’s why 8 is prized (it sounds like 发, wealth) and 4 is avoided (it sounds like 死, death). The Beijing 2008 Olympics famously opened on <b>8 August 2008 at 8:08 pm</b> local time to capture that luck.</p>
<h2 id="economy">The economic side</h2>
<p>These beliefs move real money. A Chengdu phone number, 8888-8888, sold for ¥2.33 million in 2003. Hong Kong’s single-number licence plates have sold for millions — “9” for HK$13 million in 1994 and “28” for HK$18.1 million in 2016. Numeric domain names are prized too: Chinese users remember digits more easily than romanised words, which is why some of China’s biggest web brands use numeric domains.</p>
<h2 id="people">What it means for people</h2>
<ul><li><b>Families</b> pick wedding dates, gift amounts and house numbers with 8s and 9s.</li><li><b>Businesses</b> choose phone numbers, prices (¥88, ¥168, ¥888) and opening dates to signal prosperity.</li><li><b>Collectors</b> treat rare numbers as assets that can be resold.</li></ul>
<blockquote>Try it: run any number through our <a href="../tools/number-analyzer.html?n=008009">Lucky Number Analyzer</a> — 008009 scores in the top tier.</blockquote>
<p class="muted">Note: “008009” is used on this site as a descriptive number. We are not affiliated with any brand that uses a similar number.</p>
""" + sources("cli", "olympics", "gwr", "kwik", "mo"),
[("What does 008009 mean in Chinese?", "Read by sound, 8 (八) evokes 发 (prosperity) and 9 (九) evokes 久 (long-lasting); the zeros suggest wholeness. Together: complete prosperity that lasts."),
 ("Is 008009 a lucky number?", "Yes. It contains no 4, pairs 8 with 9 (发久), ends on 9 and is symmetrical, so it scores in the top tier on most Chinese number-luck scales.")]),

("why-8-is-lucky", "Why is 8 the luckiest number in China?", "The sound, history and money behind the number 8 — from the 08/08/08 Olympics to multi-million-dollar phone numbers and plates.", "Culture", 7, """
<p>Ask anyone in China, Hong Kong, Taiwan or Singapore for the luckiest number and most will say <b>8</b>. The reason is sound: <b>八 (bā)</b> is close to <b>发 (fā)</b>, the verb in 发财 — “to make a fortune”. In Cantonese the match is even closer (baat / faat).</p>
<h2>8 in public life</h2>
<ul><li><b>Olympics:</b> Beijing’s 2008 Games opened on 08-08-08 at 8:08 pm.</li><li><b>Prices:</b> shops price goods at 88, 168 or 888 to signal prosperity.</li><li><b>Addresses:</b> homes and offices on the 8th, 18th, 28th or 88th floor are easier to sell.</li><li><b>Phone numbers & plates:</b> numbers packed with 8s sell at auction.</li></ul>
<h2>What an 8 is worth</h2>
<div class="table-wrap"><table><thead><tr><th>Item</th><th>Price</th><th>Year</th></tr></thead><tbody>
<tr><td>Phone number 8888-8888 (Chengdu)</td><td>¥2.33 million (~US$280,000)</td><td>2003</td></tr>
<tr><td>Hong Kong plate “28” (易发, easy prosperity)</td><td>HK$18.1 million</td><td>2016</td></tr>
<tr><td>Hong Kong plate “18” (实发, certain prosperity)</td><td>HK$16.5 million</td><td>2008</td></tr>
<tr><td>Hong Kong plate “8”</td><td>HK$5 million</td><td>1988</td></tr>
</tbody></table></div>
<p>Hong Kong’s “special registration mark” auctions send their proceeds to the government Lotteries Fund for welfare projects — so lucky numbers fund real causes too.</p>
<h2>Combinations that amplify 8</h2>
<p><a href="../numbers/168.html">168</a> (一路发, prosper all the way), <a href="../numbers/518.html">518</a> (我要发, I will prosper), <a href="../numbers/88.html">88</a>, <a href="../numbers/888.html">888</a> and <a href="../numbers/8899.html">8899</a> (prosperity that lasts).</p>
""" + sources("olympics", "gwr", "kwik", "w", "cli"),
[("Why is 8 lucky in Chinese?", "Because 八 (bā) sounds like 发 (fā), meaning to prosper or get rich."), ("What is the most expensive lucky number ever sold in China?", "The 8888-8888 phone number in Chengdu sold for ¥2.33 million in 2003 — a record at the time.")]),

("why-4-is-unlucky", "Why is 4 unlucky? Tetraphobia explained", "How the number 4 became the most avoided digit in East Asia — skipped floors, cheaper phone numbers and the exceptions where 4 is fine.", "Culture", 5, """
<p><b>四 (sì)</b> sounds almost identical to <b>死 (sǐ)</b>, “death”. That single homophone shapes architecture, pricing and gifting across China, Hong Kong, Taiwan, Japan and Korea.</p>
<h2>Where you’ll see it</h2>
<ul><li>Buildings that skip 4, 14, 24 and sometimes every floor ending in 4.</li><li>Hospitals and hotels avoiding room numbers with 4.</li><li>Phone numbers and plates with many 4s selling for less.</li><li>Gift sets never sold in fours.</li></ul>
<h2>Especially bad combinations</h2>
<p><a href="../numbers/14.html">14</a> (要死, “going to die”), <a href="../numbers/24.html">24</a> (Cantonese 易死), <a href="../numbers/44.html">44</a> and 74.</p>
<h2>When 4 is fine</h2>
<p>Context changes everything. In <a href="../numbers/1314.html">1314</a> (一生一世, “a lifetime”) and <a href="../numbers/9420.html">9420</a> (就是爱你, “it’s you I love”) the 4 is read as a different word. Our analyzer accounts for these exceptions.</p>
<blockquote>Stuck with a 4? Use the <a href="../tools/number-analyzer.html">analyzer</a> to see luckier variations — or ask about swapping on our <a href="../exchange/index.html">Exchange</a>.</blockquote>
""" + sources("cli"),
[("Why do Chinese buildings skip the 4th floor?", "Because 4 (四, sì) sounds like death (死, sǐ). Developers relabel floors to avoid putting off buyers."), ("Is 4 always unlucky?", "No — in romantic codes like 1314 and 9420 the 4 is read as a different word and is positive.")]),

("lucky-number-economy", "The lucky number economy: phones, plates and domains", "Real prices from the market for lucky numbers — record phone numbers, Hong Kong plate auctions and numeric domain names — and how to buy or sell one.", "Market", 8, """
<p>Lucky numbers aren’t just folklore — they’re a market. Wherever Chinese communities live, numbers with 8s, 9s and repeated digits sell at a premium, while numbers with 4s sell at a discount.</p>
<h2>1. Phone numbers</h2>
<p>The Chengdu number <b>8888-8888</b> sold for ¥2.33 million in 2003. Guinness World Records lists the most expensive phone number as <b>666-6666</b>, sold for about US$2.75 million at a 2006 charity auction in Qatar — where 6 is also lucky.</p>
<h2>2. Licence plates</h2>
<div class="table-wrap"><table><thead><tr><th>Hong Kong plate</th><th>Price</th><th>Year</th></tr></thead><tbody>
<tr><td>W</td><td>HK$26 million</td><td>2021</td></tr><tr><td>28</td><td>HK$18.1 million</td><td>2016</td></tr><tr><td>18</td><td>HK$16.5 million</td><td>2008</td></tr><tr><td>9</td><td>HK$13 million</td><td>1994</td></tr></tbody></table></div>
<p>Hong Kong’s Transport Department auctions special marks regularly, and proceeds go to the Lotteries Fund for welfare projects.</p>
<h2>3. Numeric domain names</h2>
<p>Because Chinese characters can’t easily be typed into web addresses, numbers have become a shared “language” for Chinese brands. Reported sales include 55.com (US$2.3 million, 2011), 114.com (US$2.1 million, 2013) and 88888.com (US$245,000). Short all-numeric .com domains exist in fixed supply — only 1,000 three-digit and 10,000 four-digit combinations.</p>
<h2>How to value a lucky number</h2>
<ol><li><b>Digit quality:</b> 8s and 9s up; 4s down.</li><li><b>Pattern:</b> AAAA, AABB, ABAB and mirror numbers are collectible.</li><li><b>Ending:</b> the last digit counts most.</li><li><b>Length & scarcity:</b> shorter is rarer.</li><li><b>Market:</b> plates depend on local rules; domains on extension (.com first).</li></ol>
<div class="notice"><b>Buying or selling?</b> Use our <a href="../exchange/index.html#lead">free valuation & matching service</a>.</div>
""" + sources("gwr", "kwik", "w", "td", "mo", "cnn"),
[("How much is a lucky phone number worth?", "Most sell for tens to thousands of dollars; exceptional ones set records — 8888-8888 sold for ¥2.33 million in Chengdu in 2003."), ("Why are numeric domains valuable in China?", "Numbers are easier for Chinese users to remember and type than romanised words, and short numeric .com domains exist in fixed supply.")]),

("red-envelope-amounts", "Lucky red envelope (hongbao) amounts guide", "How much to give in a red envelope for weddings, Chinese New Year, birthdays and business openings — lucky amounts and ones to avoid.", "Etiquette", 5, """
<p>Red envelopes (红包 hóngbāo) carry money wrapped in luck. The amount matters as much as the gesture.</p>
<h2>Golden rules</h2>
<ul><li>Avoid any amount with a <b>4</b>.</li><li>For weddings and New Year, give <b>even</b> amounts (good things come in pairs).</li><li>Use crisp, new bills and never coins.</li><li>8 for wealth, 9 for longevity, 6 for smoothness.</li></ul>
<h2>Popular amounts</h2>
<div class="table-wrap"><table><thead><tr><th>Occasion</th><th>Popular amounts</th><th>Why</th></tr></thead><tbody>
<tr><td>Wedding</td><td>188 · 288 · 520 · 666 · 888 · 1314</td><td>Prosperity, love (520), a lifetime (1314)</td></tr>
<tr><td>Chinese New Year</td><td>66 · 88 · 168 · 188</td><td>Smooth, prosperous year</td></tr>
<tr><td>Birthday (elders)</td><td>99 · 199 · 999</td><td>Longevity (久)</td></tr>
<tr><td>Business opening</td><td>168 · 518 · 888 · 1688</td><td>Prosper all the way</td></tr></tbody></table></div>
<p>Generate amounts in your own budget with the <a href="../tools/red-envelope.html">Red Envelope & Lucky Price tool</a>.</p>
""" + sources("cli"),
[("How much should I put in a wedding red envelope?", "Choose an even amount without a 4 that fits your relationship — 188, 288, 520, 888 and 1314 are popular."), ("What amounts should I avoid?", "Anything containing 4, odd amounts at weddings, and 250 (slang for ‘idiot’).")]),

("choose-lucky-phone-number", "How to choose a lucky phone number", "A practical checklist for picking an auspicious mobile or business phone number: digits, endings, patterns and mistakes to avoid.", "How-to", 6, """
<p>Your phone number is on business cards, invoices and signage for years. In Chinese markets a lucky number is a small but real brand asset.</p>
<h2>The 7-point checklist</h2>
<ol><li><b>Zero or minimal 4s</b> — especially at the end.</li><li><b>End on 8, 9 or 6.</b> The ending is what people remember.</li><li><b>Look for power combos</b>: 168, 518, 1688, 8899, 88, 99.</li><li><b>Repeated runs</b> (888, 9999) are premium and memorable.</li><li><b>Avoid 14, 24, 74 and 250.</b></li><li><b>Keep it readable</b> — ABAB and mirror numbers are easy to recall.</li><li><b>Check the full number</b>, not just the last four digits.</li></ol>
<h2>Test before you buy</h2>
<p>Paste candidates into the <a href="../tools/number-analyzer.html">Lucky Number Analyzer</a> or compare two side by side with the <a href="../tools/index.html#compare">Compare tool</a>.</p>
<h2>Where to find one</h2>
<p>Carriers sometimes sell “靓号” (premium numbers) directly. For rarer numbers, use a broker — or post a request on our <a href="../exchange/index.html#lead">Lucky Number Exchange</a> and we’ll alert you when a match appears.</p>
""",
[("What is a lucky phone number in Chinese culture?", "One with several 8s, 9s or 6s, no 4s, and a strong ending such as 8 or 9."), ("Can I change my number to a luckier one?", "Often yes — carriers and brokers sell premium numbers. Check local portability rules first.")]),

("chinese-zodiac-guide", "Chinese zodiac: the 12 animals explained", "How the Chinese zodiac works — the 12 animals, the five elements, lunar new year boundaries, compatibility and lucky numbers for each sign.", "Zodiac", 7, """
<p>The Chinese zodiac (生肖 shēngxiào) assigns each lunar year one of 12 animals in a fixed order: <b>Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig</b>. Combine the animals with the five elements (Wood, Fire, Earth, Metal, Water) and you get a 60-year cycle.</p>
<h2>Why January babies get it wrong</h2>
<p>The zodiac year starts at Chinese New Year, which falls between 21 January and 20 February. Someone born on 1 February 2027 is still a Horse, because the Year of the Goat begins on 6 February 2027. Our <a href="../tools/chinese-zodiac.html">Zodiac Finder</a> handles that automatically.</p>
<h2>Compatibility in brief</h2>
<ul><li><b>Trines (三合):</b> Rat–Dragon–Monkey · Ox–Snake–Rooster · Tiger–Horse–Dog · Rabbit–Goat–Pig.</li><li><b>Secret friends (六合):</b> Rat–Ox · Tiger–Pig · Rabbit–Dog · Dragon–Rooster · Snake–Monkey · Horse–Goat.</li><li><b>Clashes (六冲):</b> Rat–Horse · Ox–Goat · Tiger–Monkey · Rabbit–Rooster · Dragon–Dog · Snake–Pig.</li></ul>
<p>Explore each sign: <a href="../zodiac/index.html">all 12 animals</a>.</p>
""" + sources("ch"),
[("When does the Chinese zodiac year start?", "At Chinese New Year (the second new moon after the winter solstice), between 21 January and 20 February."), ("What is the 2027 Chinese zodiac?", "2027 is the Year of the Fire Goat, starting 6 February 2027.")]),

("feng-shui-numbers-home", "Feng shui numbers for your home and office", "Using numbers in feng shui: house and floor numbers, Kua numbers and favourable directions, and simple fixes for unlucky addresses.", "Feng shui", 6, """
<p>Feng shui (风水) is the traditional practice of arranging spaces for harmony. Numbers are one of its easiest levers.</p>
<h2>House and unit numbers</h2>
<ul><li>Addresses with 8, 9 or 6 are favoured; addresses with 4 are often discounted.</li><li>Add the digits for a “root” number: 2+8 → 10 → 1. Many practitioners read 8 and 9 roots as strongest.</li><li>An unlucky number can be “softened” with décor — practitioners suggest adding a small 8 or balancing element near the door.</li></ul>
<h2>Your Kua number</h2>
<p>Your Kua number comes from your birth year and sex and places you in the East or West group, each with four favourable directions for success, health, love and growth. Find yours with the <a href="../tools/kua-number.html">Kua calculator</a>.</p>
<h2>Office tips</h2>
<ol><li>Sit facing your success direction.</li><li>Keep the entrance clear — it’s where energy (qi) enters.</li><li>Pick a lucky suite or floor number when you can.</li></ol>
<p class="muted">Feng shui is a cultural tradition, not a science. Use it for inspiration and peace of mind.</p>
""",
[("What house numbers are lucky in feng shui?", "Numbers containing 8, 9 or 6 — and whose digits don’t add up to 4 — are generally favoured."), ("What is a Kua number?", "A personal feng shui number from 1–9 (never 5) based on your birth year and sex, used to find your favourable directions.")]),
]
