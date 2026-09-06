# Organized AI — editorial design direction

On September 5, 2026, the user requested the aesthetics of the local reference
at `http://127.0.0.1:4180/#home`. Its source is the independent
`../cowork-aalo-alternate/` project, which was inspected but not modified.

This editorial direction supersedes the earlier recordings-style layout.
The original supplied notes remain preserved in
`design/recordings-design-kit.md`, outside deployed assets.

## Applied

- Warm black (`#10100b`) and ivory (`#fffcf4`) sections with yellow accents.
- Oversized, regular-weight Inter headings, restrained labels, thin rules,
  generous negative space, and rounded pill actions.
- Full-width atmospheric homepage with a procedural golden particle field.
- Light editorial chapter pages with a compact reading sidebar and page outline.
- A numbered curriculum without filled dashboard-style cards.
- A full-screen native chapter dialog with focus containment and Escape closing.
- Local Inter and JetBrains Mono; no runtime external fonts or animation libraries.
- Manual motion pause, OS reduced-motion support, and off-screen/hidden-tab pause.
- Versioned stylesheet/script URLs and revalidated HTML to prevent mixed designs.

## Deliberate adaptations

The product remains a long-form engineering guide, not a cowork meeting
synthesis. No session data, recordings, source links, or local-only labels from
the reference were carried into the guide. Homepage copy describes the guide's
existing curriculum and capstone.

All 12 chapter texts, the glossary, capstone, lab files, and Markdown reading
edition retain their editorial content. Generated companion-project panels now
add worked code, repository links, and four progress milestones per chapter.
Search and progress remain browser-local; the upgraded progress schema migrates
the earlier all-or-nothing completion state and supports export/import.
Chapter navigation remains available without relying on the decorative canvas.
Print styles continue to exclude navigation and art.

No GTM, Stripe, sign-in flow, sponsor assets, or recordings video was added.
The build is still static and framework-free at runtime. Build-time Markdown
rendering is retained so one source continues to generate all reading formats.

## Implementation

- `src/assets/style.css`: local fonts and baseline documentation layout.
- `src/assets/editorial.css`: active light/dark theme and responsive reading UI.
- `src/assets/editorial.js`: procedural art, motion lifecycle, header surface.
- `src/assets/app.js`: search, progress, native menu, code copy, and page outline.
- `src/home.mjs`, `src/shell.mjs`: editorial homepage and shared page structure.
- `scripts/build.mjs`: Markdown rendering, assembly, and asset-version generation.
- `scripts/check.mjs`: theme, navigation, source-content, font, and link checks.
- `src/assets/design-kit.css`: retained previous theme, no longer loaded.
