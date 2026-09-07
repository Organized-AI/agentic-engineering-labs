const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function renderShell({title,description,body,active='',toc='',base,origin,updated,navHTML,assetVersion,url=base+'/',className=''}) {
  const isHome=className==='home';
  const onPage=toc?`<aside class="page-toc" aria-label="On this page"><p>ON THIS PAGE</p><nav>${toc}</nav><a class="back-top" href="#main">Back to top ↑</a></aside>`:'';
  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="${esc(description)}"><meta name="theme-color" content="${isHome?'#10100b':'#fffcf4'}">
<title>${esc(title)} · Organized AI</title><link rel="canonical" href="${origin}${url}">
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(description)}"><meta property="og:type" content="article"><meta property="og:url" content="${origin}${url}">
<link rel="icon" href="${base}/assets/favicon.svg?v=${assetVersion}" type="image/svg+xml">
<link rel="preload" href="${base}/assets/fonts/inter-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="${base}/assets/fonts/jetbrains-mono-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="${base}/assets/style.css?v=${assetVersion}"><link rel="stylesheet" href="${base}/assets/editorial.css?v=${assetVersion}">
<script src="${base}/assets/app.js?v=${assetVersion}" defer></script><script src="${base}/assets/player.js?v=${assetVersion}" defer></script><script src="${base}/assets/editorial.js?v=${assetVersion}" defer></script>
</head><body class="${className}" data-current="${esc(active)}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="${base}/">ORGANIZED <span class="brand-yellow">AI</span></a>
  <nav class="header-nav" aria-label="Primary navigation"><a href="${base}/#curriculum">Curriculum</a><a href="${base}/progress/">Progress</a><a href="${base}/#practice">The practice</a><a href="${base}/sources/">Sources</a></nav>
  <div class="topbar-actions"><button class="search-trigger" type="button" aria-haspopup="dialog"><span>Search</span><kbd>/</kbd></button><button class="menu-trigger" aria-label="Open chapter menu" aria-expanded="false" aria-controls="chapter-menu" aria-haspopup="dialog" type="button">Menu</button></div>
</header>
<aside class="sidebar" id="sidebar">
  <a class="sidebar-title" href="${base}/">AGENTIC ENGINEERING<span>A field guide to useful systems</span></a>
  <div class="progress-box"><div><span>YOUR PROGRESS</span><span data-progress-label>0 / 124</span></div><progress max="124" value="0" aria-label="Hands-on milestones complete"></progress><p><a href="${base}/progress/">Open progress dashboard →</a></p></div>
  <nav aria-label="Guide chapters">${navHTML}<p class="nav-group">07 · Put it into practice</p><a class="extra-link" href="${base}/progress/" ${active==='progress'?'aria-current="page"':''}>Hands-on progress</a><a class="extra-link" href="${base}/capstone/" ${active==='capstone'?'aria-current="page"':''}>Capstone & starter lab ↗</a><a class="extra-link" href="${base}/glossary/">Glossary</a><a class="extra-link" href="${base}/deep-research/" ${active==='deep-research'?'aria-current="page"':''}>Deep research</a><a class="extra-link" href="${base}/sources/">Sources & editorial notes</a><a class="extra-link" href="${base}/book/">Full reading edition</a><a class="extra-link" href="${base}/audio/" ${active==='audio'?'aria-current="page"':''}>Audio edition</a></nav>
  <div class="sidebar-footer">EDITION 01 <span>SEP 2026</span></div>
</aside>
<div class="page-layout"><main id="main" tabindex="-1">${body}</main>${onPage}</div>
<footer class="site-footer"><span>Organized AI / Agentic Engineering</span><span>Reviewed ${updated} · <a href="${base}/sources/">Evidence & scope</a></span>${isHome?'<button type="button" data-motion-toggle aria-pressed="false">Pause motion</button>':''}</footer>
<dialog class="chapter-menu" id="chapter-menu" aria-label="Chapter menu">
  <header class="menu-header"><a class="brand" href="${base}/">ORGANIZED <span class="brand-yellow">AI</span></a><button class="menu-close" type="button" aria-label="Close chapter menu" autofocus>Close <span aria-hidden="true">×</span></button></header>
  <div class="menu-layout"><div class="menu-overview"><p class="eyebrow">Agentic Engineering / Field guide</p><nav aria-label="Guide resources"><a href="${base}/">Overview</a><a href="${base}/progress/">Your progress</a><a href="${base}/capstone/">The capstone</a><a href="${base}/glossary/">Glossary</a><a href="${base}/sources/">The sources</a><a href="${base}/book/">Reading edition</a></nav><p class="menu-reading-progress">Project milestones <span data-progress-label>0 / 124</span></p></div><nav class="menu-chapters" aria-label="All chapters">${navHTML}</nav></div>
  <footer class="menu-footer"><span>Twenty-three chapters. One connected system.</span><span>Progress is saved in this browser.</span></footer>
</dialog>
<dialog class="search-dialog" aria-labelledby="search-title"><div class="search-heading"><h2 id="search-title">Search the field guide</h2><button type="button" data-close-search aria-label="Close search">Esc ×</button></div><label class="sr-only" for="guide-search">Search chapters, concepts, and labs</label><input id="guide-search" type="search" placeholder="Try “idempotency”, “KV cache”, or “ontology”…" autocomplete="off"><p id="search-status" aria-live="polite">Search across all 12 chapters.</p><div id="search-results"></div></dialog>
<div class="toast" role="status" aria-live="polite" hidden></div>
</body></html>`;
}
