/* 008009.com numerology engine — cultural/entertainment scoring of numbers.
   Pure functions, no DOM. Exposed as window.LN */
(function (root) {
  'use strict';
  var DIGITS = {
    '0': { cn: '零', py: 'líng', w: 1, sound: '灵 (líng, spirit/clever) · 圆 (wholeness)', mean: 'Completeness, wholeness and a fresh start; amplifies the digits around it.' },
    '1': { cn: '一', py: 'yī', w: 1, sound: '要 (yào, want) in combos', mean: 'Unity, beginnings and leadership; “one path” (一路) in 168.' },
    '2': { cn: '二', py: 'èr', w: 3, sound: '双 / 易 (easy, Cantonese)', mean: 'Pairs and harmony — “good things come in pairs” (好事成双).' },
    '3': { cn: '三', py: 'sān', w: 2, sound: '生 (shēng/saang, life, Cantonese)', mean: 'Life and growth, especially in Cantonese usage.' },
    '4': { cn: '四', py: 'sì', w: -10, sound: '死 (sǐ, death)', mean: 'The most avoided digit: sounds like “death”. Many buildings skip 4th/14th floors.' },
    '5': { cn: '五', py: 'wǔ', w: -1, sound: '无 (wú, none) · 我 (wǒ, me) in slang', mean: 'Neutral-to-mixed: the Five Elements; also “me” (5) in 520 / 518.' },
    '6': { cn: '六', py: 'liù', w: 6, sound: '流 / 溜 (smooth, flowing)', mean: 'Smooth progress — 六六大顺 “everything goes smoothly”.' },
    '7': { cn: '七', py: 'qī', w: 0, sound: '起 (rise) · 气 (qi) · 妻 (wife)', mean: 'Mixed: togetherness (Qixi love festival) but also the 7th “ghost” month.' },
    '8': { cn: '八', py: 'bā', w: 10, sound: '发 (fā, prosper / get rich)', mean: 'The king of lucky digits: wealth, prosperity and success.' },
    '9': { cn: '九', py: 'jiǔ', w: 7, sound: '久 (jiǔ, long-lasting)', mean: 'Longevity and eternity; the emperor’s number, popular for weddings.' }
  };
  // Pattern rules: [regex-or-string, points, label]
  var COMBOS = [
    ['5201314', 12, '5201314 — “I love you for a lifetime”'],
    ['1314', 6, '1314 — “one lifetime” (一生一世)'],
    ['520', 6, '520 — “I love you” (我爱你)'],
    ['168', 8, '168 — “one road to prosperity” (一路发)'],
    ['1688', 6, '1688 — “prosper all the way”'],
    ['518', 8, '518 — “I will prosper” (我要发)'],
    ['888', 10, '888 — triple prosperity'],
    ['88', 6, '88 — double prosperity (发发); also “bye-bye”'],
    ['999', 8, '999 — eternal, long-lasting'],
    ['99', 5, '99 — “forever and ever” (久久)'],
    ['666', 7, '666 — everything smooth (六六大顺)'],
    ['66', 4, '66 — smooth sailing'],
    ['28', 5, '28 — “easy prosperity” (易发, Cantonese)'],
    ['89', 5, '89 — prosperity that lasts (发久)'],
    ['98', 4, '98 — lasting wealth'],
    ['68', 4, '68 — smooth prosperity (路发)'],
    ['86', 3, '86 — prosperity flowing'],
    ['1818', 5, '1818 — “will prosper, will prosper” (要发要发)'],
    ['008', 4, '008 — wholeness + prosperity'],
    ['009', 3, '009 — wholeness + longevity'],
    ['14', -8, '14 — sounds like “will die” (要死 / 实死)'],
    ['24', -5, '24 — “easy death” (易死, Cantonese)'],
    ['74', -6, '74 — “certainly die” (气死 / 去死)'],
    ['54', -5, '54 — “I die / no death” — ambiguous, often avoided'],
    ['44', -8, '44 — double death'],
    ['250', -5, '250 — slang for “idiot” (二百五)'],
    ['38', -1, '38 — mildly negative slang in Mandarin'],
    ['13', -1, '13 — Western bad-luck number (mild)']
  ];
  function clean(s) { return String(s || '').replace(/\D+/g, ''); }
  function countOf(s, d) { return s.split(d).length - 1; }
  function occurrences(s, pat) { var c = 0, i = 0; while ((i = s.indexOf(pat, i)) !== -1) { c++; i += 1; } return c; }

  function analyze(input) {
    var s = clean(input);
    var out = { number: s, score: 0, raw: 0, lines: [], digits: [], verdict: '', tier: '', counts: {} };
    if (!s) return out;
    var raw = 0, lines = [];
    for (var i = 0; i < s.length; i++) out.digits.push({ d: s[i], info: DIGITS[s[i]] });
    // digit weights (diminishing for long numbers)
    var norm = Math.max(1, Math.sqrt(s.length / 4));
    '0123456789'.split('').forEach(function (d) {
      var c = countOf(s, d); out.counts[d] = c;
      if (d === '4') c = Math.max(0, c - occurrences(s, '1314')); // 4 inside 1314 means "lifetime", not death
      if (!c) return;
      var pts = DIGITS[d].w * c / norm;
      if (Math.abs(pts) >= 0.5) lines.push([pts, c + '× ' + d + ' (' + DIGITS[d].cn + ' ' + DIGITS[d].py + ') — ' + DIGITS[d].sound]);
      raw += pts;
    });
    // combos (longest first, avoid double counting via masking)
    var masked = s;
    COMBOS.slice().sort(function (a, b) { return b[0].length - a[0].length; }).forEach(function (c) {
      var n = occurrences(masked, c[0]);
      if (n) {
        raw += c[1] * n; lines.push([c[1] * n, (n > 1 ? n + '× ' : '') + c[2]]);
        if (c[0].length >= 3) masked = masked.split(c[0]).join('x'.repeat(c[0].length));
      }
    });
    // ending digit matters most (last impression)
    var last = s[s.length - 1];
    if (last === '8' || last === '9' || last === '6') { raw += 5; lines.push([5, 'Ends in ' + last + ' — a strong finish']); }
    if (last === '4' && !/1314$/.test(s)) { raw -= 6; lines.push([-6, 'Ends in 4 — weak finish']); }
    // repetition / patterns
    if (/^(\d)\1+$/.test(s) && s.length >= 3) { raw += 8; lines.push([8, 'All-same digits (' + s.length + '× ' + s[0] + ') — premium “solid” pattern']); }
    else {
      var run = s.match(/(\d)\1{2,}/g);
      if (run) { var b = Math.min(8, run.length * 3 + run.join('').length - 3); raw += b; lines.push([b, 'Repeating run ' + run.join(', ') + ' — memorable, collectible']); }
    }
    if (s.length >= 4 && /^(\d\d)\1+$/.test(s)) { raw += 4; lines.push([4, 'ABAB pattern — rhythmic and memorable']); }
    if (s.length >= 4 && isAscending(s)) { raw += 5; lines.push([5, 'Ascending sequence — 步步高升 “rising step by step”']); }
    if (s.length >= 4 && isAscending(s.split('').reverse().join(''))) { raw -= 2; lines.push([-2, 'Descending sequence — “going downhill”']); }
    if (s.length >= 4 && s === s.split('').reverse().join('')) { raw += 3; lines.push([3, 'Palindrome — balanced (mirror number)']); }
    if (!countOf(s, '4')) { raw += 3; lines.push([3, 'Contains no 4 — nothing to avoid']); }
    out.raw = raw;
    out.score = Math.round(100 / (1 + Math.exp(-raw / 14)));
    out.score = Math.max(1, Math.min(99, out.score));
    lines.sort(function (a, b) { return Math.abs(b[0]) - Math.abs(a[0]); });
    out.lines = lines.map(function (l) { return { pts: Math.round(l[0] * 10) / 10, text: l[1] }; });
    var sc = out.score;
    out.tier = sc >= 88 ? 'imperial' : sc >= 75 ? 'excellent' : sc >= 60 ? 'good' : sc >= 45 ? 'neutral' : sc >= 30 ? 'weak' : 'avoid';
    out.verdict = {
      imperial: 'Imperial-grade lucky number 🏮', excellent: 'Excellent — highly auspicious', good: 'Good fortune number',
      neutral: 'Neutral — neither lucky nor unlucky', weak: 'Weak — some unlucky signals', avoid: 'Better to avoid'
    }[out.tier];
    return out;
  }
  function isAscending(s) { for (var i = 1; i < s.length; i++) if (+s[i] !== +s[i - 1] + 1) return false; return true; }

  // Suggest upgrades: replace 4s with 8/9, try last-digit swap
  function suggest(input, max) {
    var s = clean(input); if (!s) return [];
    var base = analyze(s).score, seen = {}, res = [];
    function push(c, why) { if (seen[c] || c === s) return; seen[c] = 1; var a = analyze(c); if (a.score > base) res.push({ n: c, score: a.score, why: why }); }
    push(s.replace(/4/g, '8'), 'Swap every 4 → 8');
    push(s.replace(/4/g, '9'), 'Swap every 4 → 9');
    push(s.slice(0, -1) + '8', 'End in 8');
    push(s.slice(0, -1) + '9', 'End in 9');
    if (s.length >= 3) push(s.slice(0, -3) + '168', 'End in 168 (一路发)');
    if (s.length >= 3) push(s.slice(0, -3) + '888', 'End in 888');
    if (s.length >= 3) push(s.slice(0, -3) + '518', 'End in 518 (我要发)');
    if (s.length >= 2) push(s.slice(0, -2) + '89', 'End in 89 (发久)');
    res.sort(function (a, b) { return b.score - a.score; });
    return res.slice(0, max || 5);
  }

  // Generate lucky numbers of a given length with options
  function generate(len, opts) {
    opts = opts || {}; len = Math.max(1, Math.min(16, len | 0));
    var pool = opts.pool || '0123567889966888';
    var best = [];
    for (var t = 0; t < 1500; t++) {
      var s = opts.prefix ? clean(opts.prefix) : '';
      while (s.length < len) s += pool[Math.floor(Math.random() * pool.length)];
      s = s.slice(0, len);
      if (opts.noFour !== false && s.indexOf('4') > -1) continue;
      best.push({ n: s, score: analyze(s).score });
    }
    var uniq = {}, out = [];
    best.sort(function (a, b) { return b.score - a.score; }).forEach(function (x) { if (!uniq[x.n] && out.length < (opts.count || 12)) { uniq[x.n] = 1; out.push(x); } });
    return out;
  }

  // Chinese calendar helpers (via Intl, with a verified override table for New Year dates)
  var ANIMALS = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig'];
  var ANIMALS_CN = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
  var STEMS_EL = ['Wood', 'Wood', 'Fire', 'Fire', 'Earth', 'Earth', 'Metal', 'Metal', 'Water', 'Water'];
  // Verified Chinese New Year dates (official PRC calendar) — override ICU edge cases
  var CNY = { 2020: '2020-01-25', 2021: '2021-02-12', 2022: '2022-02-01', 2023: '2023-01-22', 2024: '2024-02-10', 2025: '2025-01-29', 2026: '2026-02-17', 2027: '2027-02-06', 2028: '2028-01-26' };
  function lunar(date) {
    try {
      var f = new Intl.DateTimeFormat('en-u-ca-chinese', { year: 'numeric', month: 'numeric', day: 'numeric', timeZone: 'Asia/Shanghai' });
      var p = {}; f.formatToParts(date).forEach(function (x) { p[x.type] = x.value; });
      var y = +(p.relatedYear || p.year), m = p.month, d = +p.day;
      var leap = /bis|L/.test(m); m = parseInt(m, 10);
      // override around verified New Year edges
      var gy = date.getFullYear();
      [gy, gy + 1].forEach(function (yy) {
        if (!CNY[yy]) return; var ny = new Date(CNY[yy] + 'T00:00:00+08:00');
        var diff = Math.floor((date - ny) / 864e5);
        if (diff >= 0 && diff < 3 && y === yy - 1) { y = yy; m = 1; d = diff + 1; leap = false; }
      });
      return { year: y, month: m, day: d, leap: leap };
    } catch (e) { return null; }
  }
  function zodiacForDate(date) {
    var l = lunar(date); var y = l ? l.year : date.getFullYear();
    var idx = ((y - 4) % 12 + 12) % 12, stem = ((y - 4) % 10 + 10) % 10;
    return { year: y, animal: ANIMALS[idx], cn: ANIMALS_CN[idx], index: idx, element: STEMS_EL[stem], yin: stem % 2 === 1, lunar: l };
  }
  function nextCNY(from) {
    from = from || new Date(); var y = from.getFullYear();
    for (var yy = y; yy <= y + 1; yy++) { if (CNY[yy]) { var d = new Date(CNY[yy] + 'T00:00:00+08:00'); if (d > from) return { date: d, year: yy }; } }
    return null;
  }
  root.LN = { DIGITS: DIGITS, COMBOS: COMBOS, analyze: analyze, suggest: suggest, generate: generate, clean: clean, lunar: lunar, zodiacForDate: zodiacForDate, nextCNY: nextCNY, ANIMALS: ANIMALS, ANIMALS_CN: ANIMALS_CN };
})(typeof window !== 'undefined' ? window : globalThis);
