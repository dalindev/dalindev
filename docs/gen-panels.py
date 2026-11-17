#!/usr/bin/env python3
"""Generates media/ask.svg: a replay of the "Ask the model" panel on dalin.dev.

Plain SVG + SMIL only (no scripts, no CSS, explicit fills), because GitHub shows README images with scripts off.
The questions, answers and "picked by" source are what the real page produces for these questions. The softmax numbers and
hidden activations are from one real page load; the network starts from random weights, so they differ a little on every visit.
Usage: python3 docs/gen-panels.py media
"""
import sys, textwrap, json, random, os
from xml.sax.saxutils import escape as E

OUT = sys.argv[1]
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Monaco, Consolas, monospace"
W, H = 800, 510
P = 15.0                      # seconds per question
ANS_FS, ANS_CW, ANS_LH, WRAP = 12, 7.224, 18, 64   # answer text: font size, char width, line height, chars per line
TOK = 0.07                    # seconds per token

QA = [
    dict(q="AI", by="keywords",
         a="AI is my day job. At Parker AI I built a 10+ agent engineering loop, an automated research and training loop on a GPU "
           "cluster, and an eval framework that benchmarks 50+ models on production tools, MCP, and context. The fine-tuned LLMs I "
           "trained match frontier-model quality at 200× lower cost and serve billions of requests a week. The goal is always the "
           "same: agents that do real engineering work, safely.",
         probs=[("is it real?", .51), ("ai", .27), ("vision", .10), ("workflow", .09)], pick=1,
         rel=["Parker AI", "Agent loops", "Self-hosted LLMs", "Evals"]),
    dict(q="agents", by="keywords",
         a="I built a 10+ agent loop covering intake, coding, QA, security, incident response, and release. It runs on top "
           "of Status Island, which tracks live health across 30+ systems. Agents ship to production, write data, and run "
           "migrations. Each kind of change starts behind a human yes and goes automatic as it earns trust, so the "
           "automated share climbs from 10% toward 99%. The last 1% still needs a person. Clean-context QA and Security "
           "agents verify every diff against real replicas, previews, and logs before anything merges. The team itself is "
           "a Chief of Staff bot directing about ten specialist Grok bots (ask me about Grok bots). You can watch a "
           "version of it in the office below.",
         probs=[('agents', 0.99), ('safety', 0.01), ('agent team', 0), ('support', 0)], pick=0,
         rel=["Agent loops", "Grok bots", "Human-in-the-loop", "Verifier agents"]),
    dict(q="fine-tuning", by="similar question",
         a="I trained our self-hosted fine-tuned LLMs. They match frontier-model quality at 200× lower cost and serve "
           "billions of requests a week. Inference runs async on GPU clusters through a job queue with producers and "
           "finalizers, which saves even more. The research and training loop behind them is automated too: agents run the "
           "experiments, monitor the runs, and iterate. On top of that, a continuous learning pipeline turns user "
           "reactions and feedback into a training queue for models and LLM judges. It also distills domain experts' "
           "outputs, chats, and review history into vision+text → text reasoning models. The 👍 button below is a tiny "
           "version of that.",
         probs=[('fine-tuning', 1), ('aijobs', 0), ('inspiration', 0), ('shopify', 0)], pick=0,
         rel=["Fine-tuning", "Self-hosted LLMs", "Learning loop", "Distillation"]),
    dict(q="where is AI going?", by="keywords",
         a="I'm an optimist: I believe AI will build a better future, and I expect AGI around 2027. You can already see the path in "
           "my own work. Agents that used to autocomplete code now take a ticket, write the fix, test it, and verify the deploy, "
           "while a person keeps the gate on anything risky. The next step is agents that improve themselves safely: they learn "
           "from their own incidents, run their own experiments, and earn more autonomy as their track record grows. The hard part "
           "isn't raw intelligence any more, it's trust: evals, guardrails, and verification. That's the part I build.",
         probs=[("vision", .99), ("fit", .01), ("hello", .00), ("ai", .00)], pick=0,
         rel=["Agent loops", "Human-in-the-loop", "Evals", "Verifier agents"]),
    dict(q="is this a real LLM?", by="similar question",
         a="Partly, and I'd rather be upfront about it. The network in the picture is real: a tiny classifier trained in your "
           "browser when the page loaded, and the thumbs-up runs a real gradient step on it. The rest is a show of how an LLM "
           "works: there's no API call and no large language model, and nothing you type leaves your browser. The answers were "
           "written ahead of time from Dalin's resume and notes, so I can't invent facts, though I can still pick the wrong "
           "answer. The real models are Dalin's day job: self-hosted fine-tuned LLMs "
           "that match frontier-model quality at 200× lower cost.",
         probs=[("is it real?", .97), ("ai", .02), ("hello", .00), ("agents", .00)], pick=0,
         rel=["Self-hosted LLMs", "Fine-tuning"]),
]
T = P * len(QA)
# Real hidden-layer activations (64 ReLU units, scaled to the strongest one) from the site's trained network, per question.
ACTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acts.json')))
RND = random.Random(7)


def timing(i):
    qa = QA[i]
    t_typed = i * P + 0.6 + len(qa["q"]) * 0.08
    st = [t_typed + 0.15 + k * 0.35 for k in range(5)]        # tokenize, embed, retrieve, prefill, decode start
    n = len(qa["a"].split(' '))
    return st, st[4] + n * TOK, (i + 1) * P - 0.3, n
STAGES = ["TOKENIZE", "EMBED", "RETRIEVE", "PREFILL", "DECODE", "BACKPROP"]


def f(x):
    return f"{x:.4f}".rstrip('0').rstrip('.')


def on(t, t_end):
    """Step opacity: hidden, shown from t to t_end (seconds in the loop), hidden again."""
    t, t_end = max(t, 0.02), min(t_end, T - 0.02)
    return f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;{f(t / T)};{f(t_end / T)}" dur="{f(T)}s" repeatCount="indefinite"/>'


def chip(x, y, label, fill="#161b22", stroke="#30363d", color="#c9d1d9", fs=10, pad=9, h=20):
    w = len(label) * fs * 0.602 + pad * 2
    return w, (f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
               f'<text x="{f(x + w / 2)}" y="{y + h / 2 + fs * 0.36:.1f}" text-anchor="middle" font-size="{fs}" fill="{color}">{E(label)}</text>')


s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ask the model: a replay of the question box on dalin.dev">', '  <defs>']
# typing: one clip per question, growing a character at a time
for i, qa in enumerate(QA):
    t0, n = i * P + 0.6, len(qa["q"])
    ts = [t0 + k * 0.08 for k in range(n + 1)]
    end = (i + 1) * P - 0.3
    vals = ['0'] + [f(k * 7.83 + 1) for k in range(n + 1)] + ['0', '0']
    keys = [0] + ts + [end, T]
    s.append(f'    <clipPath id="type{i}"><rect x="48" y="50" height="34" width="0"><animate attributeName="width" calcMode="discrete" values="{";".join(vals)}" keyTimes="{";".join(f(k / T) for k in keys)}" dur="{f(T)}s" repeatCount="indefinite"/></rect></clipPath>')
s.append('  </defs>')

# ── window chrome ──
s.append(f'''  <rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>
  <path d="M 0,10 A 10,10 0 0 1 10,0 L {W - 10},0 A 10,10 0 0 1 {W},10 L {W},36 L 0,36 Z" fill="#161b22"/>
  <line x1="0" y1="36" x2="{W}" y2="36" stroke="#30363d"/>
  <circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="22" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#6e7681" letter-spacing="1">dalin-lm · tiny classifier · trains in your browser in ~70 ms</text>
  <g transform="translate(722, 22)" font-family="{FONT}" font-size="11" letter-spacing="1">
    <circle cx="-12" cy="-4" r="4" fill="#4ade80"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>
    <text x="0" y="0" fill="#4ade80">REPLAY</text>
  </g>''')
s.append(f'  <g font-family="{FONT}">')

# ── composer ──
s.append('    <rect x="20" y="48" width="760" height="36" rx="9" fill="#0b1210" stroke="#2f6f4a"><animate attributeName="stroke" values="#2f6f4a;#4ade80;#2f6f4a" dur="3s" repeatCount="indefinite"/></rect>')
s.append('    <text x="32" y="71" font-size="13" font-weight="700" fill="#4ade80">❯</text>')
s.append('    <rect x="710" y="55" width="62" height="22" rx="5" fill="#12261b" stroke="#2f6f4a"/><text x="741" y="70" text-anchor="middle" font-size="10" font-weight="700" fill="#4ade80" letter-spacing="1">ASK ↵</text>')
for i, qa in enumerate(QA):
    s.append(f'    <text x="49" y="71" font-size="13" fill="#e6edf3" clip-path="url(#type{i})">{E(qa["q"])}</text>')

# ── TRY chips ──
s.append('    <text x="24" y="108" font-size="9" fill="#6e7681" letter-spacing="1">TRY</text>')
x = 52
for label in ["agents", "fine-tuning", "where is AI going?", "is this a real LLM?"]:   # the site's chips, minus "why hire you?"; "AI" is the page's own opening demo
    w, svg = chip(x, 94, label, color="#8b949e")
    hot = [i for i, qa in enumerate(QA) if qa["q"] == label]
    s.append('    ' + svg)
    if hot:   # the chip lights up while "its" question is being asked
        i = hot[0]
        _, svg2 = chip(x, 94, label, fill="#12261b", stroke="#4ade80", color="#4ade80")
        s.append(f'    <g opacity="0">{svg2}{on(i * P + 0.2, (i + 1) * P - 0.3)}</g>')
    x += w + 6

# ── stage bar ──
SY, SW = 124, 760 / 6
s.append(f'    <line x1="20" y1="{SY}" x2="780" y2="{SY}" stroke="#21262d"/><line x1="20" y1="{SY + 24}" x2="780" y2="{SY + 24}" stroke="#21262d"/>')
for k, name in enumerate(STAGES):
    x0 = 20 + k * SW
    if k:
        s.append(f'    <line x1="{f(x0)}" y1="{SY}" x2="{f(x0)}" y2="{SY + 24}" stroke="#21262d"/>')
    s.append(f'    <text x="{f(x0 + 10)}" y="{SY + 16}" font-size="9.5" fill="#484f58" letter-spacing="1">0{k + 1} {name}</text>')

# ── static frame of the body ──
BY = SY + 24                                   # body top
DIV, FOOT = 514, H - 44
s.append(f'    <line x1="{DIV}" y1="{BY}" x2="{DIV}" y2="{FOOT}" stroke="#21262d"/>')
s.append(f'    <text x="24" y="{BY + 18}" font-size="9" fill="#6e7681" letter-spacing="1">ANSWER · streamed token by token</text>')
s.append(f'    <text x="{DIV + 14}" y="{BY + 18}" font-size="9" fill="#6e7681" letter-spacing="1">CLASSIFIER · real · 68,460 params</text>')

# the classifier: input words → all 64 hidden units (4 sub-columns of 16) → top answers
NY = BY + 30
IN = (DIV + 22, NY + 62)
HID = [(DIV + 74 + (k // 16) * 13, NY + 1 + (k % 16) * 8.3) for k in range(64)]
OUTX, OUTS = DIV + 158, [NY + 14, NY + 46, NY + 78, NY + 110]
s.append('    <g stroke="#30363d" stroke-width="0.4" fill="none" opacity="0.55">')
for k, (hx, hy) in enumerate(HID):
    if k % 2 == 0:
        s.append(f'      <line x1="{IN[0]}" y1="{IN[1]}" x2="{hx}" y2="{f(hy)}"/><line x1="{hx}" y1="{f(hy)}" x2="{OUTX}" y2="{OUTS[k % 4]}"/>')
s.append('    </g>')
s.append(f'    <circle cx="{IN[0]}" cy="{IN[1]}" r="4" fill="#a78bfa"/>')
TOPN = 12
for k, (hx, hy) in enumerate(HID):
    ev = [(0.0, 0.1)]                                  # (time, opacity) steps over the whole loop
    for i, qa in enumerate(QA):
        st, t_done, t1, n = timing(i)
        h = ACTS[qa["q"]]["h"]
        base = 0.1 + 0.9 * h[k]
        ev.append((st[1], base))                       # EMBED: the question's real activation appears
        if k in sorted(range(64), key=lambda j: -h[j])[:TOPN]:
            for m in range(0, n, 2):                   # the strongest units flicker while tokens are written
                ev.append((st[4] + m * TOK, max(0.25, min(1, base * RND.uniform(0.45, 1.15)))))
            ev.append((t_done, base))
        ev.append((t1, 0.1))
    vals = ';'.join(f"{v:.2f}".rstrip('0').rstrip('.') for _, v in ev)
    keys = ';'.join(f(t / T) for t, _ in ev)
    s.append(f'    <circle cx="{hx}" cy="{f(hy)}" r="2.3" fill="#60a5fa" opacity="0.1"><animate attributeName="opacity" calcMode="discrete" values="{vals}" keyTimes="{keys}" dur="{f(T)}s" repeatCount="indefinite"/></circle>')
for y in OUTS:
    s.append(f'    <circle cx="{OUTX}" cy="{y}" r="3.2" fill="#161b22" stroke="#6e7681"/>')
AX = NY + 138
s.append(f'    <text x="{IN[0]}" y="{AX}" text-anchor="middle" font-size="8.5" fill="#6e7681">words</text>')
s.append(f'    <text x="{DIV + 94}" y="{AX}" text-anchor="middle" font-size="8.5" fill="#6e7681">1 layer · 64 units</text>')
s.append(f'    <text x="{OUTX + 44}" y="{AX}" text-anchor="middle" font-size="8.5" fill="#6e7681">softmax · top 4 of 44</text>')

# next-token panel (the simulated decoder)
TY = AX + 14
s.append(f'    <line x1="{DIV}" y1="{TY}" x2="780" y2="{TY}" stroke="#21262d"/>')
s.append(f'    <text x="{DIV + 14}" y="{TY + 18}" font-size="9" fill="#6e7681" letter-spacing="1">NEXT TOKEN · simulated top-5</text>')
BARX, BARW = DIV + 86, 150

# ── per question ──
for i, qa in enumerate(QA):
    st, t_done, t1, _n = timing(i)
    t_dec = st[4]
    words = qa["a"].split(' ')
    lines = textwrap.wrap(qa["a"], WRAP)
    hq = ACTS[qa["q"]]["h"]
    top = sorted(range(64), key=lambda j: -hq[j])[:TOPN]
    s.append(f'    <g><!-- Q{i + 1}: {E(qa["q"])} -->')

    # stage highlights: each one lights while it runs; DECODE stays lit while tokens stream
    for k in range(5):
        a, b = st[k], (st[k + 1] if k < 4 else t_done)
        x0 = 20 + k * SW
        s.append(f'      <g opacity="0"><rect x="{f(x0)}" y="{SY}" width="{f(SW)}" height="24" fill="#12261b"/><rect x="{f(x0)}" y="{SY + 22}" width="{f(SW)}" height="2" fill="#4ade80"/>'
                 f'<text x="{f(x0 + 10)}" y="{SY + 16}" font-size="9.5" font-weight="700" fill="#4ade80" letter-spacing="1">0{k + 1} {STAGES[k]}</text>{on(a, b)}</g>')

    # the question, echoed above the answer
    s.append(f'      <text x="24" y="{BY + 40}" font-size="11" opacity="0"><tspan fill="#4ade80" font-weight="700">YOU ❯</tspan> <tspan fill="#8b949e">{E(qa["q"])}</tspan>{on(st[0], t1)}</text>')

    # the answer, one token at a time, with a cursor block riding the last token
    n, y0 = 0, BY + 62
    for li, ln in enumerate(lines):
        col = 0
        for wd in ln.split(' '):
            tw = t_dec + n * TOK
            xw = 24 + col * ANS_CW
            s.append(f'      <text x="{f(xw)}" y="{y0 + li * ANS_LH}" font-size="{ANS_FS}" fill="#e6edf3" opacity="0">{E(wd)}{on(tw, t1)}</text>')
            s.append(f'      <rect x="{f(xw + len(wd) * ANS_CW + 2)}" y="{y0 + li * ANS_LH - 10}" width="6" height="12" fill="#4ade80" opacity="0">{on(tw, tw + TOK)}</rect>')
            col += len(wd) + 1
            n += 1

    # the wires of the strongest units light up for this question; pulses run through the top three during EMBED/RETRIEVE
    g = [f'      <g stroke="#4ade80" stroke-width="0.7" fill="none" opacity="0">{on(st[1], t1)}']
    for k in top:
        hx, hy = HID[k]
        g.append(f'<path d="M {IN[0]},{IN[1]} L {hx},{f(hy)} L {OUTX},{OUTS[qa["pick"]]}" stroke-opacity="{0.15 + 0.45 * hq[k]:.2f}"/>')
    s.append(''.join(g) + '</g>')
    for k in top[:3]:
        hx, hy = HID[k]
        s.append(f'      <circle r="3" fill="#4ade80" opacity="0"><animateMotion path="M {IN[0]},{IN[1]} L {hx},{f(hy)} L {OUTX},{OUTS[qa["pick"]]}" dur="{f(T)}s" keyPoints="0;0;1;1" keyTimes="0;{f(st[1] / T)};{f(st[3] / T)};1" calcMode="linear" repeatCount="indefinite"/>{on(st[1], st[3])}</circle>')
    # the network's real softmax for this question
    for oi, (name, p) in enumerate(qa["probs"]):
        y, picked = OUTS[oi], oi == qa["pick"]
        s.append(f'      <g opacity="0">{on(st[2], t1)}' + (f'<circle cx="{OUTX}" cy="{y}" r="4.2" fill="#4ade80"/>' if picked else '')
                 + f'<text x="{OUTX + 9}" y="{y + 3.5}" font-size="9.5" font-weight="{700 if picked else 400}" fill="{"#4ade80" if picked else "#8b949e"}">{E(name)} {p:.2f}</text></g>')

    # next-token panel: the top row is the token being written (changes on every token); the runners-up rotate
    y1 = TY + 34
    s.append(f'      <g opacity="0">{on(t_dec, t1)}<rect x="{BARX}" y="{y1 - 4}" width="{BARW}" height="5" rx="2.5" fill="#21262d"/></g>')
    probs = [RND.uniform(0.42, 0.93) for _ in words]
    bw = ';'.join(['0'] + [f(BARW * p) for p in probs] + ['0'])
    bk = ';'.join(f(x / T) for x in [0] + [t_dec + m * TOK for m in range(len(words))] + [t1])
    s.append(f'      <rect x="{BARX}" y="{y1 - 4}" height="5" rx="2.5" fill="#4ade80" width="0"><animate attributeName="width" calcMode="discrete" values="{bw}" keyTimes="{bk}" dur="{f(T)}s" repeatCount="indefinite"/></rect>')
    for m, (wd, pr) in enumerate(zip(words, probs)):
        tw = t_dec + m * TOK
        s.append(f'      <g opacity="0">{on(tw, tw + TOK if m < len(words) - 1 else t1)}<text x="{DIV + 14}" y="{y1 + 3}" font-size="9.5" fill="#e6edf3">{E(wd[:10])}</text><text x="{BARX + BARW + 8}" y="{y1 + 3}" font-size="9" fill="#4ade80">{pr:.2f}</text></g>')
    step = max(len(words) // 8, 1)
    others = [w for w in dict.fromkeys(words) if len(w) > 2][3:60:3]
    for fi in range(8):
        a = t_dec + fi * step * TOK
        b = t_dec + (fi + 1) * step * TOK if fi < 7 else t1
        g = [f'      <g opacity="0">{on(a, b)}']
        for j in range(1, 5):
            c, pr = others[(fi * 3 + j) % len(others)], [0, 0.17, 0.08, 0.04, 0.02][j] * RND.uniform(0.6, 1.2)
            yy = TY + 34 + j * 14
            g.append(f'<text x="{DIV + 14}" y="{yy + 3}" font-size="9.5" fill="#8b949e">{E(c[:10])}</text>'
                     f'<rect x="{BARX}" y="{yy - 4}" width="{BARW}" height="5" rx="2.5" fill="#21262d"/><rect x="{BARX}" y="{yy - 4}" width="{f(BARW * pr)}" height="5" rx="2.5" fill="#60a5fa"/>'
                     f'<text x="{BARX + BARW + 8}" y="{yy + 3}" font-size="9" fill="#6e7681">{pr:.2f}</text>')
        g.append('</g>')
        s.append(''.join(g))

    # after the last token: "open in map" chips and the stats line
    yc = y0 + len(lines) * ANS_LH + 2
    g, x = [f'      <g opacity="0">{on(t_done + 0.2, t1)}<text x="24" y="{yc + 14}" font-size="9" fill="#6e7681" letter-spacing="1">OPEN IN MAP →</text>'], 110
    for r in qa["rel"]:
        w, svg = chip(x, yc, r, fill="#151b2e", stroke="#3b4a7a", color="#a5b4fc", fs=9.5, pad=8, h=20)
        g.append(svg)
        x += w + 6
    g.append('</g>')
    s.append(''.join(g))
    secs = len(words) * TOK
    s.append(f'      <text x="24" y="{FOOT - 12}" font-size="9.5" fill="#6e7681" opacity="0">{len(qa["q"].split())} in · {len(words)} out · {secs:.1f}s · picked by <tspan fill="#c9d1d9" font-weight="700">{E(qa["by"])}</tspan> · answers are pre-written, not generated{on(t_done + 0.2, t1)}</text>')
    s.append('    </g>')

# ── footer ──
s.append(f'    <line x1="0" y1="{FOOT}" x2="{W}" y2="{FOOT}" stroke="#21262d"/>')
s.append(f'    <text x="24" y="{FOOT + 27}" font-size="11" fill="#6e7681">a replay of dalin.dev · there, the network trains in your browser and you can type</text>')
s.append(f'    <text x="776" y="{FOOT + 27}" text-anchor="end" font-size="11" font-weight="700" fill="#4ade80">ask it yourself → dalin.dev</text>')
s.append('  </g>')
s.append('</svg>')
open(f'{OUT}/ask.svg', 'w').write('\n'.join(s) + '\n')
print('wrote ask.svg', 'loop', T, 's', 'lines', [len(textwrap.wrap(q["a"], WRAP)) for q in QA])
