# Agentic Engineering — Organized AI Field Guide

Source for `https://guide.organizedai.vip/agentic-eng/`.

Twelve substantial Markdown chapters, worked examples, failure drills, ship
gates, a capstone, glossary, primary-source references, a companion repository
with 12 test projects and 37 tests, and a printable/Markdown reading edition.

## Local workflow

```sh
npm ci
npm run build
npm run check
npm run dev
# http://127.0.0.1:4186/agentic-eng/
```

Chapter source is in `content/`; navigation and bibliography are in
`src/catalog.mjs`. `scripts/build.mjs` renders escaped Markdown as static HTML.
The content works without JavaScript. JavaScript adds search, copy buttons,
mobile navigation, and locally stored project milestones. The progress page
tracks four milestones per chapter and supports JSON export/import. There is no
analytics, account, form, remote model call, or data collection in the website.

`labs/` contains the explicitly limited offline SQLite simulation and tests.
Its files are copied unchanged to the public downloads during the build.
`research/source-audit.json` is a local link-check record, not published content.

The broader hands-on curriculum is maintained in the public companion repo:
`https://github.com/Organized-AI/agentic-engineering-labs`. `src/projects.mjs`
defines the one-to-one mapping, runnable commands, code excerpts, test counts,
and links used by every chapter and the progress dashboard.

## Design system

The active design follows the user's local editorial reference at port 4180:
a dark procedural hero, ivory reading surfaces, oversized regular-weight type,
thin rules, rounded actions, and a full-screen chapter menu. `DESIGN.md` records
the adaptations. The earlier Recordings Design Kit is retained in
`design/recordings-design-kit.md` for historical reference.

Inter and JetBrains Mono are served locally with their upstream licenses.
Canvas motion respects reduced-motion preferences and pauses off-screen or
when the tab is hidden. There is also a manual pause control. No runtime
animation dependency, checkout, tracking, or reference-site content was added.
Static HTML stays readable without JavaScript. Versioned CSS/JS URLs avoid
mixing old and new styles across releases.

## Publishing boundary

```sh
npm run deploy
```

This deploys the dedicated `organized-ai-agentic-eng` Worker. Its route is
`guide.organizedai.vip/agentic-eng*`, because Cloudflare route matching includes
query strings. The Worker strictly handles `/agentic-eng` and `/agentic-eng/…`;
other similarly prefixed paths pass through an explicit `GUIDE_ROUTER` service
binding to the existing router. The shared `organizedai-vanity-router` is not
edited or redeployed. A global same-zone fetch is deliberately not used for
that fallback, because the existing guide origin is itself a routed Worker.

The Worker serves static assets through an explicit binding after removing
the prefix. It applies content security and other response headers, redirects
to canonical trailing-slash pages, and preserves a real 404 for unknown pages.

To roll back a later release, use Cloudflare's Worker version/rollback workflow
for this Worker only. To unpublish this new guide, remove this Worker's scoped
route; do not remove or modify the guide domain or shared router.

## Content boundaries

Inspired by Shep Bryan's LinkedIn post, not endorsed by or attributed to him
beyond the original topic selection. Deployment/productivity claims are
self-reported. All numeric cost examples are synthetic. Pseudocode and toy-lab
limitations are explicit. Provider-specific behavior should be rechecked
against current documentation before implementation.
