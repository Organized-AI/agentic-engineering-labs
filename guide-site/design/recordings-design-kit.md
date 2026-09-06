# Organized AI — Recordings Design Kit

Extracted from `https://recordings.organizedai.vip/` (single inline `<style>` block, no framework, no build step). Everything below is verbatim from the live page unless marked *derived*.

---

## 1. Design tokens

### Colors

| Token | Value | Role |
|---|---|---|
| `--bg` | `#0c0b09` | Page background (near-black, warm) |
| `--bg-2` | `#100f0c` | Slightly lifted bg (stat row) |
| `--surface` | `#1a1814` | Cards, video frame, modal |
| `--surface-2` | `#211e19` | Top of buy-panel gradient |
| `--line` | `#2a2520` | All borders / dividers |
| `--muted` | `#605848` | Labels, captions, footer, secondary nav |
| `--text-2` | `#a09888` | Body copy, subtitles |
| `--text-1` | `#cfc7b6` | Default body text (`body` color) |
| `--text-hi` | `#f0ece4` | Headings, emphasized text |
| `--accent` | `#f5d623` | Primary yellow — CTAs, stats, highlights |
| `--accent-dim` | `#c4943d` | Section labels, repo links, list arrows |
| `--accent-deep` | `#8b7a12` | Accent borders (pills, hover borders) |
| `--accent-tint` | `rgba(245,214,35,.06)` | Pill / tag backgrounds |

Fixed values used outside tokens:
- Nav bg: `rgba(12,11,9,.92)` + `backdrop-filter: blur(8px)`
- Modal scrim: `rgba(12,11,9,.8)` + `blur(4px)`
- Video card shadow: `0 30px 80px rgba(0,0,0,.5)`
- Video element bg: `#000`

### Typography

| Token | Value |
|---|---|
| `--mono` | `"JetBrains Mono", ui-monospace, monospace` |
| `--sans` | `"Inter", -apple-system, system-ui, sans-serif` |

Google Fonts load:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Rule of thumb: **Inter for headings and body; JetBrains Mono for everything "system-y"** — brand, nav, buttons, labels, stats, prices, dates, captions, footer. Mono text is almost always uppercase with wide tracking.

| Element | Family | Weight | Size | Tracking | Case |
|---|---|---|---|---|---|
| body | sans | 400 | 15.5px / lh 1.65 | — | — |
| h1 | sans | 700 | `clamp(34px,4.6vw,56px)` / lh 1.12 | -.5px | — |
| h2 | sans | 700 | `clamp(26px,3.4vw,40px)` / lh 1.18 | -.4px | — |
| card h3 | sans | 700 | 19.5px / lh 1.25 | — | — |
| brand | mono | 800 | 16px | .04em | upper |
| nav link | mono | 600 | 12.5px | .1em | upper |
| button | mono | 700 | 13px | .05em | upper |
| status pill | mono | 600 | 11.5px | .16em | upper |
| section label | mono | 600 | 12px | .1em | upper |
| event head | mono | 600 | 12px | .08em | upper |
| org tag | mono | 600 | 10px | .08em | upper |
| stat number | mono | 800 | 26px / lh 1.1 | — | — |
| stat label | mono | 600 | 10.5px | .14em | upper |
| price | mono | 800 | `clamp(46px,6vw,72px)` / lh 1 | — | — |
| caption / guarantee | mono | 400–600 | 11px | .1–.12em | upper |
| sponsors kicker | mono | 600 | 11px | .4em | upper |
| footer | mono | 400 | 11.5px | .04em | upper |

### Layout & shape

| Token | Value |
|---|---|
| `--maxw` | `1180px` |
| `--r` | `10px` (cards, stat row) |
| Wrap padding | `0 22px` |
| Section padding | `72px 0`, `border-top: 1px solid var(--line)` |
| Hero padding | `72px 0 64px` |
| Hero grid | `1.15fr .85fr`, gap `clamp(28px,4vw,56px)` |
| Card grid | `repeat(auto-fill, minmax(300px,1fr))`, gap 18px |
| Radii | 5px (org tag) · 6px (date) · 7px (buttons, pill) · 8px (video) · 10px (cards) · 14px (video card, modal, buy panel) |
| Breakpoint | `920px` — hero → 1 col, stats 4→2, nav links hidden |

### Motion

- Buttons: `transition: transform .12s, background .2s, border-color .2s`; primary hover `translateY(-1px)`
- Cards: `transition: transform .12s, border-color .2s`; hover `translateY(-3px)` + `border-color: var(--accent-deep)`
- Card images: `filter: saturate(.92)`, `object-position: top`
- `html { scroll-behavior: smooth }`

---

## 2. Signature patterns

- **Brand lockup:** `ORGANIZED <span class="y">AI</span> <span class="sec">// RECORDINGS</span>` — white / yellow / muted. The `//` slash-comment motif recurs in section labels ("The Talks //", "Get Access //") and the page title.
- **Accent pill:** yellow text + `--accent-deep` 1px border + `--accent-tint` fill. Used for status badge, dates, and speaker tags. Status pill gets a 7px yellow dot via `::before`.
- **Stat row:** bordered container, cells divided by `border-right`, big mono yellow number over tiny muted label.
- **Talk card:** 16:9 image on top, tag → h3 → description → mono repo path with `→` that turns yellow on hover.
- **Buy panel:** vertical gradient `surface-2 → surface`, 2-col (1.2fr / .8fr), dashed-border list with `→` bullets, oversized mono price.
- **Arrows:** `→` used as CTA suffix and list bullet everywhere. No icons.
- **Sponsor logos:** white PNGs at `height:32px; opacity:.85`.

---

## 3. Full stylesheet (verbatim)

```css
:root{
  --bg:#0c0b09; --bg-2:#100f0c; --surface:#1a1814; --surface-2:#211e19;
  --line:#2a2520; --muted:#605848; --text-2:#a09888; --text-1:#cfc7b6; --text-hi:#f0ece4;
  --accent:#f5d623; --accent-dim:#c4943d; --accent-deep:#8b7a12; --accent-tint:rgba(245,214,35,.06);
  --maxw:1180px; --r:10px;
  --mono:"JetBrains Mono",ui-monospace,monospace;
  --sans:"Inter",-apple-system,system-ui,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text-1);font-family:var(--sans);line-height:1.65;font-size:15.5px}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
a{color:inherit}

/* nav */
.topbar{border-bottom:1px solid var(--line);background:rgba(12,11,9,.92);backdrop-filter:blur(8px);position:sticky;top:0;z-index:50}
.topnav{display:flex;align-items:center;gap:26px;padding:16px 0}
.brand{font-family:var(--mono);font-weight:800;font-size:16px;letter-spacing:.04em;color:var(--text-hi);text-decoration:none;white-space:nowrap}
.brand .y{color:var(--accent)}
.brand .sec{color:var(--muted);font-weight:600}
.navlinks{display:flex;gap:22px;margin-left:auto;align-items:center}
.navlink{font-family:var(--mono);font-size:12.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text-2);text-decoration:none}
.navlink:hover{color:var(--text-hi)}
.btn{font-family:var(--mono);font-weight:700;font-size:13px;letter-spacing:.05em;text-transform:uppercase;
     padding:14px 22px;border-radius:7px;cursor:pointer;border:1px solid transparent;text-decoration:none;display:inline-block;
     transition:transform .12s, background .2s, border-color .2s}
.btn-primary{background:var(--accent);color:var(--bg)}
.btn-primary:hover{transform:translateY(-1px)}
.btn-ghost{border-color:var(--line);color:var(--text-1)}
.btn-ghost:hover{border-color:var(--accent-deep);color:var(--text-hi)}
.btn small{display:block;font-size:10px;font-weight:500;letter-spacing:.12em;margin-top:3px;opacity:.75}

/* hero */
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(28px,4vw,56px);align-items:center;padding:72px 0 64px}
.status{display:inline-flex;align-items:center;gap:9px;font-family:var(--mono);font-size:11.5px;font-weight:600;
        letter-spacing:.16em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent-deep);
        border-radius:7px;padding:8px 14px;background:var(--accent-tint);margin-bottom:26px}
.status::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--accent)}
h1{font-family:var(--sans);font-weight:700;font-size:clamp(34px,4.6vw,56px);line-height:1.12;color:var(--text-hi);letter-spacing:-.5px}
h1 .y{color:var(--accent)}
.sub{color:var(--text-2);margin:20px 0 30px;max-width:56ch}
.heroctas{display:flex;gap:14px;flex-wrap:wrap;align-items:center}

.statrow{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:var(--r);
         margin-top:38px;background:var(--bg-2);overflow:hidden}
.stat{padding:20px 18px;border-right:1px solid var(--line)}
.stat:last-child{border-right:none}
.stat b{display:block;font-family:var(--mono);font-weight:800;font-size:26px;color:var(--accent);line-height:1.1}
.stat span{font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}

.videocard{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.videocard video{display:block;width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:8px;background:#000}
.videocap{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);padding:12px 6px 4px;text-align:center}

/* sections */
section{padding:72px 0;border-top:1px solid var(--line)}
.evhead{display:flex;align-items:center;gap:12px;font-family:var(--mono);font-size:12px;font-weight:600;
        letter-spacing:.08em;text-transform:uppercase;color:var(--text-2);margin:0 0 18px}
.grid + .evhead{margin-top:34px;padding-top:22px;border-top:1px solid var(--line)}
.evdate{color:var(--accent);border:1px solid var(--accent-deep);background:var(--accent-tint);
        border-radius:6px;padding:5px 9px;font-size:11px;white-space:nowrap}
.seclabel{font-family:var(--mono);font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-dim);margin-bottom:18px}
h2{font-family:var(--sans);font-weight:700;font-size:clamp(26px,3.4vw,40px);line-height:1.18;color:var(--text-hi);letter-spacing:-.4px;max-width:24ch}
.lead{color:var(--text-2);margin:16px 0 40px;max-width:64ch}

/* talk cards */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;
      display:flex;flex-direction:column;transition:transform .12s, border-color .2s}
.card:hover{transform:translateY(-3px);border-color:var(--accent-deep)}
.card img{width:100%;aspect-ratio:16/9;object-fit:cover;object-position:top;border-bottom:1px solid var(--line);filter:saturate(.92)}
.card .pad{padding:18px 20px 20px;display:flex;flex-direction:column;flex:1}
.org-tag{align-self:flex-start;font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
         color:var(--accent);border:1px solid var(--accent-deep);border-radius:5px;padding:4px 8px;background:var(--accent-tint)}
.card h3{font-family:var(--sans);font-weight:700;font-size:19.5px;color:var(--text-hi);margin:12px 0 8px;line-height:1.25}
.card p{color:var(--text-2);font-size:13.5px;flex:1}
.card .gh{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:var(--accent-dim);margin-top:16px}
.card:hover .gh{color:var(--accent)}
.card .gh:hover{text-decoration:underline}

/* sign-in modal */
.modal{position:fixed;inset:0;background:rgba(12,11,9,.8);backdrop-filter:blur(4px);display:none;place-items:center;z-index:100}
.modal.open{display:grid}
.mbox{width:min(400px,92vw);background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:34px;position:relative}
.mbox h3{color:var(--text-hi);font-size:20px;margin-bottom:8px}
.mbox p{color:var(--text-2);font-size:13.5px;margin-bottom:22px;line-height:1.5}
.mbox .btn{display:block;width:100%;text-align:center;margin-top:10px}
.mclose{position:absolute;top:12px;right:16px;font-family:var(--mono);color:var(--muted);cursor:pointer;background:none;border:none;font-size:16px;padding:4px}
.mclose:hover{color:var(--text-hi)}

/* buy */
.buypanel{background:linear-gradient(180deg,var(--surface-2),var(--surface));border:1px solid var(--line);border-radius:14px;
          padding:clamp(30px,5vw,54px);display:grid;grid-template-columns:1.2fr .8fr;gap:36px;align-items:center}
.price{font-family:var(--mono);font-weight:800;font-size:clamp(46px,6vw,72px);color:var(--accent);line-height:1}
.price small{font-size:16px;color:var(--muted);font-weight:600;letter-spacing:.1em}
.buylist{list-style:none;margin:18px 0 0}
.buylist li{font-size:14px;color:var(--text-1);padding:7px 0;border-bottom:1px dashed var(--line)}
.buylist li::before{content:"→ ";font-family:var(--mono);color:var(--accent-dim)}
.buyside{text-align:center}
.buyside .btn{width:100%;padding:18px 22px;font-size:14px}
.guarantee{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:14px}

/* sponsors + footer */
.sponsors{display:flex;flex-direction:column;align-items:center;gap:20px;padding:56px 0 20px;border-top:1px solid var(--line)}
.sponsors .k{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.4em;text-transform:uppercase;color:var(--muted)}
.sponsors .row{display:flex;align-items:center;gap:52px;flex-wrap:wrap;justify-content:center}
.sponsors img{height:32px;width:auto;opacity:.85}
footer{font-family:var(--mono);color:var(--muted);font-size:11.5px;text-align:center;padding:28px 0 44px;letter-spacing:.04em}
footer a{color:var(--text-2);text-decoration:none}
footer a:hover{color:var(--accent)}

@media(max-width:920px){
  .hero{grid-template-columns:1fr}
  .videocard{max-width:420px;margin:0 auto}
  .statrow{grid-template-columns:repeat(2,1fr)}
  .stat:nth-child(2){border-right:none}
  .buypanel{grid-template-columns:1fr}
  .navlink{display:none}
}
```

---

## 4. Component markup (verbatim from the page)

```html
<!-- Brand -->
<a class="brand" href="#">ORGANIZED <span class="y">AI</span> <span class="sec">// RECORDINGS</span></a>

<!-- Status pill -->
<div class="status">Workshops + How To Series · Austin</div>

<!-- Event header -->
<div class="evhead"><span class="evdate">10 Jul 2026</span>Vol 2 · The Agentic Engineering Stack Workshops</div>

<!-- Talk card -->
<a class="card" href="/vault?talk=01" data-talk="01" data-gh="https://github.com/Organized-AI/agentic-eng-workshops/tree/main/workshops/02-giving-agents-data">
  <img src="assets/michael.jpg" alt="Michael" loading="lazy">
  <div class="pad">
    <span class="org-tag">Michael</span>
    <h3>Real-Time Web Data for Agents</h3>
    <p>Live Apify actor workflows — scraping LinkedIn, feeding agents fresh web data, and shipping skills that call actors.</p>
    <div class="gh">workshops/02-giving-agents-data →</div>
  </div>
</a>

<!-- Price -->
<div class="price">$40 <small>ONE-TIME</small></div>

<!-- Buttons -->
<a class="btn btn-primary" href="#buy">Get the Recordings →<small>secure Stripe checkout</small></a>
<a class="btn btn-ghost" href="#talks">Browse the talks</a>
```

Page skeleton (*derived*): `header.topbar > .wrap.topnav` → `main.wrap > .hero` (copy + `.statrow` | `.videocard`) → `section#talks` (`.seclabel`, `h2`, `.lead`, `.evhead`, `.grid`) → `section#buy` (`.buypanel`) → `.sponsors` → `footer` → `.modal`.

---

## 5. Tokens in other formats

### Tailwind (`tailwind.config.js`)
```js
theme: {
  extend: {
    colors: {
      bg: '#0c0b09', 'bg-2': '#100f0c', surface: '#1a1814', 'surface-2': '#211e19',
      line: '#2a2520', muted: '#605848', 'text-2': '#a09888', 'text-1': '#cfc7b6', 'text-hi': '#f0ece4',
      accent: { DEFAULT: '#f5d623', dim: '#c4943d', deep: '#8b7a12', tint: 'rgba(245,214,35,.06)' },
    },
    fontFamily: { mono: ['"JetBrains Mono"','ui-monospace','monospace'], sans: ['Inter','-apple-system','system-ui','sans-serif'] },
    maxWidth: { wrap: '1180px' },
    borderRadius: { card: '10px', panel: '14px', btn: '7px' },
  }
}
```

### JSON (design-token style)
```json
{
  "color": {
    "bg": "#0c0b09", "bg2": "#100f0c", "surface": "#1a1814", "surface2": "#211e19",
    "line": "#2a2520", "muted": "#605848", "text2": "#a09888", "text1": "#cfc7b6", "textHi": "#f0ece4",
    "accent": "#f5d623", "accentDim": "#c4943d", "accentDeep": "#8b7a12", "accentTint": "rgba(245,214,35,0.06)"
  },
  "font": { "mono": "JetBrains Mono", "sans": "Inter" },
  "size": { "maxWidth": 1180, "radius": 10, "radiusPanel": 14, "radiusBtn": 7, "gutter": 22, "breakpoint": 920 }
}
```

---

## 6. Stack notes

- Single static HTML file, inline CSS, Google Fonts — no framework.
- GTM served via Stape custom domain: `arxmgigt.usv.stape.io`, container `GTM-T3SL8JPK`.
- Checkout: Stripe. Member area: `/vault`. Promo video: `/promo/recap_ig.mp4` (9:16).
- Sponsor assets: `/assets/twelvelabs_logo_white.png`, `/assets/webai_logo_white.png`.
