# dalindev GitHub Profile README — Mission Control Update

**Date:** 2026-05-24
**Target repo:** `dalindev/dalindev` (GitHub special profile repo, this one)
**Source of truth:** `dalin.dev/index.html` + `Dalin_Huang_Resume_2026.pdf`

## Goal

Mirror the dalin.dev hero section on the GitHub profile, plus the two animated console widgets — streaming `system.live` log and `finetune.v17` LoRA training monitor — re-implemented as standalone SMIL-animated SVGs.

## Why SVG, not GIF

GIFs of the dalin.dev demo are 1–5 MB, fixed loop, can't be updated cheaply. SVGs with SMIL `<animate>` tags are ~8 KB each, infinite loop, render natively in both GitHub dark + light themes, and survive being reloaded by browsers (no "first frame frozen" issue you sometimes get with GIFs in image proxies).

## Final Structure

Markdown content + two SVG files.

### 1. Hero (markdown)

Mirrors the dalin.dev hero section text, but skips the topbar/buttons since the profile page has its own chrome.

```markdown
# Dalin Huang

### Senior Full Stack Developer / AI Developer

Building AI agent platforms at **Parker AI**. Async pipelines that process billions of data points a day. Fine-tunes open-weight LLMs with LoRA. Eleven years shipping production systems — backend, frontend, and the weird stuff in between.
```

### 2. `media/term-stream.svg` — streaming log

- 800 × 180, Mac terminal chrome with traffic lights
- Title: `dalin@parker-ai — system.live`
- Right side: `● STREAMING` indicator (green dot, blinks at 1.8s)
- 12 pre-rendered log lines covering 6 scroll frames at 1.5s each (9 s loop)
- `<animateTransform>` with `calcMode="discrete"` translates the log group up by 18 px each tick
- Clip rect (y=46, h=128) shows exactly 7 lines, no ascender/descender bleed
- Color coding matches dalin.dev: `.ts` (dim timestamp), `.key` (light gray), `.acc` (amber), `.ok` (green), `.warn` (yellow). Default `.term` fill is `#c9d1d9` so untyped text remains visible.

Log content (rotating sample):

```
[18:54:21] agent.classify   · 482 ads · 96.4% acc
[18:54:22] supabase.read    ok · replica-2 · 14ms
[18:54:23] agent.parker     · batch 482 · 12.4M embeddings
[18:54:24] finetune.v17     LoRA · step 1240/2000
[18:54:25] scraper.adset    ok · 87 sources synced
[18:54:26] dashboard.ttq    · 38ms p50 · 124ms p95
[18:54:27] [!] rate-limit   · backoff 2s · retry · ok
[18:54:28] f1.score         = 0.794 ↑
[18:54:29] gemini.batch     · 12 jobs queued
[18:54:30] embeddings.write ok · 3.2K vectors
[18:54:31] dashboard.kpi    · uptime 99.9% · p95 124ms
[18:54:32] agent.classify   · 421 ads · 96.7% acc
```

### 3. `media/office-floor.svg` — agent crew dashboard

- 800 × 260, terminal chrome titled `office-floor — crew of 8 · 5 busy · 2 idle · 1 offline`
- 4×2 grid of 186×96 agent cards, each with:
  - Status dot (filled colored + blink for busy, hollow gray for idle, filled red for offline)
  - Role name in agent color
  - Model name (dim)
  - 2-line task description (light gray + dim second line; italic for idle agents)
- Color map: Claude Opus → `#f59e0b` amber; Gemini → `#60a5fa` blue; GPT (idle) → `#6e7681` gray ring; Whisper (idle) → gray ring; DeepSeek (offline) → `#ef4444` red
- Busy agents' dots blink in staggered cycles (begin offsets 0s / 0.3s / 0.6s / 0.9s / 1.2s) so they don't pulse in unison
- Agent data sourced from `OFFICE_AGENTS` const in `dalin.dev/index.html` line ~1947

### 4. `media/term-finetune.svg` — LoRA training monitor

- 800 × 240, Mac terminal chrome
- Title: `finetune.v17 — qwen-3.6-27b · A100`
- Right side: `● TRAINING` indicator (blinks 1.8s)
- 3-state cycle for STEP counter via overlapping `<text>` opacity animations: `1258 → 1264 → 1271`
- Matching 3-state cycle for percentage: `63% → 64% → 66%`
- Progress bar `<rect>` width animates `126 → 135 → 126` continuously over 9 s
- GPU bar fluctuates `73–78` over 6 s, CPU bar `34–42` over 4.5 s (gives "alive" feel without random jitter)
- Static rows: loss / val / lr · VRAM · temp · RAM · recent 3 log lines

### 5. Footer (markdown)

```markdown
---

**→ [dalin.dev](https://dalin.dev)** · Three.js System Map · live terminals · built with Claude Opus 4.7

[LinkedIn badge] [Stack Overflow badge] [X badge]
```

## Technical decisions

- **`<img>` vs `<object>`:** README references SVG via `<img>` (markdown-native). On GitHub's image proxy, SMIL animations work in modern browsers. Local preview uses `<object>` because the headless preview browser doesn't run SMIL inside `<img>` (real browsers do).
- **No JS, no external fonts:** SVGs are self-contained and use the system monospace stack.
- **`font-feature-settings: "liga" 0`** disables ligatures so `--`, `==`, `>=` etc. render as separate glyphs.
- **`fill: #c9d1d9` on `.term`:** SVG default text fill is black, invisible on the dark terminal background. Setting the default on the parent class lets untyped tspans inherit a readable color.
- **XML comment escape:** SVG comments can't contain `--`. The `// stack core` comment was rewritten to avoid the double-hyphen.

## Local preview workflow

1. `python3 -m http.server 9876 --bind 127.0.0.1 --directory /tmp/dalindev` (or the project root)
2. Open `http://127.0.0.1:9876/preview.html`
3. The preview page renders the README content with the SVGs embedded via `<object>` so animations play in headless browsers as well.

## Iteration history

- **v1:** 5 sections including GitHub Stats and a 6-category heat-coded skill matrix.
- **v2:** Dropped Stats, top-langs, heat tiers, metric chips, visit counter, easter-egg breadcrumb. 4 sections, ~30 lines.
- **v3:** Split AI row into practices (Agentic, Context Eng, Prompt Eng, Agent Tools, AI Workflows, Evals) + implementation stack.
- **v4:** Replaced text Active Agent + Core Stack with single animated terminal-banner SVG (`whoami / cat role.md / stack --core / open dalin.dev`).
- **v5:** Replaced the typewriter banner with the dalin.dev hero text + two animated console SVGs (streaming log + LoRA training monitor) to match how dalin.dev presents the work.
- **v6 (this spec):** Added the OFFICE FLOOR panel — 4×2 grid of agent cards showing the Parker AI crew (Main, Fine-tune, Classifier, Analyze, Web Search, Failover, Transcribe, Overthink). Also rewrote term-stream.svg and term-finetune.svg using inline `fill` attributes instead of a `<style>` block, because GitHub's image proxy doesn't reliably apply CSS classes when SVGs are loaded via `<img>` — text without an explicit `fill` was falling back to SVG's default black, invisible on the dark terminal background.
