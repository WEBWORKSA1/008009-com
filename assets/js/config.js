/* ============================================================
   008009.com — SITE CONFIG (edit this file to monetize)
   Everything revenue-related is switched on here. No rebuild needed.
   ============================================================ */
window.SITE_CONFIG = {
  siteName: '008009.com',
  // External interest / acquisition link shown on top of every page
  interestUrl: 'https://web.works/contact',

  // --- Google AdSense ---------------------------------------------------
  // 1) Apply at https://adsense.google.com with this site.
  // 2) Paste your publisher id below, e.g. 'ca-pub-1234567890123456'
  // 3) Update /ads.txt with the same id. Until set, tasteful house ads show.
  adsenseClient: '',
  adSlots: { top: '', inArticle: '', sidebar: '', footer: '' }, // optional manual slot ids (else Auto ads)

  // --- Analytics (optional) ---------------------------------------------
  ga4Id: '', // e.g. 'G-XXXXXXXXXX'

  // --- YouTube channel (optional) ----------------------------------------
  youtubeChannelUrl: '', // e.g. 'https://www.youtube.com/@008009'

  // --- Donations / payments (paste hosted payment links; leave '' to use the pledge form) ---
  payments: {
    stripe: '',        // Stripe Payment Link  https://buy.stripe.com/...
    paypal: '',        // PayPal.me or hosted button link (do NOT use an email-based link)
    kofi: '',          // https://ko-fi.com/yourname
    buymeacoffee: '',  // https://buymeacoffee.com/yourname
    githubSponsors: '' // https://github.com/sponsors/yourname
  },

  // --- Social ----------------------------------------------------------
  social: { x: '', facebook: '', instagram: '', youtube: '', tiktok: '', linkedin: '', wechat: '' }
};
