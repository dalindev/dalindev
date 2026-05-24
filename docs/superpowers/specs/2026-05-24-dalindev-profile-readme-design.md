# dalindev GitHub Profile README — Mission Control Update

**Date:** 2026-05-24
**Target repo:** `dalindev/dalindev` (GitHub special profile repo, this one)
**Source of truth:** `dalin.dev/index.html` + `Dalin_Huang_Resume_2026.pdf`

## Goal

Update this profile README to reflect Dalin's current identity (Senior FS / AI Developer at Parker AI) and match the "Mission Control" terminal aesthetic of dalin.dev. Keep it short — this is a bio, not a portfolio.

## Design principle: ruthless simplicity

A profile README serves a single visitor goal: "is this person interesting enough to click into their projects or dalin.dev?" Everything that doesn't serve that goal is noise. Final structure intentionally drops:

- GitHub Stats cards (visual filler, not differentiating)
- Top-languages chart (same)
- Heat-coded warm/cool skill tiers (interesting on dalin.dev's heat map; on a bio they bury the primary stack)
- Metric chip row (numbers already live in bullets above)
- Easter-egg breadcrumb (defeats the purpose; charm belongs on dalin.dev itself)
- Visit counter (decorative)
- The big shield-badge tech wall from the previous README

## Final Structure (4 sections, ~30 lines)

### 1. Boot Sequence Header

```
$ dalin@parker-ai > booting mission-control...
[✓] identity ........... Senior Full Stack / AI Developer
[✓] location ........... Ottawa, Canada
[✓] tenure ............. 11 years shipping production systems
[✓] mission ............ → dalin.dev
```

### 2. Active Agent — Parker AI

`## 🛰️ Active Agent`

Sub-line: `` **`PARKER-AI`** · Senior FS / AI Developer · Dec 2023 → Present · `status: live` ``

Four bullets (trimmed from six). Kept the strongest: differentiated work, headline metric, scale, and stack signal:
- Architected AI agent platform for marketing/creative strategy
- LoRA fine-tunes + auto-research loop — F1 **0.7% → 79%** across 30+ iterations
- Pipelines: billions of data points/day · millions of ads · TBs of media
- Async ad classification on Gemini Batch API + Supabase Postgres at scale

### 3. Core Stack

`## ⚡ Core Stack`

Four lines inside a fenced code block. Only the primary stack — the things actually shipping today. Anyone curious about exploratory or older tech can see the heat-map on `dalin.dev`.

```
AI         LoRA · Gemini API · Claude API · OpenAI API · Embeddings
Frontend   React · Next.js · TypeScript · TanStack Query
Backend    Node.js · Python
Data       PostgreSQL · Supabase · GCP
```

### 4. Open Mission Control (footer)

`## 🌐 Open Mission Control`

- One-line call-to-action: `**→ [dalin.dev](https://dalin.dev)** · Three.js System Map · live terminals · built with Claude Opus 4.7`
- Socials line: LinkedIn / Stack Overflow / X badges (unchanged)

## Tone & voice

- Terminal / engineering tone — no marketing fluff.
- Numbers and proper nouns over adjectives.
- Lowercase tech names where the brand uses lowercase (e.g., `parker-ai` in the boot line).
- No emojis inside the boot block (keeps it pure terminal).
- Emojis only on section headings (🛰️ ⚡ 🌐).

## Data sources

- `dalin.dev/index.html` ROLES['parker-ai'] → Active Agent bullets
- `Dalin_Huang_Resume_2026.pdf` page 1 → Ottawa location, F1 numbers `0.7% → 28% (v1) → 79% (v16)`
- `dalin.dev` README → "built with Claude Opus 4.7" tag

## Iteration history

- **v1 (initial):** 5 sections including GitHub Stats and 6-category heat-coded skill matrix. Felt overstuffed on a bio.
- **v2 (this spec):** Dropped Stats, top-langs, heat tiers, metric chips, visit counter, and easter-egg breadcrumb. 4 sections, ~30 lines.
