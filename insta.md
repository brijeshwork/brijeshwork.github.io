# Instagram Assistant — Promotion Plan for homepage

Extension: Instagram Assistant | Auto Liker Post Reels & Comments
Chrome Web Store: https://chromewebstore.google.com/detail/instagram-assistant-auto/bidiegdfcdagpnkagbelgpbfnamhonfm

Overview
--------
Instagram Assistant is a Chrome extension that automates engagement actions (auto-like posts & reels, auto-like comments, auto-follow profiles) with built-in safety (rate limiting, human-like delays, skip patterns). It includes a dashboard, activity logging, and configurable settings.

Goal
----
Add a prominent, conversion-optimized promotion block to the site home page (`index.php`) that:
- Increases direct installs via the Chrome Web Store link
- Educates visitors on features & safety
- Tracks clicks, impressions and installs (via attribution)
- Respects privacy & disclosure requirements

High-level placement options
---------------------------
1. Hero strip (top of the page, directly under the header)
   - Short headline, 2-line description, big CTA button "Add to Chrome" with store badge and rating.
2. Feature card on homepage (below hero)
   - 3–4 feature bullets with small illustrations, secondary CTA to "Learn more" (leads to a dedicated extension landing page)
3. Persistent promo (floating/inline) for logged-in users only
   - Small sticky bar or sidebar that can be dismissed; ideal for returning visitors.

Design & UX copy
----------------
- Headline (hero): "Boost your Instagram engagement — safely and automatically"
- Subhead: "Auto-like posts & reels, engage comments, and follow targeted profiles — with smart rate limits and human-like behavior."
- Primary CTA: "Add to Chrome — Free"
- Secondary CTA: "See Demo & Safety" (anchor to a section explaining safety)
- Microcopy near CTA: "Works on instagram.com · Local-only data · 5★ from users"

Legal & Privacy
---------------
- Display a short privacy note: "Stores activity locally; optional sync is disclosed in extension settings."
- Link to privacy policy (use the Chrome Web Store privacy URL or site privacy page).
- Add a sentence explaining permissions required: "Requires access to instagram.com pages to perform actions — all data stored locally unless you enable sync."

Implementation details (index.php snippets)
------------------------------------------
Use a small, self-contained promo partial. Example markup (Bootstrap 5-friendly):

```html
<!-- Extension Promo Block -->
<section class="extension-promo bg-light py-4">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-md-7">
        <h2 class="promo-title">Boost your Instagram engagement — safely and automatically</h2>
        <p class="lead">Auto-like posts & reels, engage comments and follow relevant profiles with smart rate limiting and natural behavior.</p>
        <div class="d-flex gap-2 align-items-center">
          <a id="insta-promote-cta" href="https://chromewebstore.google.com/detail/instagram-assistant-auto/bidiegdfcdagpnkagbelgpbfnamhonfm" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg">Add to Chrome — Free</a>
          <a href="#insta-details" class="btn btn-outline-secondary">See Demo & Safety</a>
        </div>
        <p class="small mt-2 text-muted">Works on instagram.com · <strong>Local storage only</strong> by default · <span class="badge bg-success">5.0 ★</span></p>
      </div>
      <div class="col-md-5 text-center">
        <img src="/pub/media/img/insta-promo-screenshot.png" alt="Instagram Assistant sidebar screenshot" class="img-fluid shadow-sm" style="max-width:320px;">
      </div>
    </div>
  </div>
</section>
```

Minimal CSS (add to your stylesheet or inline):

```css
.extension-promo { background: linear-gradient(180deg,#fff 0%, #fbfbff 100%); }
.promo-title { font-size: 1.6rem; font-weight:700; }
```

Structured Data (JSON-LD)
-------------------------
Add SoftwareApplication schema in the page head (replace values if needed):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Instagram Assistant",
  "url": "https://chromewebstore.google.com/detail/instagram-assistant-auto/bidiegdfcdagpnkagbelgpbfnamhonfm",
  "image": "https://lh3.googleusercontent.com/xHmlNNFKfPABM5VJZeKaCFVXDBwE_2pmxByE8FzRXdhKwW4zWPxp9IoAP9x7XNEWO7rot8blnOjyCs2_k9Kz2zolTqk=s60",
  "description": "Auto-like posts & reels, engage comments, and follow profiles with smart rate limiting and human-like behavior.",
  "applicationCategory": "Social",
  "operatingSystem": "Chrome",
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "ratingCount": "3" }
}
</script>
```

Analytics & Tracking
--------------------
Goal: track impressions, CTA clicks, and referral installs (as much as Chrome Web Store allows).

1. Impression (fire once when block is visible):

```js
// gtag example
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);} 
// On block visible (e.g. when DOM ready):
gtag('event','extension_promo_impression', { 'event_category':'extension', 'event_label':'instagram_assistant' });
```

2. CTA click event (track outbound click):

```js
document.getElementById('insta-promote-cta').addEventListener('click', function(){
  gtag('event','extension_cta_click',{ 'event_category':'extension','event_label':'instagram_assistant','transport_type':'beacon' });
});
```

3. Attribution & installs
- You cannot directly detect Chrome Web Store installs from the website. Use referral links with UTM and the Web Store's developer analytics:

Example CTA href with UTM:

```
https://chromewebstore.google.com/detail/instagram-assistant-auto/bidiegdfcdagpnkagbelgpbfnamhonfm?utm_source=brijesh.work&utm_medium=promo_home&utm_campaign=insta_extension
```

Then in your Chrome Web Store developer dashboard, filter installs by the referral/UTM where possible, or capture clicks with your own analytics and treat a click as a proxy conversion.

Promotional Assets
------------------
- Use a clean screenshot of the sidebar UI (`insta-promo-screenshot.png`), 16:9 or 4:3
- Use the store icon (small) and a 5★ badge
- Short demo GIF (autoplay muted) helps conversion
- Include a short 20–30s explainer video on a dedicated landing page

A/B testing suggestions
-----------------------
- Test headline variations (emphasize safety vs. speed vs. growth)
- CTA copy: "Add to Chrome — Free" vs "Try it now" vs "Install"
- Use variant with screenshot vs GIF
- Sticky bar vs inline hero block

Accessibility
-------------
- Ensure CTA is keyboard-focusable and has aria-label: `aria-label="Add Instagram Assistant to Chrome (opens in new tab)"`
- Provide alt text for images and captions for GIFs/videos
- Ensure color contrast for button and text

Microcopy & FAQ (insta-details anchor content)
-----------------------------------------------
- Q: Is this safe for my account? A: The extension uses intelligent rate limiting and human-like delays. Use conservative defaults.
- Q: Where is my data stored? A: By default, all data is stored locally in your browser. Optional server sync is clearly disclosed in settings.
- Q: What permissions are required? A: Access to instagram.com pages to detect and perform actions and storage to keep logs and settings.

Rollout checklist
-----------------
- [ ] Add `insta-promo-screenshot.png` to `/pub/media/img/`
- [ ] Add promo partial to `index.php` (copy snippet above)
- [ ] Add JSON-LD to `<head>`
- [ ] Add analytics events and UTM to CTA
- [ ] Prepare privacy microcopy and link to extension privacy page
- [ ] QA: cross-browser visual check, keyboard navigation, mobile responsiveness
- [ ] Launch A/B test for headline/CTA for 2 weeks
- [ ] Review click-to-install ratio and adjust creative

Implementation notes & pitfalls
-------------------------------
- Do not try to auto-open installation windows — only link to the Chrome Web Store.
- Declare permissions and privacy clearly; do not obscure the data handling behavior.
- The Chrome Web Store may limit how installs are attributed; rely on click metrics and store dashboard.

Suggested commit message
------------------------
`feat(promo): add insta.md with homepage promotion plan & implementation snippets for Instagram Assistant extension`

---
File created by automation: `insta.md` — contains the promotion plan and copy snippets for adding the extension promo to `index.php`. Feel free to edit the copy, images and UTM values before deploying.