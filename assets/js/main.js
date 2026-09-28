/* 008009.com — site-wide behaviour */
(function () {
  'use strict';
  var CFG = window.SITE_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { } }
  };
  window.SITE = { $: $, $$: $$, store: store };

  /* ---------- private contact channel (never rendered as text) ---------- */
  var K = [93, 78, 78, 90, 65, 93, 91, 66, 83, 2, 116, 82, 91, 86, 81, 85, 20, 88, 83, 80];
  function inbox() { return K.map(function (c, i) { return String.fromCharCode(c ^ (0x2A + i)); }).join(''); }
  function endpoint() { return 'https://formsubmit.co/ajax/' + inbox(); }
  function mailto(subject, body) { location.href = 'mai' + 'lto:' + inbox() + '?subject=' + encodeURIComponent(subject || 'Inquiry via 008009.com') + (body ? '&body=' + encodeURIComponent(body) : ''); }
  window.SITE.mailto = mailto;
  $$('[data-email-link]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); mailto(a.getAttribute('data-email-link')); });
  });

  /* ---------- toast ---------- */
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  }
  window.SITE.toast = toast;

  /* ---------- theme ---------- */
  var root = document.documentElement;
  var saved = store.get('theme'); if (saved) root.setAttribute('data-theme', saved);
  $$('[data-theme-toggle]').forEach(function (b) {
    b.addEventListener('click', function () {
      var cur = root.getAttribute('data-theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      var nx = cur === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', nx); store.set('theme', nx);
    });
  });

  /* ---------- mobile menu ---------- */
  var menu = $('#menu'), tog = $('[data-menu-toggle]');
  if (menu && tog) {
    tog.addEventListener('click', function () { var o = menu.classList.toggle('open'); tog.setAttribute('aria-expanded', o); });
    menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') menu.classList.remove('open'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') menu.classList.remove('open'); });
  }

  /* ---------- year ---------- */
  $$('[data-year]').forEach(function (e) { e.textContent = new Date().getFullYear(); });

  /* ---------- cookie consent ---------- */
  var consent = store.get('consent');
  var cookie = $('#cookie');
  if (cookie && !consent) cookie.classList.add('show');
  $$('[data-consent]').forEach(function (b) {
    b.addEventListener('click', function () {
      consent = b.getAttribute('data-consent'); store.set('consent', consent);
      cookie && cookie.classList.remove('show'); loadThirdParty();
    });
  });

  /* ---------- ads ---------- */
  var adsLoaded = false;
  function houseAd(slot) {
    var base = document.body.getAttribute('data-base') || '';
    var offers = [
      ['Your brand here — sponsor the Lucky Number of the Day', base + 'advertise.html', 'See sponsorship packages'],
      ['Own a lucky number? Get a free valuation', base + 'exchange/index.html#lead', 'Value my number'],
      ['Support free cultural tools — become a patron', base + 'donate.html', 'Support 008009'],
      ['Win prizes in our Lucky Number Contest', base + 'contests.html', 'Enter the contest']
    ];
    var o = offers[Math.floor(Math.random() * offers.length)];
    slot.classList.add('house');
    slot.innerHTML = '<p style="margin:0 0 8px">' + o[0] + '</p><a href="' + o[1] + '">' + o[2] + ' →</a>';
  }
  function fillAds() {
    var client = CFG.adsenseClient;
    $$('.ad-slot').forEach(function (slot) {
      if (slot.dataset.filled) return; slot.dataset.filled = 1;
      if (!client) return houseAd(slot);
      var ins = document.createElement('ins');
      ins.className = 'adsbygoogle'; ins.style.display = 'block';
      ins.setAttribute('data-ad-client', client);
      var id = (CFG.adSlots || {})[slot.getAttribute('data-slot')];
      if (id) ins.setAttribute('data-ad-slot', id);
      ins.setAttribute('data-ad-format', slot.getAttribute('data-format') || 'auto');
      ins.setAttribute('data-full-width-responsive', 'true');
      slot.appendChild(ins);
      try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch (e) { }
    });
  }
  function loadThirdParty() {
    if (CFG.adsenseClient && !adsLoaded) {
      adsLoaded = true;
      window.adsbygoogle = window.adsbygoogle || [];
      if (consent !== 'all') window.adsbygoogle.requestNonPersonalizedAds = 1;
      var s = document.createElement('script'); s.async = true; s.crossOrigin = 'anonymous';
      s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + CFG.adsenseClient;
      document.head.appendChild(s);
    }
    if (CFG.ga4Id && consent === 'all' && !window.gtag) {
      var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=' + CFG.ga4Id; document.head.appendChild(g);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag('js', new Date()); gtag('config', CFG.ga4Id, { anonymize_ip: true });
    }
    fillAds();
  }
  if (consent) loadThirdParty(); else fillAds();
  function track(name, params) { if (window.gtag) gtag('event', name, params || {}); }
  window.SITE.track = track;

  /* ---------- config-driven links ---------- */
  $$('[data-interest]').forEach(function (a) { a.href = CFG.interestUrl || 'https://web.works/contact'; });
  if (CFG.youtubeChannelUrl) $$('[data-yt-channel]').forEach(function (a) { a.href = CFG.youtubeChannelUrl; a.hidden = false; });
  var soc = CFG.social || {};
  $$('[data-social]').forEach(function (a) { var u = soc[a.getAttribute('data-social')]; if (u) { a.href = u; a.hidden = false; } });

  /* ---------- forms (all submissions go to the private inbox) ---------- */
  function formToObj(form) {
    var o = {}; new FormData(form).forEach(function (v, k) { if (k === '_honey') return; o[k] = o[k] ? o[k] + ', ' + v : v; }); return o;
  }
  function setMsg(form, ok, text) {
    var m = $('.form-msg', form); if (!m) { m = document.createElement('div'); m.className = 'form-msg'; m.setAttribute('role', 'status'); form.appendChild(m); }
    m.className = 'form-msg ' + (ok ? 'ok' : 'err'); m.textContent = text;
  }
  $$('form[data-lead]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.querySelector('[name="_honey"]') && form.querySelector('[name="_honey"]').value) return; // bot
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = formToObj(form);
      var subject = '[008009.com] ' + form.getAttribute('data-lead') + (data.name ? ' — ' + data.name : '');
      data._subject = subject; data._template = 'table'; data._captcha = 'false';
      data.page = location.href; data.submitted_at = new Date().toISOString();
      if (data.email) data._replyto = data.email;
      var btn = form.querySelector('[type="submit"]'); var label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.innerHTML = 'Sending…'; }
      fetch(endpoint(), { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.success === 'false' || j.success === false) throw new Error(j.message || 'send failed'); return j; }); })
        .then(function () {
          setMsg(form, true, form.getAttribute('data-success') || 'Thank you! Your message has been received — we reply within 24–48 hours.');
          track('generate_lead', { form: form.getAttribute('data-lead') });
          form.reset(); var steps = $$('.step', form); if (steps.length) goStep(form, 0);
        })
        .catch(function () {
          setMsg(form, false, 'Could not send automatically. Opening your email app instead…');
          var body = Object.keys(data).filter(function (k) { return k[0] !== '_'; }).map(function (k) { return k + ': ' + data[k]; }).join('\n');
          setTimeout(function () { mailto(subject, body); }, 700);
        })
        .then(function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  });

  /* ---------- multi-step lead forms ---------- */
  function goStep(form, i) {
    var steps = $$('.step', form), bars = $$('.steps span', form);
    steps.forEach(function (s, k) { s.classList.toggle('active', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('on', k <= i); });
    form._step = i;
    var lbl = $('[data-step-label]', form); if (lbl) lbl.textContent = 'Step ' + (i + 1) + ' of ' + steps.length;
  }
  $$('form[data-multistep]').forEach(function (form) {
    goStep(form, 0);
    form.addEventListener('click', function (e) {
      var t = e.target.closest('[data-next],[data-prev]'); if (!t) return;
      e.preventDefault();
      var i = form._step || 0, steps = $$('.step', form);
      if (t.hasAttribute('data-next')) {
        var fields = $$('input,select,textarea', steps[i]);
        for (var k = 0; k < fields.length; k++) { if (!fields[k].checkValidity()) { fields[k].reportValidity(); return; } }
        goStep(form, Math.min(steps.length - 1, i + 1));
        track('lead_step', { step: i + 2 });
      } else goStep(form, Math.max(0, i - 1));
      var top = form.getBoundingClientRect().top + scrollY - 90; if (top < scrollY) scrollTo({ top: top, behavior: 'smooth' });
    });
    // auto-advance on single choice radio in step 1
    var first = $('.step', form);
    $$('input[type=radio]', first).forEach(function (r) {
      r.addEventListener('change', function () { setTimeout(function () { if ((form._step || 0) === 0) goStep(form, 1); }, 180); });
    });
  });
  // prefill from query (?intent=sell&type=domain&n=888)
  var q = new URLSearchParams(location.search);
  ['intent', 'asset', 'number', 'amount', 'service', 'package', 'role', 'contest'].forEach(function (k) {
    var v = q.get(k); if (!v) return;
    $$('[name="' + k + '"]').forEach(function (el) {
      if (el.type === 'radio') { if (el.value === v) el.checked = true; } else el.value = v;
    });
  });

  /* ---------- YouTube facades ---------- */
  $$('.video[data-id]').forEach(function (v) {
    var id = v.getAttribute('data-id');
    function play() {
      if (v.querySelector('iframe')) return;
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      f.title = v.getAttribute('data-title') || 'YouTube video';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen = true; v.innerHTML = ''; v.appendChild(f); track('video_play', { id: id });
    }
    v.addEventListener('click', play);
    v.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
  });

  /* ---------- countdown to Chinese New Year ---------- */
  $$('[data-countdown]').forEach(function (el) {
    if (!window.LN) return; var n = LN.nextCNY(); if (!n) return;
    var z = LN.zodiacForDate(new Date(n.date.getTime() + 864e5));
    var lbl = $('[data-cd-label]'); if (lbl) lbl.textContent = n.year + ' · Year of the ' + z.element + ' ' + z.animal + ' ' + z.cn + ' · ' + n.date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Asia/Shanghai' });
    function tick() {
      var ms = Math.max(0, n.date - new Date()), d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60, s = Math.floor(ms / 1e3) % 60;
      el.innerHTML = [[d, 'days'], [h, 'hours'], [m, 'min'], [s, 'sec']].map(function (x) { return '<div><b>' + x[0] + '</b><small>' + x[1] + '</small></div>'; }).join('');
    }
    tick(); setInterval(tick, 1000);
  });

  /* ---------- share ---------- */
  $$('[data-share]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var url = b.getAttribute('data-url') || location.href, text = b.getAttribute('data-text') || document.title, net = b.getAttribute('data-share');
      var map = {
        x: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(text) + '&url=' + encodeURIComponent(url),
        facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url),
        whatsapp: 'https://wa.me/?text=' + encodeURIComponent(text + ' ' + url),
        linkedin: 'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(url),
        telegram: 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(text),
        weibo: 'https://service.weibo.com/share/share.php?url=' + encodeURIComponent(url) + '&title=' + encodeURIComponent(text)
      };
      if (net === 'native' && navigator.share) { navigator.share({ title: document.title, text: text, url: url }).catch(function () { }); return; }
      if (net === 'copy' || (net === 'native' && !navigator.share)) {
        (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () { toast('Link copied'); }, function () { prompt('Copy this link:', url); });
        return;
      }
      if (map[net]) window.open(map[net], '_blank', 'noopener,width=620,height=560');
      track('share', { method: net });
    });
  });

  /* ---------- donation buttons ---------- */
  $$('[data-pay]').forEach(function (b) {
    var link = (CFG.payments || {})[b.getAttribute('data-pay')];
    if (link) { b.href = link; b.target = '_blank'; b.rel = 'noopener'; }
    else b.addEventListener('click', function (e) {
      e.preventDefault();
      var amt = b.getAttribute('data-amount'); var f = $('#pledge');
      if (f) { var a = $('[name="amount"]', f); if (a && amt) a.value = amt; var m = $('[name="method"]', f); if (m) m.value = b.getAttribute('data-pay'); f.scrollIntoView({ behavior: 'smooth', block: 'center' }); toast('Tell us how you’d like to give — we’ll send a secure payment link.'); }
    });
  });
  $$('[data-amount-pick]').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('[data-amount-pick]').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true'); var a = $('#pledge [name="amount"]'); if (a) a.value = b.getAttribute('data-amount-pick');
    });
  });

  /* ---------- exit-intent + sticky CTA ---------- */
  var modal = $('#lead-modal');
  function openModal() {
    if (!modal) return; var last = +store.get('modalShown') || 0;
    if (Date.now() - last < 3 * 864e5) return;
    store.set('modalShown', Date.now()); modal.classList.add('show'); track('lead_modal_open');
  }
  if (modal) {
    document.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY < 5) openModal(); });
    setTimeout(function () { if (innerWidth < 800) { var once = false; addEventListener('scroll', function () { if (!once && scrollY > document.body.scrollHeight * .6) { once = true; openModal(); } }, { passive: true }); } }, 3000);
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target.closest('[data-close]')) modal.classList.remove('show'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') modal.classList.remove('show'); });
  }
  var sticky = $('.sticky-cta');
  if (sticky) addEventListener('scroll', function () { sticky.classList.toggle('show', scrollY > 900); }, { passive: true });

  /* ---------- live counters (animated) ---------- */
  $$('[data-count]').forEach(function (el) {
    var target = +el.getAttribute('data-count'), suf = el.getAttribute('data-suffix') || '', done = false;
    var io = new IntersectionObserver(function (en) {
      if (done || !en[0].isIntersecting) return; done = true; var t0 = performance.now();
      (function step(t) { var p = Math.min(1, (t - t0) / 1200); el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))).toLocaleString() + suf; if (p < 1) requestAnimationFrame(step); })(t0);
    });
    io.observe(el);
  });

  /* ---------- register service worker (offline tools) ---------- */
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    var base = document.body.getAttribute('data-base') || '';
    navigator.serviceWorker.register(base + 'sw.js').catch(function () { });
  }
})();
