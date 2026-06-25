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
2. Set your LLM key in `.env` (e.g. `ANTHROPIC_API_KEY=...`).
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

### 3.1 Run modes _(planned CLI)_
| Command | Mode |
|---|---|
| `uv run python -m marl_cop_thief` | Full local match (6 sub-games) |
| `uv run python -m marl_cop_thief --subgame` | Single sub-game |
| `uv run python -m marl_cop_thief --gui` | Real-time GUI |
| `uv run python -m marl_cop_thief --headless` | CLI-log mode (no GUI) |
| `--strategy heuristic\|q_table` · `--grid 5x5` · `--seed 42` · `--config path` | Common flags |

### 3.2 Typical workflow
Edit `config/config.json` → `uv run python -m marl_cop_thief` → watch the GUI play 6 sub-games →
read the CLI logs of the natural-language MCP exchange → receive the JSON report email.

### 3.3 Worked example _(planned output shape)_
```text
$ uv run python -m marl_cop_thief --seed 42
[sub-game 1] thief: "I'm hugging the north wall, heading east." cop: "Cutting you off at (3,1)."
... CAPTURE at move 14 → cop_win
[match] totals: cop=..., thief=...  → JSON report emailed to <reporting.recipient_email>
```

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
| 4 | Decision strategy | 🟦 minimal | heuristic decider only; belief/Q-table pending |
| 5 | Natural-language + LLM | ✅ done | NL encode/decode, ambiguity handler, NL decider; LLM via gatekeeper |
| 8 | Report builder + Gmail/Calendar agent | 🟦 partial | JSON builders + read/extract/calendar/send tools tested; real OAuth send pending |
| 9 | API gatekeeper | 🟦 minimal | retry + per-call logging; FIFO queue/backpressure pending |
| 6, 7, 10 | GUI, cloud, research | ⬜ pending | — |

Whole suite: **106 tests, 100% coverage, Ruff zero-violation.** The NL match is runnable via
`uv run python -m marl_cop_thief --nl`. The Gmail/Calendar tools are dependency-injected (tested with
fakes); `shared/google_auth.py` builds the real services and needs your Google OAuth `client_secret.json`.

## R.1 Work Log (running changelog)
Newest first.

| Date | What we did | Why | Evidence |
|------|-------------|-----|----------|
| 2026-06-25 | **NL match runnable** (`--nl`) + **Phase 8** report builder (internal + inter-group JSON) and Gmail/Calendar agent tools (read/extract/calendar/send, dependency-injected) | Make NL playable + build the submission report | 106 tests, 100% cov; `--nl` CLI works (workflow-authored) |
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
> _TBD._ Sensitivity analysis (OAT sweeps over `grid_size`, `visibility_radius`, `α`, `γ`), learning
> curves. Plots → `results/` / `assets/` with clear labels, legend, accessible colors, captions, ≥150 dpi.

## R.4 Screenshots (GUI & states)  ·  ## R.5 CLI Logs & MCP Communication
> _TBD._ GUI of agents+barriers and key states; CLI logs proving valid (cloud) MCP NL exchange.

## R.6 Communication-Challenge Analysis
> _TBD._ Ambiguity/deception/mutual-understanding without a fixed protocol (see [`docs/PRD_nl_communication.md`](docs/PRD_nl_communication.md)).

## R.7 Token-Cost Analysis
| Model | Input tokens | Output tokens | $/1M in | $/1M out | Total cost |
|---|---|---|---|---|---|
| _TBD_ | | | | | |
> Plus budget management: forecast (cost/token × projected calls/match), real-time spend counter in the
> gatekeeper, and an overrun alert at a config-driven threshold.

## R.8 Prompt-Engineering Log
Maintained in [`docs/PROMPT_LOG.md`](docs/PROMPT_LOG.md) — development prompts + runtime agent prompt
templates, with context/goal, example outputs, and improvements (guidelines §8.3).

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
| `scoring.*` | int | `20/10/5/5` | cop_win / thief_win / cop_loss / thief_loss |
| `reporting.recipient_email` | str | `sharbelma3@gmail.com` | Report recipient (→ `rmisegal+uoh26b@gmail.com` at submission) |
| `google.secrets_dir` | path | _external_ | Folder (outside repo) holding `client_secret.json`/`token.json` |
| `google.scopes` | list | gmail.modify, calendar | OAuth scopes |
| `rate_limits.services.*` | obj | see file | Per-service RPM/RPH/concurrency/retries (gatekeeper) |

## 6. Contribution Guidelines
Follow [`CLAUDE.md`](CLAUDE.md) and the submission guidelines: docs-first, SDK-only, files ≤150 lines,
TDD ≥85% coverage, Ruff clean, `uv` only, no hardcoded values/secrets, **and report your work here**.
Develop each feature on its own branch off `main` and merge via **Pull Request** with review.

## 7. License & Credits
Licensed under the **MIT License** — see [`LICENSE`](LICENSE).
Assignment, guidelines, and Google-setup materials © **Dr. Yoram Segal** (see [`MATERIALS/`](MATERIALS/)).
Third-party libraries (attribution finalized as deps are pinned): **FastMCP**, **google-api-python-client**,
**google-auth-oauthlib**, **google-auth-httplib2**, the chosen **LLM SDK**, **Ruff**, **pytest**.
