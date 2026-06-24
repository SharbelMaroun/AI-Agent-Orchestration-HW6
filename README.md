# Dual AI Agent Race via MCP Servers — "Cop & Thief"

> Course: **Orchestration of AI Agents**, University of Haifa — Task 6 (ex06).
> This README is the project's **user manual** *and* its **living scientific report**.
> Engineering standards: [`MATERIALS/software_submission_guidelines-V3_Summary.md`](MATERIALS/software_submission_guidelines-V3_Summary.md).
> Design docs: [`docs/`](docs/) ([PRD](docs/PRD.md) · [PLAN](docs/PLAN.md) · [TODO](docs/TODO.md)).

**Status:** 🟦 In progress — documentation phase. _(Update this badge as milestones land.)_

---

## 1. Overview
Two autonomous AI agents — a **Cop** and a **Thief** — play a pursuit game on a 2-D grid. Each agent is
backed by its **own MCP server (FastMCP)** and they coordinate in **natural language** under
**partial observation**. A full match is **6 sub-games** (≤25 moves each), run end-to-end with no
manual intervention. The project also ships a **Gmail & Calendar agent** (read inbox → extract a
meeting invite → add a Calendar event → send email); when the match ends, it emails the JSON result.

See [`docs/PRD.md`](docs/PRD.md) for full requirements.

## 2. Installation
> _TBD — filled during Phase 0._
```bash
# uv is the only package manager/runner (no pip/venv)
uv sync
```

## 3. Usage
> _TBD — filled as the SDK/CLI/GUI land._
```bash
uv run python -m marl_cop_thief        # run a full local match
```
Configuration lives in `config/config.json` (grid size, moves, scoring, report recipient, Google scopes).
The report recipient is **config-driven** (`reporting.recipient_email`): dev `sharbelma3@gmail.com`,
submission `rmisegal+uoh26b@gmail.com` (kept verbatim).

## 4. Architecture
Summary in [`docs/PLAN.md`](docs/PLAN.md) (C4 model, ADRs, module layout). Diagrams go in `assets/`.

---

# 📊 Project Report / Results

> **Reporting rule:** we report **everything we do** here as we go — every feature, experiment, and
> decision — with **graphs and screenshots whenever possible**. Images live in `assets/`, generated
> plots and run outputs in `results/`. This section is updated continuously, not only at submission.

## R.1 Work Log (running changelog)
Newest first. One row per meaningful change.

| Date | What we did | Why | Evidence (graph/screenshot/log) |
|------|-------------|-----|----------------------------------|
| 2026-06-25 | Authored `docs/` suite + integrated Gmail/Calendar agent; created this README report section | Docs-first workflow; capture reporting requirement | — (documentation) |
| 2026-06-24 | Added engineering-standards `CLAUDE.md` + reminder hook | Enforce submission guidelines every session | — |
| _…_ | _…_ | _…_ | _…_ |

## R.2 Formal Model (Dec-POMDP)
> _TBD._ Present the game as a Dec-POMDP `⟨n, S, {Aᵢ}, P, R, {Oᵢ}, O, γ⟩`; define the tuple,
> state space, and observations. (Required scientific section.)

## R.3 Experiments & Graphs
> _TBD._ Parameter/sensitivity research (grid size sweeps 2×2→5×5, visibility radius, hyper-params),
> learning curves (if Q-table). Embed plots from `results/`:
>
> `![Learning curve](assets/learning_curve.png)` · `![Sensitivity heatmap](assets/sensitivity.png)`

## R.4 Screenshots (GUI & states)
> _TBD._ Real-time GUI of agents + barriers, key game states.
>
> `![GUI – mid game](assets/gui_midgame.png)`

## R.5 CLI Logs & MCP Communication
> _TBD._ Logs proving valid (cloud) MCP communication and natural-language exchange between agents.

## R.6 Communication-Challenge Analysis
> _TBD._ Handling ambiguity, deception, and mutual understanding without a fixed protocol
> (see [`docs/PRD_nl_communication.md`](docs/PRD_nl_communication.md)).

## R.7 Token-Cost Analysis
> _TBD._ Input/output token counts, cost per model, totals, optimization strategies.

## R.8 Prompt-Engineering Log
> _TBD._ Significant prompts, context/goal, example outputs, and improvements made.

---

## 5. Configuration Guide
> _TBD._ Explain `config/config.json` and `config/rate_limits.json` keys and effects.

## 6. Contribution Guidelines
Follow [`CLAUDE.md`](CLAUDE.md) and the submission guidelines: docs-first, SDK-only, files ≤150 lines,
TDD ≥85% coverage, Ruff clean, `uv` only, no hardcoded values/secrets, **and report your work here**.

## 7. License & Credits
> _TBD._ License and third-party attributions. Source assignment & guides by **Dr. Yoram Segal**
> (see [`MATERIALS/`](MATERIALS/)).
