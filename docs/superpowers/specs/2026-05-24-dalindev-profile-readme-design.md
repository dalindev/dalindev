# dalindev GitHub Profile README — Mission Control Update

**Date:** 2026-05-24
**Target repo:** `dalindev/dalindev` (GitHub special profile repo, this one)
**Source of truth:** `dalin.dev/index.html` (portfolio site, v2026.1)

## Goal

Update this profile README to reflect Dalin's current identity (Senior FS / AI Developer at Parker AI) and match the "Mission Control" terminal aesthetic of dalin.dev. The previous README was generic — no mention of Parker AI, AI/agent work, LoRA, or the portfolio site.

## Out of scope

- No Featured Projects section — pinned repos already serve that purpose.
- No new images or screenshots — markdown only.
- No animations or interactive elements — beyond what markdown supports.
- No changes to pinned repos, profile bio fields, or any other GitHub profile surface.

## Final Structure (5 sections)

### 1. Boot Sequence Header

A fenced code block styled as a terminal boot log. Sets the Mission Control tone immediately.

```
$ dalin@parker-ai > booting mission-control...
[✓] identity ........... Senior Full Stack / AI Developer
[✓] location ........... Canada · UTC-04:00
[✓] tenure ............. 11 years shipping production systems
[✓] mission ............ → dalin.dev
```

### 2. Active Agent — Parker AI

Heading: `## 🛰️ Active Agent`

Sub-line: `` **`PARKER-AI`** · Senior FS / AI Developer · Dec 2023 → Present · `status: live` ``

Bullets (verbatim from `dalin.dev/index.html` ROLES['parker-ai'].bullets):
- Architected AI agent platform for marketing/creative strategy
- Pipelines: billions of data points/day · millions of ads · TBs of media
- LoRA fine-tunes + auto-research loop — F1 **0.7% → 79%** over 30 iterations
- Supabase Postgres at scale: partitioning, indexing, rollups, read-replicas
- One of the best Meta ad dashboards on the market — fast, fully sortable, daily data up to 1 year
- Async batch on Gemini Batch API — large-scale ad classification, media analysis, embeddings

Metric row (inline code chips):
`` `DATA/DAY ~B` · `SCALE ~100×` · `ITER 30+` · `UPTIME 99.9%` ``

### 3. System Capabilities

Heading: `## ⚡ System Capabilities`

Legend (blockquote): `> 🔥 hot · 🟡 warm · ⚪ cool`

Categories with inline heat-coded text (matches `SKILLS` const in `dalin.dev/index.html`), inside a fenced code block to preserve column alignment:

```
AI / LLM    🔥 LoRA  🔥 Gemini API  🔥 Claude API  🔥 OpenAI API  🔥 Embeddings  🔥 Eval loops
            🟡 Claude Code  🟡 Cursor  🟡 ChatGPT  ⚪ Grok

Frontend    🔥 React  🔥 Next.js  🔥 TanStack Q  🔥 TypeScript
            🟡 Tailwind  🟡 Shadcn/UI  🟡 Chakra UI  🟡 HTML5/CSS3

Backend     🔥 Node.js  🔥 Python
            ⚪ Ruby  ⚪ PHP  ⚪ Java  ⚪ Perl

Data        🔥 PostgreSQL  🔥 Supabase
            🟡 Redis  🟡 Elasticsearch  ⚪ MySQL  ⚪ Firebase

Cloud       🔥 Supabase  🔥 GCP
            🟡 AWS  🟡 Azure  🟡 Vercel  ⚪ Netlify  ⚪ Firebase  ⚪ Tencent

Frameworks  🔥 Next.js  🟡 Remix
            ⚪ Rails  ⚪ Django  ⚪ Flask  ⚪ Vue  ⚪ Express  ⚪ Backbone  ⚪ CodeIgniter
```

### 4. GitHub Stats

Heading: `## 📊 GitHub Stats`

Keep the existing 3 stat cards exactly as they were:
- github-readme-stats main card (dark theme)
- nirzak-streak-stats
- top-langs compact layout

### 5. Open Mission Control (footer)

Heading: `## 🌐 Open Mission Control`

- Call-to-action: `**→ [dalin.dev](https://dalin.dev)**`
- Stats line: `Three.js System Map · 8 AI agents · live terminals · built with Claude Opus 4.7`
- Easter-egg breadcrumb (italic): `_Try: dalin.dev/?boot=1_`
- Socials line: LinkedIn / Stack Overflow / X badges (unchanged from previous README)
- Horizontal rule, then visit counter badge (unchanged)

## Tone & voice

- Terminal / engineering tone — no marketing fluff.
- Numbers and proper nouns over adjectives.
- Lowercase tech names where the brand uses lowercase (e.g., `parker-ai` in the boot line).
- No emojis inside the boot block (keeps it pure terminal).
- Emojis only for section headings (matches existing style: 🛰️ ⚡ 📊 🌐).

## What got removed from previous README

- The "About Me" line ("passionate full-stack developer who loves Meme/Ski/Fishing/Tech") — replaced by boot sequence.
- The big `# 💻 Tech Stack:` shield wall — replaced by heat-coded categories.

## What stayed unchanged

- All three GitHub stats cards (URLs and parameters identical).
- Visit counter badge at the bottom.
- LinkedIn / Stack Overflow / X social badges (moved into footer).

## Data sources

All role/skill content traceable to `dalin.dev/index.html`:
- `ROLES` const → Active Agent bullets and metrics
- `SKILLS` const → System Capabilities heat levels
- `<title>` meta tag → identity line in boot block
- `dalin.dev` README → "8 AI agents · built with Claude Opus 4.7" stats line + `?boot=1` easter egg
