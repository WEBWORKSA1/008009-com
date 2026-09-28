/* 008009.com — interactive tools (depends on numerology.js + main.js) */
(function () {
  'use strict';
  var $ = SITE.$, $$ = SITE.$$, LN = window.LN;
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var BASE = document.body.getAttribute('data-base') || '';
  var ORIGIN = document.body.getAttribute('data-origin') || location.origin + '/';

  /* ================= Lucky Number Analyzer ================= */
  function renderAnalysis(box, a, kind) {
    var color = a.score >= 75 ? 'var(--gold)' : a.score >= 45 ? 'var(--jade)' : 'var(--red)';
    var digits = a.digits.slice(0, 24).map(function (x) { return '<div class="digit d' + x.d + '" title="' + esc(x.info.mean) + '">' + x.d + '<small>' + x.info.cn + '</small></div>'; }).join('');
    var lines = a.lines.slice(0, 10).map(function (l) { return '<li><span>' + esc(l.text) + '</span><span class="' + (l.pts >= 0 ? 'pos' : 'neg') + '">' + (l.pts > 0 ? '+' : '') + l.pts + '</span></li>'; }).join('');
    var sug = LN.suggest(a.number, 4).map(function (s) { return '<li><span><b class="mono">' + s.n + '</b> — ' + esc(s.why) + '</span><span class="pos">' + s.score + '/100</span></li>'; }).join('');
    var share = ORIGIN + 'tools/number-analyzer.html?n=' + a.number;
    box.innerHTML =
      '<div class="card">' +
      '<div class="score-wrap"><div class="dial" style="--v:' + a.score + ';--dial-c:' + color + '"><span>' + a.score + '<small>/ 100</small></span></div>' +
      '<div><span class="tag ' + (a.score >= 60 ? 'gold' : a.score >= 45 ? 'jade' : '') + '">' + esc(kind || 'number') + ' luck score</span>' +
      '<p class="verdict">' + esc(a.verdict) + '</p><p class="mono muted" style="margin:0;font-size:1.2rem;letter-spacing:.08em">' + esc(a.number) + '</p></div></div>' +
      '<div class="digits">' + digits + '</div>' +
      '<h3>Why this score</h3><ul class="breakdown">' + lines + '</ul>' +
      (sug ? '<h3 style="margin-top:20px">Luckier variations</h3><ul class="breakdown">' + sug + '</ul>' : '') +
      '<div class="share-row"><button class="btn btn-gold btn-sm" data-card>⬇ Download share card</button>' +
      '<button class="btn btn-ghost btn-sm" data-sh="whatsapp">WhatsApp</button><button class="btn btn-ghost btn-sm" data-sh="x">X</button><button class="btn btn-ghost btn-sm" data-sh="facebook">Facebook</button><button class="btn btn-ghost btn-sm" data-sh="copy">Copy link</button></div>' +
      '<div class="notice" style="margin-top:18px"><b>Want a number like this — or selling one?</b> Our Lucky Number Exchange matches buyers and sellers of premium phone numbers, plates and numeric domains. <a href="' + BASE + 'exchange/index.html?number=' + a.number + '#lead">Get a free valuation or alert →</a></div>' +
      '</div>';
    box.classList.add('show');
    $('[data-card]', box).addEventListener('click', function () { shareCard(a); });
    $$('[data-sh]', box).forEach(function (b) {
      b.setAttribute('data-share', b.getAttribute('data-sh')); b.setAttribute('data-url', share);
      b.setAttribute('data-text', 'My number ' + a.number + ' scored ' + a.score + '/100 on the 008009 Lucky Number Analyzer 🏮');
      b.addEventListener('click', function (e) {
        e.preventDefault(); var net = b.getAttribute('data-sh'), text = b.getAttribute('data-text');
        if (net === 'copy') { (navigator.clipboard ? navigator.clipboard.writeText(share) : Promise.reject()).then(function () { SITE.toast('Link copied'); }, function () { prompt('Copy link', share); }); return; }
        var u = { whatsapp: 'https://wa.me/?text=' + encodeURIComponent(text + ' ' + share), x: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(share), facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(share) }[net];
        window.open(u, '_blank', 'noopener,width=620,height=560');
      });
    });
    SITE.track('analyze_number', { length: a.number.length, score: a.score });
  }

  function shareCard(a) {
    var c = document.createElement('canvas'); c.width = 1080; c.height = 1080; var x = c.getContext('2d');
    var g = x.createLinearGradient(0, 0, 1080, 1080); g.addColorStop(0, '#8E0E15'); g.addColorStop(1, '#B3131B');
    x.fillStyle = g; x.fillRect(0, 0, 1080, 1080);
    x.strokeStyle = '#C9A227'; x.lineWidth = 10; x.strokeRect(40, 40, 1000, 1000);
    x.fillStyle = '#C9A227'; x.textAlign = 'center';
    x.font = '600 44px Georgia,serif'; x.fillText('LUCKY NUMBER SCORE', 540, 170);
    x.fillStyle = '#fff'; var fs = Math.min(150, Math.floor(1800 / Math.max(6, a.number.length)));
    x.font = '800 ' + fs + 'px ui-monospace,Menlo,monospace'; x.fillText(a.number, 540, 380);
    x.beginPath(); x.arc(540, 610, 150, 0, Math.PI * 2); x.fillStyle = 'rgba(255,255,255,.1)'; x.fill();
    x.beginPath(); x.lineWidth = 22; x.strokeStyle = '#C9A227'; x.arc(540, 610, 150, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * a.score / 100); x.stroke();
    x.fillStyle = '#fff'; x.font = '800 120px ui-monospace,Menlo,monospace'; x.fillText(a.score, 540, 650);
    x.font = '600 48px Georgia,serif'; x.fillText(a.verdict.replace(/[^\x20-⿿]/g, '').trim(), 540, 850);
    x.fillStyle = '#C9A227'; x.font = '700 42px ui-monospace,Menlo,monospace'; x.fillText('008009.com', 540, 960);
    c.toBlob(function (b) {
      var file = new File([b], 'lucky-' + a.number + '.png', { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [file] })) { navigator.share({ files: [file], title: 'My lucky number' }).catch(function () { dl(); }); } else dl();
      function dl() { var u = URL.createObjectURL(b), l = document.createElement('a'); l.href = u; l.download = file.name; document.body.appendChild(l); l.click(); l.remove(); setTimeout(function () { URL.revokeObjectURL(u); }, 2000); }
    });
    SITE.track('share_card', {});
  }

  $$('[data-analyzer]').forEach(function (form) {
    var input = $('input[name="n"]', form), out = $(form.getAttribute('data-analyzer')), kind = 'Number';
    $$('.chip', form).forEach(function (ch) {
      ch.addEventListener('click', function () {
        $$('.chip', form).forEach(function (c) { c.setAttribute('aria-pressed', 'false'); }); ch.setAttribute('aria-pressed', 'true');
        kind = ch.getAttribute('data-kind'); input.placeholder = ch.getAttribute('data-ph') || input.placeholder; input.focus();
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault(); var n = LN.clean(input.value);
      if (!n) { SITE.toast('Enter a number with at least one digit'); input.focus(); return; }
      if (n.length > 40) n = n.slice(0, 40);
      renderAnalysis(out, LN.analyze(n), kind);
      if (form.hasAttribute('data-update-url')) history.replaceState(null, '', '?n=' + n);
      out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
    var pre = new URLSearchParams(location.search).get('n') || form.getAttribute('data-prefill');
    if (pre) { input.value = pre; if (form.hasAttribute('data-update-url') || form.hasAttribute('data-prefill')) renderAnalysis(out, LN.analyze(pre), kind); }
  });

  /* ================= Compare two numbers ================= */
  var cmp = $('#compare-form');
  if (cmp) cmp.addEventListener('submit', function (e) {
    e.preventDefault(); var a = LN.analyze(cmp.a.value), b = LN.analyze(cmp.b.value), o = $('#compare-out');
    if (!a.number || !b.number) { SITE.toast('Enter two numbers'); return; }
    var win = a.score === b.score ? 'It’s a tie' : (a.score > b.score ? a.number : b.number) + ' is luckier';
    o.innerHTML = '<div class="grid g2">' + [a, b].map(function (x) { return '<div class="card center"><div class="dial" style="--v:' + x.score + ';margin:0 auto"><span>' + x.score + '</span></div><p class="mono" style="font-size:1.3rem;margin:.6em 0 0">' + x.number + '</p><p class="muted">' + x.verdict + '</p></div>'; }).join('') + '</div><p class="verdict center" style="margin-top:16px">🏆 ' + esc(win) + '</p>';
    o.classList.add('show');
  });

  /* ================= Generator ================= */
  var gen = $('#gen-form');
  if (gen) gen.addEventListener('submit', function (e) {
    e.preventDefault();
    var list = LN.generate(+gen.len.value, { prefix: gen.prefix.value, noFour: gen.nofour.checked, count: 12 });
    $('#gen-out').innerHTML = '<div class="num-grid">' + list.map(function (x) { return '<button type="button" class="num-tile great" data-copy="' + x.n + '"><b>' + x.n + '</b><small>' + x.score + '/100 · tap to copy</small></button>'; }).join('') + '</div>';
    $('#gen-out').classList.add('show');
    $$('[data-copy]', $('#gen-out')).forEach(function (b) { b.addEventListener('click', function () { var v = b.getAttribute('data-copy'); (navigator.clipboard ? navigator.clipboard.writeText(v) : Promise.reject()).then(function () { SITE.toast('Copied ' + v); }, function () { }); }); });
  });

  /* ================= Red envelope / lucky price ================= */
  var env = $('#envelope-form');
  if (env) env.addEventListener('submit', function (e) {
    e.preventDefault();
    var lo = Math.max(1, +env.min.value || 1), hi = Math.min(1e6, Math.max(lo, +env.max.value || lo)), occ = env.occasion.value, cands = [];
    var step = hi - lo > 200000 ? 10 : 1;
    for (var v = lo; v <= hi; v += step) {
      var s = String(v); if (s.indexOf('4') > -1) continue;
      if ((occ === 'wedding' || occ === 'newyear') && v % 2) continue; // even amounts for celebrations
      if (occ === 'price') { if (!/[89]$/.test(s)) continue; }
      var a = LN.analyze(s); if (a.score >= 70) cands.push({ v: v, s: a.score, round: /0+$/.test(s) ? 0 : 1 });
    }
    cands.sort(function (a, b) { return b.s - a.s || a.v - b.v; });
    var pick = cands.slice(0, 16).sort(function (a, b) { return a.v - b.v; });
    $('#envelope-out').innerHTML = pick.length ? '<div class="num-grid">' + pick.map(function (x) { return '<div class="num-tile great"><b>' + x.v.toLocaleString() + '</b><small>' + x.s + '/100</small></div>'; }).join('') + '</div><p class="muted" style="margin-top:12px">Tip: ' + ({ wedding: 'wedding gifts are traditionally even amounts; avoid 4. Red envelopes, crisp new bills.', newyear: 'give crisp new bills in even amounts; 8s and 6s are favourites.', birthday: 'amounts with 9 wish long life (久).', business: 'opening-day gifts love 8 (发) and 168 (一路发).', price: 'retail prices ending in 8 or 9 read as prosperous in Chinese markets.' }[occ] || '') + '</p>' : '<p>No strong lucky amounts in that range — try widening it.</p>';
    $('#envelope-out').classList.add('show');
  });

  /* ================= Zodiac ================= */
  var ZD = window.ZODIAC_DATA || null;
  var zf = $('#zodiac-form');
  if (zf) zf.addEventListener('submit', function (e) {
    e.preventDefault(); if (!zf.dob.value) { SITE.toast('Pick your birth date'); return; }
    var d = new Date(zf.dob.value + 'T12:00:00+08:00'), z = LN.zodiacForDate(d), info = ZD ? ZD[z.index] : null;
    var l = z.lunar;
    $('#zodiac-out').innerHTML = '<div class="card"><div class="score-wrap"><div class="dial" style="--v:100"><span style="font-family:var(--serif);font-size:3rem;color:var(--red)">' + z.cn + '</span></div><div>' +
      '<span class="tag gold">Your Chinese zodiac</span><p class="verdict">' + z.element + ' ' + z.animal + ' (' + (z.yin ? 'Yin' : 'Yang') + ')</p>' +
      (l ? '<p class="muted" style="margin:0">Lunar birthday: month ' + l.month + (l.leap ? ' (leap)' : '') + ', day ' + l.day + ', lunar year ' + l.year + '</p>' : '') + '</div></div>' +
      (info ? '<div class="grid g2" style="margin-top:18px"><div><h3>Personality</h3><p>' + info.traits + '</p></div><div><h3>Luck guide</h3><ul class="breakdown"><li><span>Lucky numbers</span><b>' + info.nums + '</b></li><li><span>Lucky colours</span><b>' + info.colors + '</b></li><li><span>Best matches</span><b>' + info.best + '</b></li><li><span>Clashes with</span><b>' + info.clash + '</b></li></ul></div></div>' +
        '<p style="margin-top:12px"><a class="btn btn-ghost btn-sm" href="' + BASE + 'zodiac/' + z.animal.toLowerCase() + '.html">Full ' + z.animal + ' profile →</a></p>' : '') +
      '<p class="form-note">Born in January or early February? Your animal follows the lunar new year, not January 1 — this tool accounts for that.</p></div>';
    $('#zodiac-out').classList.add('show');
    SITE.track('zodiac_lookup', { animal: z.animal });
  });

  var compat = $('#compat-form');
  if (compat) compat.addEventListener('submit', function (e) {
    e.preventDefault(); var a = +compat.a.value, b = +compat.b.value, A = LN.ANIMALS;
    var trine = function (x) { return x % 4; }, harmony = [[0, 1], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]];
    var isH = harmony.some(function (p) { return (p[0] === a && p[1] === b) || (p[0] === b && p[1] === a); });
    var clash = Math.abs(a - b) === 6, same = a === b, tr = trine(a) === trine(b) && !same;
    var score = clash ? 28 : isH ? 95 : tr ? 90 : same ? 70 : 60;
    var why = clash ? 'Opposite signs (六冲 clash) — strong attraction but frequent friction; needs patience.' : isH ? 'Secret friends (六合 six harmonies) — naturally supportive, one of the best pairings.' : tr ? 'Same trine (三合) — shared values and rhythm; an easy, lucky alliance.' : same ? 'Same sign — you understand each other; watch for mirrored weaknesses.' : 'Neutral pairing — compatibility depends on effort and the rest of the chart.';
    $('#compat-out').innerHTML = '<div class="card center"><div class="dial" style="--v:' + score + ';margin:0 auto"><span>' + score + '</span></div><p class="verdict" style="margin-top:12px">' + A[a] + ' ' + LN.ANIMALS_CN[a] + ' + ' + A[b] + ' ' + LN.ANIMALS_CN[b] + '</p><p>' + why + '</p></div>';
    $('#compat-out').classList.add('show');
  });

  /* ================= Lucky date checker ================= */
  var df = $('#date-form');
  if (df) df.addEventListener('submit', function (e) {
    e.preventDefault(); if (!df.date.value) { SITE.toast('Pick a date'); return; }
    var p = df.date.value.split('-'), d = new Date(df.date.value + 'T12:00:00+08:00'), l = LN.lunar(d), z = LN.zodiacForDate(d);
    var md = p[1] + p[2], full = p[0] + p[1] + p[2];
    var a = LN.analyze(full), b = LN.analyze(String(+p[1]) + String(+p[2]));
    var score = Math.round(a.score * .45 + b.score * .55), notes = [];
    if (l && l.month === 7) { score -= 18; notes.push(['neg', 'Falls in the 7th lunar month (Ghost Month) — traditionally avoided for weddings, moves and openings.']); }
    if (l && l.month === 1 && l.day <= 15) { score += 6; notes.push(['pos', 'Within the Spring Festival (first 15 days of the lunar year) — festive and auspicious.']); }
    if (md === '0808') { score += 10; notes.push(['pos', '8 August (8/8) — double prosperity; Beijing opened the 2008 Olympics on 08-08-08 at 8:08 pm.']); }
    if (md === '0909' || (l && l.month === 9 && l.day === 9 && !l.leap)) { score += 6; notes.push(['pos', 'Double Nine — longevity symbolism (重阳 on the lunar 9/9).']); }
    if (md === '0520' || md === '0521') { score += 8; notes.push(['pos', '5/20 · 5/21 — “I love you” (520/521): hugely popular wedding-registration dates.']); }
    if (/4/.test(String(+p[2]))) { score -= 6; notes.push(['neg', 'Day-of-month contains a 4.']); }
    if (/8/.test(String(+p[2]))) notes.push(['pos', 'Day-of-month contains an 8 (发).']);
    score = Math.max(1, Math.min(99, score));
    var wd = d.toLocaleDateString(undefined, { weekday: 'long', timeZone: 'Asia/Shanghai' });
    $('#date-out').innerHTML = '<div class="card"><div class="score-wrap"><div class="dial" style="--v:' + score + '"><span>' + score + '<small>/ 100</small></span></div><div><span class="tag gold">Date luck score</span><p class="verdict">' + d.toLocaleDateString(undefined, { dateStyle: 'long', timeZone: 'Asia/Shanghai' }) + '</p><p class="muted" style="margin:0">' + wd + (l ? ' · Lunar ' + l.month + '/' + l.day + (l.leap ? ' (leap month)' : '') : '') + ' · ' + z.element + ' ' + z.animal + ' year</p></div></div>' +
      '<ul class="breakdown" style="margin-top:14px">' + notes.map(function (n) { return '<li><span>' + n[1] + '</span><span class="' + n[0] + '">' + (n[0] === 'pos' ? '▲' : '▼') + '</span></li>'; }).join('') + '<li><span>Digits of the full date (' + full + ')</span><span>' + a.score + '</span></li><li><span>Month + day digits</span><span>' + b.score + '</span></li></ul>' +
      '<p class="form-note">For weddings and business openings, many families also consult a professional almanac (通书) reading. <a href="' + BASE + 'consult.html?service=date">Request a date consultation →</a></p></div>';
    $('#date-out').classList.add('show');
  });

  /* ================= Kua number ================= */
  var kf = $('#kua-form');
  var DIRS = { 1: ['SE', 'E', 'S', 'N'], 2: ['NE', 'W', 'NW', 'SW'], 3: ['S', 'N', 'SE', 'E'], 4: ['N', 'S', 'E', 'SE'], 6: ['W', 'NE', 'SW', 'NW'], 7: ['NW', 'SW', 'NE', 'W'], 8: ['SW', 'NW', 'W', 'NE'], 9: ['E', 'SE', 'N', 'S'] };
  if (kf) kf.addEventListener('submit', function (e) {
    e.preventDefault(); if (!kf.dob.value) { SITE.toast('Pick your birth date'); return; }
    var p = kf.dob.value.split('-').map(Number), y = p[0];
    if (p[1] < 2 || (p[1] === 2 && p[2] < 4)) y -= 1; // solar year starts ~Feb 4 (Li Chun)
    var r = function (n) { while (n > 9) n = String(n).split('').reduce(function (s, c) { return s + +c; }, 0); return n; };
    var s = r(y % 100 === 0 && y >= 2000 ? 0 : (y % 100)), kua;
    if (kf.sex.value === 'm') kua = y < 2000 ? 10 - s : 9 - s; else kua = y < 2000 ? r(s + 5) : r(s + 6);
    if (kua === 0) kua = 9; if (kua > 9) kua = r(kua);
    if (kua === 5) kua = kf.sex.value === 'm' ? 2 : 8;
    var d = DIRS[kua], east = [1, 3, 4, 9].indexOf(kua) > -1;
    $('#kua-out').innerHTML = '<div class="card"><div class="score-wrap"><div class="dial" style="--v:100"><span>' + kua + '<small>Kua</small></span></div><div><span class="tag gold">' + (east ? 'East' : 'West') + ' group</span><p class="verdict">Your Kua number is ' + kua + '</p></div></div>' +
      '<ul class="breakdown" style="margin-top:14px"><li><span>💰 Success & wealth (Sheng Chi 生气)</span><b>' + d[0] + '</b></li><li><span>🌿 Health (Tien Yi 天医)</span><b>' + d[1] + '</b></li><li><span>❤️ Love & relationships (Nien Yen 延年)</span><b>' + d[2] + '</b></li><li><span>🧘 Personal growth (Fu Wei 伏位)</span><b>' + d[3] + '</b></li></ul>' +
      '<p class="form-note">Face your success direction at your desk and sleep with your head toward a favourable direction. Your ' + (east ? 'East' : 'West') + '-group favourable directions are ' + (east ? 'N, S, E, SE' : 'W, NW, SW, NE') + '.</p></div>';
    $('#kua-out').classList.add('show');
  });

  /* ================= Lucky number of the day ================= */
  $$('[data-lnotd]').forEach(function (el) {
    var t = new Date(), seed = t.getFullYear() * 1e4 + (t.getMonth() + 1) * 100 + t.getDate();
    var rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
    var pool = ['8', '9', '6', '2', '3', '1', '0', '5', '7'], n = '';
    while (n.length < 3) n += pool[Math.floor(rnd() * (n.length ? 9 : 4))];
    var a = LN.analyze(n); el.innerHTML = '<b class="mono" style="font-size:2.4rem;color:var(--red)">' + n + '</b> <span class="muted">· ' + a.score + '/100 · ' + esc(a.lines[0] ? a.lines[0].text : '') + '</span>';
  });
})();
