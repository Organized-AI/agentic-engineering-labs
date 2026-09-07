import {base} from './catalog.mjs';

const esc = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export function homeMarkup(chapters) {
  const cards=chapters.map(c=>`<a class="chapter-card" href="${c.href}" data-chapter="${c.slug}"><div class="card-meta"><span>${c.number} / ${esc(c.group.split(' · ')[1])}</span><span>${c.minutes} min read</span></div><h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p><div class="card-bottom"><span>${esc(c.level)}</span><span class="card-arrow" aria-hidden="true">↗</span></div></a>`).join('');
  return `
  <section id="home" class="hero" data-surface="dark" aria-labelledby="hero-title">
    <canvas id="signal-canvas" aria-hidden="true"></canvas><div class="hero-shade" aria-hidden="true"></div>
    <div class="hero-meta"><span>Agentic engineering / Field guide / 2026</span><span class="edition-pill">Twenty-three chapters. One system.</span></div>
    <div class="hero-content"><div class="hero-title-block"><p class="hero-overline">Understand what makes them work.</p><h1 id="hero-title">Build agents.<br><span>Engineer systems.</span></h1></div><div class="hero-aside"><p>From reliable jobs to bounded agents, private compute, and business meaning. The engineering underneath useful AI.</p><a class="button primary" href="#curriculum"><span class="pill-icon" aria-hidden="true">↓</span>Explore the guide</a></div></div>
    <div class="hero-bottom"><p>Organized AI<span>Field notes / September 2026</span></p><span class="art-label">A field of connected systems</span><a class="scroll-link" href="#approach">Scroll to discover <span aria-hidden="true">↓</span></a></div>
  </section>

  <section id="approach" class="approach-section editorial-section" data-surface="light" aria-labelledby="approach-title">
    <div class="section-kicker"><span>01 / The approach</span><span>Beyond the prompt</span></div>
    <div class="editorial-intro"><h2 id="approach-title">The model is only<br><span class="muted-word">the beginning.</span></h2><div><p>Useful AI is a system, not a single response. Its data, permissions, tools, infrastructure, and economics all have to work together.</p><p class="secondary-copy">Learn one layer at a time. Then put them to work in one practical build.</p></div></div>
    <div class="approach-detail"><div><p class="eyebrow">The working principle</p><p class="principle">Define a useful outcome.<br>Make the work recoverable.<br>Keep decisions reviewable.<br>Measure what actually works.</p><a class="text-link" href="${chapters[0].href}">Start with experimentation <span aria-hidden="true">↗</span></a></div><div class="system-map"><h3>A system you can explain</h3><ol><li><span>01</span><strong>Define</strong><p>Outcome & domain</p></li><li><span>02</span><strong>Orchestrate</strong><p>Jobs, tools & policy</p></li><li><span>03</span><strong>Execute</strong><p>Models & compute</p></li><li><span>04</span><strong>Verify</strong><p>Facts & permissions</p></li><li><span>05</span><strong>Measure</strong><p>Quality, time & cost</p></li></ol></div></div>
    <div class="stat-row" aria-label="What the guide includes"><div class="stat"><b>31</b><span>Deep dives</span></div><div class="stat"><b>31</b><span>Test projects</span></div><div class="stat"><b>91</b><span>Runnable tests</span></div><div class="stat"><b>124</b><span>Progress milestones</span></div></div>
  </section>

  <section id="curriculum" class="curriculum editorial-section" data-surface="dark" aria-labelledby="curriculum-title">
    <div class="section-kicker"><span>02 / The curriculum</span><span>Foundations to frontier</span></div>
    <div class="section-heading"><h2 id="curriculum-title">Every layer.<br><span class="muted-word">One connected story.</span></h2><p>Read in order or follow your questions. Each chapter includes the mechanics, design choices, a worked example, a lab, and failure drills.</p></div>
    <div class="chapter-grid">${cards}</div>
  </section>

  <section id="practice" class="practice-section editorial-section" data-surface="light" aria-labelledby="practice-title">
    <div class="section-kicker"><span>03 / Into practice</span><span>Build something you can trust</span></div>
    <div class="practice-grid"><div><h2 id="practice-title">One project.<br><span class="muted-word">Every layer.</span></h2><p class="practice-lede">Build an event-operations assistant that uses approved facts, survives retries, and knows when to ask a question.</p><a class="button primary" href="${base}/capstone/"><span class="pill-icon" aria-hidden="true">↗</span>Build the capstone</a><a class="text-link" href="https://github.com/Organized-AI/agentic-engineering-labs" target="_blank" rel="noopener noreferrer">Open the 31-project repository <span aria-hidden="true">↗</span></a><p class="small-note">Offline Python starters and solutions. No API keys required.</p></div><div class="practice-spec"><p class="eyebrow">What you will put to the test</p><div><span>01</span><p><strong>Trustworthy inputs</strong>Canonical records, source versions, and explicit access scope.</p></div><div><span>02</span><p><strong>Recoverable execution</strong>Idempotency, worker leases, and atomic results.</p></div><div><span>03</span><p><strong>Bounded decisions</strong>Tool contracts, review gates, and safe stopping conditions.</p></div><div><span>04</span><p><strong>Measurable outcomes</strong>Evaluations, latency, retention, and total task cost.</p></div><a class="text-link" href="${base}/progress/">Track all 124 milestones <span aria-hidden="true">↗</span></a></div></div>
  </section>

  <section id="paths" class="learning-paths editorial-section" data-surface="dark" aria-labelledby="paths-title">
    <div class="section-kicker"><span>04 / Your starting point</span><span>Follow the layer you need</span></div><h2 id="paths-title">Different questions.<br><span class="muted-word">The same foundations.</span></h2>
    <div class="path-grid"><article><span class="path-label">01 / Build & ship</span><h3>The application path</h3><p>Foundations, jobs, gateways, agents, evaluations, and outcome economics.</p><a href="${chapters[1].href}">Start with the service ↗</a></article><article><span class="path-label">02 / Operate & optimize</span><h3>The infrastructure path</h3><p>Inference, load testing, data retention, kernels, and useful capacity.</p><a href="${chapters[6].href}">Understand the runtime ↗</a></article><article><span class="path-label">03 / Know & verify</span><h3>The knowledge path</h3><p>Agent contracts, evaluations, ontologies, provenance, and business meaning.</p><a href="${chapters[10].href}">Model the business ↗</a></article></div>
  </section>

  <section id="about" class="editorial-note editorial-section" data-surface="light" aria-labelledby="about-title"><div class="section-kicker"><span>05 / About this guide</span><span>Evidence before confidence</span></div><div class="editorial-intro"><h2 id="about-title">Inspired by a post.<br><span class="muted-word">Built into a curriculum.</span></h2><div><p>Shep Bryan’s post supplied the topics. The architecture, labs, comparisons, and recommendations are original instructional extensions—not a reconstruction of his infrastructure or an endorsement by him.</p><p class="secondary-copy">“Ontology-aligned compute” is a thesis to investigate, not a proven standard. Advanced GPU work is optional.</p><a class="text-link" href="${base}/sources/">Sources & editorial notes ↗</a><a class="text-link download-link" href="${base}/downloads/agentic-engineering.md" download>Download the Markdown guide ↓</a></div></div></section>`;
}
