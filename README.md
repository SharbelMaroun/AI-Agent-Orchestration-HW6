# Dual AI Agent Race via MCP Servers — "Cop & Thief"

> Course: **Orchestration of AI Agents**, University of Haifa — Task 6 (ex06).
> This README is the project's **user manual** *and* its **living scientific report**.
> Engineering standards: [`MATERIALS/software_submission_guidelines-V3_Summary.md`](MATERIALS/software_submission_guidelines-V3_Summary.md).
> Design docs: [`docs/`](docs/) ([PRD](docs/PRD.md) · [PLAN](docs/PLAN.md) · [TODO](docs/TODO.md) · [Audit](docs/AUDIT-2026-06-25.md)).

**Status:** 🟦 In progress — documentation phase. Commands marked _planned_ run once the code lands.

---

## 1. Overview
Two autonomous AI agents — a **Cop** and a **Thief** — play a pursuit game on a 2-D grid. Each agent is
backed by its **own MCP server (FastMCP)** and they coordinate in **natural language** under
**partial observation**. A full match is **6 sub-games** (≤25 moves each), run end-to-end with no
manual intervention. The project also ships a **Gmail & Calendar agent** (read inbox → extract a
meeting invite → add a Calendar event → send email); when the match ends, it emails the JSON result.

See [`docs/PRD.md`](docs/PRD.md) for full requirements.

## 2. Installation

### 2.1 System requirements
- **Python ≥ 3.10**
- **[`uv`](https://docs.astral.sh/uv/)** package manager (the only supported manager — no `pip`/`venv`)
- OS: Windows 10/11, macOS, or Linux
- An **LLM provider** — a cloud API key (Anthropic/OpenAI/Gemini) **or** local Ollama (see `docs/PRD.md` FR-7)
- A **Google Cloud OAuth Desktop client** for Gmail/Calendar (see [`docs/PRD_gmail_calendar_agent.md`](docs/PRD_gmail_calendar_agent.md))

### 2.2 Install `uv`
```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version   # verify
```

### 2.3 Install the project
```bash
uv sync          # creates the venv and installs locked dependencies
```

### 2.4 Environment & secrets
1. Copy the template: `cp .env-example .env`
2. **Add your OpenAI API key** in `.env` (git-ignored): `OPENAI_API_KEY=sk-...`. The app auto-loads
   `.env` on every run, so once it's there the natural-language match always uses OpenAI. The model is
   set in `config/config.json` → `llm.model` (default `gpt-4o-mini`). Without a key it runs offline.
3. Put the Google OAuth files (`client_secret.json`, and `token.json` once generated) in a **secret
   folder OUTSIDE this repo**, and point `google.secrets_dir` (in `config/config.json`) at it.
4. **First run is interactive** (one time): a browser opens for OAuth consent → approve as a Google
   **Test user** → `token.json` is written. All subsequent match runs are fully autonomous.

### 2.5 Troubleshooting
| Symptom | Fix |
|---|---|
| `uv sync` fails | Confirm Python ≥3.10 and a fresh terminal after installing `uv`. |
| OAuth "Access blocked / unverified app" | Normal in Testing mode — ensure your Gmail is in **Test users**. |
| Token expired / wrong scopes | Delete `token.json` → re-run → re-consent in the browser. |
| MCP cloud URL unreachable | Avoid org networks blocking non-standard ports; verify firewall/token (see PLAN §3). |

## 3. Usage

### 3.1 Run it — one command
| Command | What it does |
|---|---|
| `uv run cop-thief` | **Natural-language match** (the assignment) → prints the JSON summary |
| `uv run cop-thief --gui` | **Natural-language match → animated GIF** with the agents' NL messages overlaid (`assets/match_nl.gif`) |
| `uv run cop-thief --simple` | Simple heuristic match (no natural language, no LLM) |
| `uv run cop-thief --simple --gui` | Heuristic/`smart` match → `assets/match.gif` |
| `.\run.ps1 [--simple\|--gui]` | Windows wrapper (shortest) |

**Full real run with the GUI:** put your key in `.env` (`OPENAI_API_KEY=sk-...`, see §2.4), then
`uv run cop-thief --gui` — this animates a natural-language sub-game where the cop and thief move on the
board **and** their LLM-interpreted NL messages appear under each frame (`assets/match_nl.gif`). Without a
key it runs the same NL pipeline on a deterministic **offline** backend (no network, no cost). Long form:
`uv run python -m marl_cop_thief [--simple\|--gui]`. All parameters (grid size, moves, scoring, seed,
report recipient, `llm.model`, `strategy.type`) come from `config/config.json` — no flags for them.

### 3.2 Typical workflow
Add `OPENAI_API_KEY` to `.env` → `uv run cop-thief` to watch a natural-language match → `uv run cop-thief
--gui` to render the animation → (with Google OAuth set up) the report email is sent after the 6 games.

### 3.3 Example output
```text
$ uv run cop-thief
{ "sub_games": [ { "index": 0, "winner": "cop", "moves_used": 8, "cop_score": 20, "thief_score": 5 }, ... ],
  "totals": { "cop": 90, "thief": 40 } }
```
A natural-language run log is in [`results/nl_match_sample.txt`](results/nl_match_sample.txt) (see R.5).

## 4. Architecture
Summary in [`docs/PLAN.md`](docs/PLAN.md) (C4 model, ADRs, module layout). Diagrams go in `assets/`.
**Standards alignment:** ISO/IEC 25010 (quality), MIT SQA, Google/Microsoft API guidelines, and
Nielsen's 10 usability heuristics (GUI/CLI) — see [`docs/PLAN.md`](docs/PLAN.md) and `docs/PRD.md` §4.

---

# 📊 Project Report / Results

> **Reporting rule:** we report **everything we do** here as we go — every feature, experiment, and
> decision — with **graphs and screenshots whenever possible**. Images live in `assets/`, generated
> plots and run outputs in `results/`. Updated continuously, not only at submission.

## R.0 Implementation status (code)
| Phase | Component | Status | Evidence |
|---|---|---|---|
| 0 | Scaffolding (uv, config, version/constants, loader) | ✅ done | ruff clean · 100% cov |
| 1 | Game engine (board, models, engine, scoring, barriers) | ✅ done | 100% cov |
| 2 | MCP tool layer + 2 FastMCP servers | 🟦 partial | tools/observation/bus/servers done; transport/auth pending |
| 3 | Orchestrator + SDK + CLI (full local match) | ✅ done | `python -m marl_cop_thief` runs |
| 4 | Decision strategy | ✅ done | cop: greedy + **cornering "smart"** (1-ply look-ahead); thief: greedy baseline + **"smart" evasion** (default, flees + keeps escape room, roams the board); all config-selectable; Q-table optional/pending |
| 5 | Natural-language + LLM | ✅ done | NL encode/decode, ambiguity handler, NL decider; **LLM-written in-character speech** (cop/thief personas, template fallback offline); LLM via gatekeeper |
| 6 | GUI | ✅ done | **modern-dark themed** board (glow cop/thief tokens, barrier slabs, movement trails, capture flash, HUD scoreboard, speech bubbles) · GIF (`--gui`) + **live real-time window** (`--live`, auto-closes when done) |
| 8 | Report builder + Gmail/Calendar agent | 🟦 partial | JSON builders + read/extract/calendar/send tools tested; real OAuth send pending |
| 9 | API gatekeeper | ✅ done | config-driven rate limit + FIFO queue + backpressure + drain + retries/backoff + concurrency + `get_queue_status` (see R.9) |
| 7, 10 | Cloud, research/submission | ⬜ pending | — |

Whole suite: **189 tests, 100% coverage, Ruff zero-violation.** Every `uv run pytest` emits an automated
**JUnit + coverage report** to `results/` (pass/fail per test); expected results and how to regenerate are
in [`results/TEST_REPORT.md`](results/TEST_REPORT.md), with a captured run log at
[`results/test_run.log`](results/test_run.log) (guidelines §6.4). The NL match is runnable via
`uv run cop-thief` (NL is the default; `--simple` for heuristic; `--gui` for a GIF; `--live` for a live
window). The Gmail/Calendar tools are dependency-injected (tested with
fakes); `shared/google_auth.py` builds the real services and needs your Google OAuth `client_secret.json`.

## R.1 Work Log (running changelog)
Newest first.

| Date | What we did | Why | Evidence |
|------|-------------|-----|----------|
| 2026-06-25 | **Phase 10 batch 2 docs + non-square sanity** — non-square match test (3×2, 4×3); PRD §1.5 market/landscape + §1.6 relative-path note; PLAN §3 production secret-store + MCP HTTP-transport (not stdio) + token encrypt/revoke notes; PRD_game_engine special-action clarification | Close audit gaps C6/C14/C15/C18/C21, gap10/37/53/61 | `test_match_runs_on_non_square_boards`; PRD §1.5/1.6, PLAN §3; 197 tests, 100% cov |
| 2026-06-25 | **Budget management (gatekeeper spend counter)** — `shared/budget.py` `BudgetTracker` reads the live gatekeeper call count + config `llm.budget.usd_per_call` for a real-time spend/remaining counter, `forecast_usd(n)`, and a two-stage **alert** (`alert_threshold`) / **over_budget** flag; the CLI prints it after a real run | Required cost forecasting + real-time monitoring + overrun alerts (audit C14/C20) | `shared/budget.py`; 196 tests, 100% cov; README R.7 + config `llm.budget` |
| 2026-06-25 | **Phase 9 research & visualization** — `scripts/sensitivity.py` runs OAT sweeps (visibility radius, grid size) over real offline matches and renders the full chart suite (**line, heatmap, box, scatter**); added `notebooks/analysis.ipynb` (LaTeX Dec-POMDP + Bellman, sensitivity results, 6 academic references). Key finding: NL capture needs visibility (r=0≈blind), peaks at r=1–2, and degrades with board size | Required sensitivity research + visualization (guidelines §11; T9.61–69, T10.23–25) | README R.3 sensitivity section; `assets/sensitivity_*.png`, `moves_boxplot.png`, `scatter_area_moves.png`; `results/sensitivity.txt` |
| 2026-06-25 | **Phase 10 audit/quality closure (batch 1)** — automated **JUnit + coverage report** to `results/` on every `pytest` run + `results/TEST_REPORT.md` (expected results) + committed `test_run.log`; **ISO/IEC 25010** self-assessment (R.10); **Nielsen 10 heuristics + accessibility + standards alignment** (R.11); **`docs/EDGE_CASES.md`** register; **extension-points** table (PLAN §4.1); `__init__.py` in all test dirs | Close graded scientific/quality gaps (guidelines §6.4, §10, §17; audit T10.8–31) | README R.10/R.11, `results/TEST_REPORT.md`, `docs/EDGE_CASES.md`, PLAN §4.1; 189 tests, 100% cov |
| 2026-06-25 | **Smarter thief — fixed the "always goes left" drift** — greedy evasion tied on distance and the fixed `DIRECTIONS_8` order made `max` pick the leftmost move every time. Added a config-selectable `smart` thief (default) ranking moves by `(distance, mobility, centrality)` via `strategy/evasion.py`, used by the simple match, the NL belief-based `_choose`, and the GUI; greedy retained as the R.3 baseline | "The thief keeps making the same move, not smart/varied" — reported in R.3 | `strategy/{smart_thief,evasion}.py`; 189 tests, 100% cov; honest capture trade-off in R.3/PRD §4 |
| 2026-06-25 | **Fixed clipped speech bubbles** — the NL message bubble (and title) were cut off the figure edge because `tight_layout` squeezed the axes; reserved explicit top/bottom margins (`subplots_adjust`) and dropped `tight_layout`, so each turn's spoken line is fully visible below the board | "I don't see the comments the agents send" — bubbles were rendered but off-frame | `gui/{board_renderer,overlays}.py`; regenerated `assets/*`; 180 tests, 100% cov |
| 2026-06-25 | **Modern-dark GUI redesign** — new `gui/theme.py` (dark palette + `glow()` halo) and `gui/overlays.py` (HUD banner/move-counter/legend + rounded **speech bubble** on the speaker); `board_renderer` now draws a dark board with **glowing cop/thief tokens**, barrier slabs, faded **movement trails**, and a **capture flash** on a cop win (renderer stays stateless; trails + `max_moves` passed in) | "Make the GUI very very beautiful" | `assets/board_state.png`, `match.gif`, `match_nl.gif` (regenerated); 180 tests, 100% cov, Ruff clean |
| 2026-06-25 | **LLM-written, in-character speech** — added a pluggable `Speaker`: `nl_speak.llm_speaker` asks the LLM (persona prompt B5) to voice each move freshly (cop = heroic + implies cell; thief = sly + cryptic), replacing the fixed `nl_encode` templates. Enabled with a real key + `llm.creative_speech`; falls back to templates on empty/error/offline. **Live window now auto-closes** after the game (`gui.close_on_finish` + `final_hold_seconds`) | The bottom-of-screen lines were identical templates (only coords changed) — make them genuinely generative; and the window lingered after the game ended | `nl_protocol/{nl_speak,prompt_templates}.py`; **180 tests, 100% cov**, Ruff clean; ~2× LLM calls (R.7) |
| 2026-06-25 | **Live window no longer freezes** — moved frame production (which blocks on the per-turn LLM call) onto a **daemon worker thread** feeding a `queue.Queue`; the Tk event loop keeps the **main thread** and drains one frame per tick via `fig.canvas.new_timer` (`gui.poll_interval_ms`). Extracted pure `_produce`/`_render_tick` helpers (unit-tested). Config key `gui.turn_delay_seconds` → `gui.poll_interval_ms` | Window showed "not responding" while waiting for the next turn (blocking call on the GUI thread) | `gui/live_viewer.py`; PLAN §4 threading note; docs-first |
| 2026-06-25 | **Live real-time GUI window** — `cop-thief --live` opens an interactive window that draws each turn the instant the engine computes it (so an NL match advances as each LLM call returns). Refactored the game loop into service-layer per-turn *frame streams* (`services/match_stream.py` `stream_subgame`/`heuristic_subgame_stream` + `nl_subgame_stream`); the GIF animator now collects the same stream (DRY); exposed via SDK (`stream_simple_frames`/`stream_nl_frames`); backend config-driven (`gui.live_backend`) | The GIF was a recording, not real-time — user wanted to watch the game live | `gui/live_viewer.py`; **166 tests, 100% cov**, Ruff clean; docs-first (PLAN §4, PRD FR-11, TODO T6.39–48) |
| 2026-06-25 | **GUI now animates the NL match** — `cop-thief --gui` renders the natural-language sub-game with each turn's NL message overlaid (real OpenAI when keyed, else offline); `--simple --gui` keeps the heuristic/smart GIF | One command to *see* the full NL run, not just text | `assets/match_nl.gif`; 154 tests, 100% cov; `peek_last` bus API + `nl_subgame_frames` |
| 2026-06-25 | **Token-cost analysis (R.7)** — `token_cost.py` util + `token_report.py` capture real prompts from an offline match; filled the cost table (config-driven gpt-4o-mini pricing) | Required cost analysis now that OpenAI is wired | **66 calls, 3310 tokens, $0.000615/match**; 149 tests, 100% cov; `results/token_cost.txt` |
| 2026-06-25 | **Phase 4: cornering "smart" cop** — 1-ply look-ahead ranking actions by `(distance, thief escape-options)` after the thief's reply; config-selectable (`strategy.type`); refreshed comparison graphs | Greedy cop fell into limit cycles and let the thief escape (R.3) | **Capture 0.72→1.00** on 5×5; 100% on 3×3–7×7; 144 tests, 100% cov; `smart_cop.py` + `geometry.py`; graphs in `assets/` |
| 2026-06-25 | **Phase 9: full API gatekeeper** — config-driven rate limiting (`rate_limits.json`), FIFO overflow queue with backpressure alert + drain-on-reset, retries with backoff, `concurrent_max` semaphore, thread-safe `RLock`, `get_queue_status()`; injected clock/sleep for deterministic offline tests; **adversarial multi-agent review** then fixed 6 confirmed defects (ticket-leak deadlock, retries bypassing the limiter, prod path not loading `rate_limits.json`, backpressure off-by-one, version validation, drain test) | Required centralized chokepoint (CLAUDE §2); close T9.1–11/45–50 | 134 tests, 100% cov; `shared/{gatekeeper,rate_limit}.py`; demo → [R.9](#r9-api-gatekeeper-rate-limiting--queueing) |
| 2026-06-25 | Made **NL the default** (`cop-thief`; `--simple` for heuristic) + wired a **real OpenAI backend** auto-loaded from `.env` | NL is the assignment; use a real LLM | 111 tests; offline fallback intact |
| 2026-06-25 | Synced `docs/PLAN.md` to the as-built tree; added a **single-command** runner (`cop-thief` console script + `run.ps1`) | Keep docs accurate; simpler UX | `uv run cop-thief` works |
| 2026-06-25 | **Phase 6**: GUI board renderer + match animator (`--gui` → animated GIF) + smoke tests | Visualize the game; required screenshots | 108 tests; `assets/match.gif` |
| 2026-06-25 | Generated **experiment graphs + board screenshots + NL log** from real runs; filled README R.3–R.5 | Report results with evidence | `scripts/make_figures.py`; 5 PNGs in `assets/`, log in `results/` |
| 2026-06-25 | **NL match runnable** (then `--nl`, now the default `cop-thief`) + **Phase 8** report builder (internal + inter-group JSON) and Gmail/Calendar agent tools (read/extract/calendar/send, dependency-injected) | Make NL playable + build the submission report | 106 tests, 100% cov; NL CLI works (workflow-authored) |
| 2026-06-25 | **Phase 5**: NL encode/decode + ambiguity handler + NL decider; **minimal gatekeeper** + LLM client; agents coordinate in free text via the LLM-through-gatekeeper | The graded core: NL coordination under partial obs | 86 tests, 100% cov; NL sub-game runs offline |
| 2026-06-25 | **Phase 2**: MCP tool layer (observation, message bus, tool service w/ turn-ownership) + 2 FastMCP servers exposing 6 tools each | Build the agent communication infra | 72 tests, 100% cov, ruff clean |
| 2026-06-25 | **Phase 3**: orchestrator + turn pipeline + accumulator + SDK + CLI; full autonomous 6-sub-game match runs (heuristic decider) | Wire the end-to-end local match | `uv run python -m marl_cop_thief` works; 55 tests, 100% cov |
| 2026-06-25 | **Phase 1**: game engine — board, models, engine (state machine/legality/capture), scoring, barriers | Build the authoritative rules | 42 tests pass, 100% coverage, ruff clean |
| 2026-06-25 | **Phase 0**: `uv` project, config (versioned), version/constants, config loader | Start the build | 14 tests, 100% cov (commit 3428a02) |
| 2026-06-25 | Ran a 176-agent requirements audit of all MATERIALS vs the repo; closed README/license/Dec-POMDP gaps; added Phase 10 closure tasks | "Did we forget anything?" — found 76+26 gaps | [`docs/AUDIT-2026-06-25.md`](docs/AUDIT-2026-06-25.md) |
| 2026-06-25 | Expanded `docs/TODO.md` to 600+ granular tasks; added `docs/PROMPT_LOG.md` | Lecturer rule (≥550 tasks); prompt log §8.3 | [`docs/TODO.md`](docs/TODO.md), [`docs/PROMPT_LOG.md`](docs/PROMPT_LOG.md) |
| 2026-06-25 | Authored `docs/` suite + integrated Gmail/Calendar agent; created this report section | Docs-first workflow | — |
| 2026-06-24 | Added engineering-standards `CLAUDE.md` + reminder hook | Enforce submission guidelines every session | — |

## R.2 Formal Model (Dec-POMDP)
The game is a Decentralized Partially Observable Markov Decision Process `⟨n, S, {Aᵢ}, P, R, {Oᵢ}, O, γ⟩`:
- **n** = 2 agents (Cop, Thief).
- **S** = grid configuration: cop position, thief position, and the set of barrier cells (on a `W×H` board).
- **{Aᵢ}** = `MOVE(dx,dy)` with `dx,dy ∈ {-1,0,1}` (8-dir), `PLACE_BARRIER` (Cop only), `STAY`.
- **P** = deterministic engine transition (legality + capture), see [`docs/PRD_game_engine.md`](docs/PRD_game_engine.md).
- **R** = scoring table (Cop win 20/5, Thief win 5/10).
- **{Oᵢ}** = each agent's partial local view (within `visibility_radius`) + inbound NL messages.
- **O** = observation function mapping true state → each agent's partial view.
- **γ** = discount factor (used only if the optional Q-learning strategy is enabled).

## R.3 Experiments & Graphs
Generated from **real match runs** by [`scripts/make_figures.py`](scripts/make_figures.py)
(`uv run python scripts/make_figures.py`).

**Match outcomes & move distribution** (5×5, 60 seeds, heuristic):

![Win distribution](assets/win_distribution.png)
![Moves histogram](assets/moves_histogram.png)

**Sensitivity — cop capture rate vs grid size, greedy vs cornering** (40 seeds per size):

![Capture rate vs grid size](assets/winrate_vs_gridsize.png)

The **greedy** cop's capture rate falls from **100% (2×2)** to **~62% (6×6)** — larger boards give the
thief more room to evade, matching the assignment's sanity-check intuition. The **cornering (smart)** cop
(Phase 4) holds **100% at every size**.

**Strategy comparison — cop win rate by strategy** (5×5, 40 seeds):

![Strategy comparison](assets/heuristic_vs_nl.png)

**Finding & fix (Phase 4).** The greedy Chebyshev pursuit falls into a **limit cycle** — the cop
oscillating (2,1)↔(1,2) while the thief mirrors (4,3)↔(3,4) — so the thief survives the 25-move cap
(greedy ≈ 0.72 on 5×5). The **cornering cop** (`strategy.type: "smart"`,
[`smart_cop.py`](src/marl_cop_thief/services/strategy/smart_cop.py)) fixes this with a **one-ply
look-ahead**: it ranks each candidate action by the position it leaves *after the thief's best evasion*,
lexicographically by `(distance, thief escape-options)`. Minimising the thief's escape options herds it
into a corner — where the board edges act as walls and its mobility collapses — lifting capture to
**1.00** on every sampled board. (Barriers only seal the cop's own cell at a tempo cost, so geometric
cornering, not wall-building, is the effective lever here — see
[`docs/PRD_decision_strategy.md`](docs/PRD_decision_strategy.md) §3.1 for the analysis.)

**🐞 Problem & fix — repetitive thief that "always goes left" (Phase 4).** We observed in the GUI that the
thief kept making the *same* move (drifting left) instead of varied, smart moves. **Root cause:** the
greedy thief maximised *only* distance, and because distance ties are common on an open board and
`DIRECTIONS_8` lists the west moves first, Python's `max` always returned the first (left) move — so the
thief hugged one wall. The default thief is now `smart` (`strategy.thief_type`,
[`smart_thief.py`](src/marl_cop_thief/services/strategy/smart_thief.py)): it ranks moves by
`(distance from cop, own mobility, centrality)` so it flees *and* keeps escape room, using the whole
board. As an **honest** consequence, this better evader lowers the cornering cop's capture against it —
**1.00/1.00/0.90/0.88/0.47** on 3×3–7×7 (vs 1.00 against the greedy baseline) — since the cop's look-ahead
still models a greedy thief. The R.3 cop comparison above keeps the greedy thief as the controlled baseline.

### Sensitivity analysis (OAT)
**Methodology:** one-at-a-time (OAT) sweeps — vary a single parameter, hold the rest fixed, average over
many seeds — generated by [`scripts/sensitivity.py`](scripts/sensitivity.py)
(`uv run python scripts/sensitivity.py` → graphs in `assets/`, data in
[`results/sensitivity.txt`](results/sensitivity.txt)). Viz stack: **Matplotlib** (Seaborn/Plotly optional).

**Partial observation matters most** — NL cop capture vs **visibility radius** and **grid size**:

![Capture vs visibility (line)](assets/sensitivity_visibility.png)
![Capture heatmap: grid × visibility](assets/sensitivity_heatmap.png)

- At **radius 0** (effectively blind, messages only) capture collapses to **0.03–0.20** — the cop can't
  reliably localise the thief from free text alone against a smart evader.
- Capture **peaks at radius 1–2** then *declines* (non-monotonic): a wider view doesn't help a *greedy* NL
  cop that still mirrors the evader — echoing the limit-cycle finding (a cornering NL cop is future work).
- Capture **falls as the board grows** (more room to evade), consistent with the grid-size curve above.

**Game length scales with board size** — moves-per-sub-game distribution (box) and board-area correlation
(scatter), smart-vs-smart:

![Moves per sub-game by grid size (box)](assets/moves_boxplot.png)
![Board area vs mean moves (scatter)](assets/scatter_area_moves.png)

Mean moves-to-conclusion rises ~linearly-to-super-linearly with area (2×2≈2 → 7×7≈18 moves); large boards
cluster at the 25-move cap (escapes), matching the capture-rate drop.

## R.4 Screenshots & GUI (Phase 6)
A **modern-dark theme** (`gui/theme.py`): glowing **cop = blue disc**, **thief = amber star**, barrier
slabs, faded **movement trails**, a **capture flash** on a cop win, and a HUD (turn/winner banner, move
counter, legend) — all rendered from engine state only (no game logic in the GUI). Matplotlib can't draw
colour emoji, so agents are distinct glowing tokens rather than emoji glyphs.

Static board (dark theme, glow tokens, HUD):

![Board: dark theme](assets/board_state.png)

**Natural-language match GUI** — `uv run cop-thief --gui` animates an NL sub-game; each turn's spoken line
appears in a **speech bubble** anchored on the speaker (with a real key the line is **LLM-written and
in-character**; offline it falls back to templates), so you watch the agents *talk* as they move
(`assets/match_nl.gif`):

![NL match animation](assets/match_nl.gif)

Heuristic/`smart` sub-game (`uv run cop-thief --simple --gui`, the cop closes in and captures):

![Match animation](assets/match.gif)

### Live real-time window (`--live`)
The GIFs above are *recordings*. For a **live** view, `uv run cop-thief --live` opens an interactive
matplotlib window (backend from `config.gui.live_backend`, default `TkAgg`) that draws **each turn the
instant the engine computes it** — for the NL match the board advances as every LLM call returns, so you
watch the pursuit unfold move-by-move (add `--simple` for the heuristic/smart match). The window stays on
the final board until you close it. Architecture: the game is exposed as a per-turn *frame stream* from
the SDK (`Sdk.stream_nl_frames` / `stream_simple_frames` → `services/match_stream.py`); the live viewer
and the GIF animator are two render-only consumers of the same stream (SDK-only; GUI holds no game logic).
**Responsiveness:** because an NL turn blocks on an LLM call, the frame generator runs on a **daemon
worker thread** that feeds a `queue.Queue`, while the Matplotlib/Tk event loop owns the **main thread** and
drains one frame per tick via `fig.canvas.new_timer` (`gui.poll_interval_ms`, default 150 ms) — so the
window never goes "not responding" while a turn computes.

#### 🐞 Fault report — live window froze while waiting for a turn
**Symptom (first `--live` build):** clicking the window while it waited for the next turn showed Windows'
**"(Not Responding)"** state. **Root cause:** frames were produced *on the GUI thread*, and producing an NL
frame blocks on the per-turn LLM call, so the Tk event loop stalled for the duration of the call.
**Fix:** moved turn computation to a daemon **worker thread** + `queue.Queue`, leaving the event loop free
on the main thread (timer-drained) — the responsiveness design above. Captured before the fix:

![Live window "Not Responding" before the threading fix](assets/realtime_GUI_not_handled_correctly.png)

## R.5 CLI Logs & MCP Communication
A natural-language sub-game (full log: [`results/nl_match_sample.txt`](results/nl_match_sample.txt)) —
the thief **bluffs**, the cop **reveals its cell**, and the LLM (via the gatekeeper) interprets messages:

```text
move  1 | thief none      cop=(4,3) thief=(2,0) | thief: Slipping away to the north-west — you'll never find me.
move  2 | cop   none      cop=(3,2) thief=(2,0) | cop:   I'm at 4,3 pushing north-west to close in.
move  7 | thief none      cop=(1,1) thief=(0,1) | thief: Slipping away to the south — you'll never find me.
move  8 | cop   capture   cop=(0,1) thief=(0,1) | cop:   I'm at 1,1 pushing west to close in.
RESULT: cop wins in 8 moves; LLM calls via gatekeeper=7
```

## R.6 Communication-Challenge Analysis
The graded core is **coordination in free text with no fixed protocol**, under partial observation
(Dec-POMDP). Each turn the acting agent speaks a natural-language `Message`; the opponent reads it off the
MCP bus, has the **LLM (via the gatekeeper) interpret** it into a belief about where the other agent is,
and acts. Design: [`docs/PRD_nl_communication.md`](docs/PRD_nl_communication.md). Four challenges and how
the implementation meets each:

- **Ambiguity.** Free text is unstructured, so we *constrain the interpretation, not the speech*:
  `interpret_prompt` asks the LLM to answer **only** `x,y` or `unknown`, and
  [`ambiguity_handler.parse_position`](src/marl_cop_thief/services/nl_protocol/nl_decode.py) parses it
  **defensively** — anything unparseable, out-of-bounds, or an LLM/transport error falls back to the
  **prior belief** and a safe action. Result: every inbound message yields a valid belief update with
  **zero crashes** (PRD S2; covered by tests).
- **Deception.** The thief deliberately **bluffs** — its encoder emits vague/misleading lines (e.g.
  *"Slipping away to the west — you'll never find me"*), while the cop **reveals its own cell** to apply
  pressure (R.5 log). The cop never lets talk override facts: belief precedence is **direct observation →
  message interpretation → prior**, so whenever the opponent is within the visibility radius, observation
  *overrides* any message (PRD S3). Messages only fill the gap when the opponent is unseen.
- **No shared protocol.** There is no agreed coordinate schema between the two agents; the **LLM is the
  bridge** that maps arbitrary free text to a structured guess, and each side **validates** that guess
  (bounds-checks it) before trusting it. Coordination thus *emerges* from NL + interpretation rather than
  a rigid wire format — exactly the assignment's intent (a JSON coordinate protocol was rejected, PRD §7).
- **Mutual understanding.** A minimal **prompt contract** keeps meaning aligned with no prior agreement:
  `interpret_prompt` fixes the reply shape (`x,y`/`unknown`) the decoder depends on. (`system_prompt` is a
  versioned role/goal template in `prompt_templates.py`; in the current backend only the user
  `interpret_prompt` is sent to the model — wiring the system prompt into the call is a noted enhancement.)
  The asymmetry — cop transparent, thief evasive — directly reflects their opposed incentives.

**Cost & limitation.** With deterministic speech, interpretation is the only LLM call (~66/match, R.7).
Enabling **creative speech** (`llm.creative_speech`, real key) adds one LLM *generation* call per turn so
each line is written fresh in-character — this roughly **doubles** the call count and token cost (the
spoken line still implies the cop's cell / hides the thief's, so interpretation keeps working; on
empty/error it falls back to the template). Belief is a single most-likely cell rather than a full
posterior; a Bayesian filter is noted as optional enrichment (PRD §7). The offline backend exercises the
same pipeline deterministically (echo → the cop recovers any revealed cell), so the mechanics are testable
without a network.

## R.7 Token-Cost Analysis
Per **full match** (6 sub-games, 5×5), measured by [`scripts/token_report.py`](scripts/token_report.py)
(`uv run python scripts/token_report.py` → [`results/token_cost.txt`](results/token_cost.txt)). The LLM
is consulted **once per turn** for `interpret_prompt` (parsing the opponent's message); with the default
deterministic speech the agent's own line costs no tokens. **Enabling creative speech**
(`llm.creative_speech`, real key) adds a second `speak_prompt` call per turn, roughly **doubling** the
figures below (a real keyed `--live` sub-game measured ~60 calls vs ~28 interpret-only). Counts below are
the default mode — an **offline estimate** (~4 chars/token, the
OpenAI rule of thumb — no tokenizer download); prices are gpt-4o-mini **list price**, config-driven in
`config.json → llm.pricing`. Exact billing should be read from the API `usage` field on a keyed run.

| Model | Input tokens | Output tokens | $/1M in | $/1M out | Total cost / match |
|---|---|---|---|---|---|
| gpt-4o-mini | 3046 | 264 | 0.15 | 0.60 | **$0.000615** |

- **66 interpret calls/match** · ~46 input + 4 output tokens each · **3310 tokens/match**.
- **Forecast:** ≈ **$0.62 per 1000 matches** — cost scales linearly with calls × tokens/call.
- **Optimization strategies:** (1) the decider already **skips the LLM** when its own observation reveals
  the opponent (sets belief directly — fewer calls on close range); (2) prompts are kept terse and the
  reply is constrained to `x,y`/`unknown` (≈4 output tokens); (3) a larger model would be ~30× costlier,
  so gpt-4o-mini is the right default for this short, structured task.

**Budget management** (implemented, config-driven — [`shared/budget.py`](src/marl_cop_thief/shared/budget.py),
closes audit C14/C20). A `BudgetTracker` reads the gatekeeper's **live call count** and a config-driven
`llm.budget.usd_per_call` to give a **real-time spend counter** (`spent_usd`/`remaining_usd`), a
**forecast** (`forecast_usd(projected_calls)` = cost/call × projected calls), and a two-stage **overrun
alert**: `alert` at `alert_threshold` (default 0.8) of `monthly_cap_usd`, and `over_budget` past the cap.
A real `uv run cop-thief` prints, e.g., `Budget: $0.0012 spent / $5.00 cap ($4.9988 left)` with an
`[ALERT]`/`[OVER BUDGET]` flag. Rate limits in `rate_limits.json` independently cap call volume (and thus
spend) per minute/hour. (Cap `0` disables monitoring.)

## R.8 Prompt-Engineering Log
Maintained in [`docs/PROMPT_LOG.md`](docs/PROMPT_LOG.md) — development prompts + runtime agent prompt
templates, with context/goal, example outputs, and improvements (guidelines §8.3).

## R.9 API Gatekeeper (rate limiting & queueing)
Every external call (the LLM today; Gmail/Calendar when OAuth is wired) routes through one
[`ApiGatekeeper`](src/marl_cop_thief/shared/gatekeeper.py) (CLAUDE.md §2). It enforces **config-driven**
limits from [`config/rate_limits.json`](config/rate_limits.json), **queues** overflow in FIFO order
(never rejecting), **drains** the queue when the window resets, **retries** transient failures with
backoff, bounds **concurrency** with a semaphore, and exposes `get_queue_status()` with a
**backpressure** alert. Time is injected (`clock`/`sleep`) so the behaviour is tested **offline and
deterministically** — no real waiting. Design: [`docs/PRD_gatekeeper.md`](docs/PRD_gatekeeper.md).

Reproduce: `uv run python scripts/gatekeeper_demo.py` (full log:
[`results/gatekeeper_demo.txt`](results/gatekeeper_demo.txt)). Under a **3 calls/min** cap, 9 calls are
admitted 3-per-minute — none rejected — and a queue of 5 behind a `max_queue_depth` of 3 raises
backpressure:

![Gatekeeper throughput under a 3/min limit](assets/gatekeeper_throughput.png)

```text
Rate limiting + FIFO drain: 9 calls under a 3/min cap (no rejections):
  call 1: t=0.0 min   call 2: t=0.0 min   call 3: t=0.0 min
  call 4: t=1.0 min   call 5: t=1.0 min   call 6: t=1.0 min
  call 7: t=2.0 min   call 8: t=2.0 min   call 9: t=2.0 min
Backpressure: 5 callers queued behind a max_queue_depth of 3:
  QueueStatus(depth=5, max_depth=3, backpressure=True, enqueued=5, drained=0, peak_depth=5)
```

Thread-safety is a single `RLock` (consistent acquisition order ⇒ no deadlock) with `with`-managed
critical sections; gatekept calls are **I/O-bound**, so concurrency uses threads, not multiprocessing
(PRD_gatekeeper §6.1). For local offline runs the default gatekeeper is **unlimited** so the match stays
snappy; when `OPENAI_API_KEY` is set the CLI auto-selects a config-driven gatekeeper
(`select_gatekeeper` → `gatekeeper_from_config(rate_limits.json, "llm")`), so editing `rate_limits.json`
changes real-run throttling with **no code edit** (version-checked on load).

## R.10 ISO/IEC 25010 Quality Self-Assessment
Mapping each of the eight product-quality characteristics to concrete evidence in this project.

| # | Characteristic | How it is addressed (evidence) |
|---|---|---|
| 1 | **Functional suitability** | All FRs implemented (engine, dual MCP tools, NL coordination, scoring, reporting); 189 tests assert correctness incl. edge cases (`docs/EDGE_CASES.md`). |
| 2 | **Performance efficiency** | O(grid) move selection; gatekeeper bounds external-call rate/concurrency; token-cost analysis (R.7). I/O-bound work uses threads, not processes (R.9). |
| 3 | **Compatibility** | Pure-Python, OS-agnostic (`uv`); SDK-only core decoupled from CLI/GUI; MCP standard for agent interop. |
| 4 | **Usability** | One-command run; clear CLI banners + colored GUI HUD/legend; documented config & workflow (R.11, §2–§3). |
| 5 | **Reliability** | Defensive NL parsing (never crashes on ambiguity); gatekeeper retries + FIFO queue (never rejects); deterministic seeds; 100% branch coverage. |
| 6 | **Security** | No secrets in code (`.env`/`.env-example`, git-ignored creds); token-based Google/MCP auth; gatekeeper as single audited choke-point. |
| 7 | **Maintainability** | ≤150-line files, SDK layering, DRY, Ruff-clean, docs-first PRD/PLAN/TODO, ≥85% coverage gate, per-feature commits. |
| 8 | **Portability** | `uv`-managed deps + lockfile; config-driven (no hard-coded paths/values); local→cloud deployment path (PLAN §3). |

## R.11 Usability (UI/UX) — Nielsen's Heuristics & Accessibility
The CLI/GUI is assessed against **Nielsen's 10 usability heuristics** (a required standard):

| # | Heuristic | In this project |
|---|---|---|
| 1 | Visibility of system status | GUI HUD shows move count, whose turn, winner banner; CLI prints backend + gatekeeper call count |
| 2 | Match to the real world | Cop/thief metaphor; plain-language NL messages; compass words (north-east…) |
| 3 | User control & freedom | Run modes/flags (`--simple/--gui/--live`); window closes on demand or auto-closes; Ctrl-C safe (gatekeeper releases tickets) |
| 4 | Consistency & standards | One config schema; consistent colors (cop=blue, thief=amber) across PNG/GIF/live; standard `uv`/pytest tooling |
| 5 | Error prevention | Config version-checked on load; illegal moves fall back to STAY; unknown strategy rejected with a clear message |
| 6 | Recognition over recall | On-screen legend + labels; documented config table (§5); no hidden commands |
| 7 | Flexibility & efficiency | One-command default plus power flags; config-tunable grid/strategy/pacing without code edits |
| 8 | Aesthetic & minimalist design | Modern-dark theme, uncluttered board, single speech bubble per turn |
| 9 | Help users recover from errors | Troubleshooting table (§2.5); token re-consent path; clear exceptions |
| 10 | Help & documentation | Scientific README + `docs/` suite + `--help` |

**Accessibility:** high-contrast dark palette; cop/thief differ by **shape *and* color** (disc vs star) so
they're distinguishable without color vision; legible sans-serif HUD. *Planned:* a color-blind-safe
palette toggle and keyboard navigation for a future live window.

**Standards alignment:** **ISO/IEC 25010** (R.10), **MIT SQA** practices (docs-first, TDD, reviews),
**Google/Microsoft API** design guidance (SDK facade, gatekeeper, versioned config), and **Nielsen's 10
heuristics** (above) — see also [`docs/PLAN.md`](docs/PLAN.md) and `docs/PRD.md` §4.

---

## 5. Configuration Guide
All tunables live in `config/` (nothing hard-coded). Full schema in [`docs/PLAN.md`](docs/PLAN.md) §5.1.

| Key | Type | Default | Effect |
|---|---|---|---|
| `grid_size` | `[W,H]` | `[5,5]` | Board size (generic, supports non-square e.g. `[3,2]`) |
| `max_moves` | int | `25` | Max moves per sub-game |
| `num_games` | int | `6` | Sub-games per match |
| `max_barriers` | int | `5` | Cop barrier budget per game |
| `visibility_radius` | int | `1` | Partial-observation radius |
| `seed` | int | `42` | RNG seed for deterministic match/figure runs |
| `scoring.*` | int | `20/10/5/5` | cop_win / thief_win / cop_loss / thief_loss |
| `strategy.type` | str | `heuristic` | Cop policy: `heuristic` (greedy) or `smart` (cornering, ~100% capture vs greedy thief) |
| `strategy.thief_type` | str | `smart` | Thief policy: `smart` (flee + keep escape room, roams the board) or `greedy` (distance-only baseline) |
| `gui.live_backend` / `gui.poll_interval_ms` | str / int | `TkAgg` / `150` | Live window (`--live`): interactive matplotlib backend + how often (ms) the GUI drains the frame queue while turns compute on a worker thread |
| `llm.model` | str | `gpt-4o-mini` | OpenAI model for the NL match (used when `OPENAI_API_KEY` is set) |
| `llm.pricing.*` | obj | `0.15/0.60` | `$/1M` input & output, `chars_per_token`, `est_output_tokens_per_call` (token-cost report, R.7) |
| `llm.budget.*` | obj | `5.0/0.8/2e-5` | `monthly_cap_usd` / `alert_threshold` / `usd_per_call` — real-time spend counter + overrun alert (R.7; cap `0` disables) |
| `reporting.recipient_email` | str | `sharbelma3@gmail.com` | Report recipient (→ `rmisegal+uoh26b@gmail.com` at submission) |
| `reporting.timezone` | str | `Asia/Jerusalem` | Timezone stamped into the JSON match report (read by `services/reporting.py`) |
| `google.secrets_dir` | path | _external_ | Folder (outside repo) holding `client_secret.json`/`token.json` |
| `google.scopes` | list | gmail.modify, calendar | OAuth scopes |
| `rate_limits.services.*` | obj | see file | Per-service `requests_per_minute`/`requests_per_hour`/`concurrent_max`/`retry_after_seconds`/`max_retries`/`max_queue_depth` (gatekeeper; `0` = unlimited) |

## 6. Contribution Guidelines
Follow [`CLAUDE.md`](CLAUDE.md) and the submission guidelines: docs-first, SDK-only, files ≤150 lines,
TDD ≥85% coverage, Ruff clean, `uv` only, no hardcoded values/secrets, **and report your work here**.
Develop each feature on its own branch off `main` and merge via **Pull Request** with review.

## 7. License & Credits
Licensed under the **MIT License** — see [`LICENSE`](LICENSE).
Assignment, guidelines, and Google-setup materials © **Dr. Yoram Segal** (see [`MATERIALS/`](MATERIALS/)).
Third-party libraries (attribution finalized as deps are pinned): **FastMCP**, **google-api-python-client**,
**google-auth-oauthlib**, **google-auth-httplib2**, the chosen **LLM SDK**, **Ruff**, **pytest**.
