# CLAUDE.md — Project Engineering Standards (HW6)

## ⛔ PRIME DIRECTIVE
**All work in this repository MUST comply with the engineering standards in
[`MATERIALS/software_submission_guidelines-V3_Summary.md`](MATERIALS/software_submission_guidelines-V3_Summary.md)**
(Dr. Yoram Segal — "Guidelines for Writing Professional Software at the Highest Level of Excellence", v3.00).

Before writing or changing code, re-read that file when in doubt. The rules below are the
enforced summary; the source document is authoritative. If a request conflicts with these
standards, flag it and propose a compliant alternative rather than silently violating them.

The assignment being built is defined in
[`MATERIALS/ex06-Dual AI agent race via MCP servers_Summary.md`](MATERIALS/ex06-Dual%20AI%20agent%20race%20via%20MCP%20servers_Summary.md)
(Cop vs. Thief pursuit game over dual MCP servers). The project also includes a **Gmail & Calendar
agent** (read inbox → extract meeting → add Calendar event → send email), described in
[`MATERIALS/Gmail_calendar_agent_guide.md`](MATERIALS/Gmail_calendar_agent_guide.md); the Google
OAuth/token setup is in
[`MATERIALS/main-google-api-installtion-guid_Summary.md`](MATERIALS/main-google-api-installtion-guid_Summary.md).
The report recipient is **config-driven** (`reporting.recipient_email`): dev `sharbelma3@gmail.com`,
submission `rmisegal+uoh26b@gmail.com` (kept verbatim). Google secrets live **outside the repo**.

---

## 1. Docs-first workflow (MANDATORY, before any code)
1. `docs/PRD.md` — Product Requirements (problem, goals/KPIs, functional + non-functional reqs, scope).
2. `docs/PLAN.md` — Architecture & design (C4 diagrams, ADRs, API/data contracts).
3. `docs/TODO.md` — Tasks with priority, status, Definition of Done.
4. `docs/PRD_<mechanism>.md` — A dedicated PRD per algorithm/central mechanism
   (e.g. `PRD_mcp_server.md`, `PRD_nl_communication.md`, `PRD_gatekeeper.md`).
5. Get documents approved → develop, keeping `TODO.md` updated → save results & update `README.md`.

## 2. Architecture
- **SDK-only**: every business function is exposed through a single SDK entry point. GUI/CLI/3rd-party
  layers contain **no business logic** — they delegate to the SDK.
- Layering: `External Consumers → SDK → Domain Services → Infrastructure`.
- **OOP / DRY**: no code duplication. Same logic in 2+ files → shared module/base class/mixin.
  Mixins: one concern each, independently testable, no method overrides between them.
- **API Gatekeeper**: ALL external API calls (LLM, Gmail, MCP) route through one centralized
  gatekeeper that enforces rate limiting, FIFO queueing on overflow (never reject/crash),
  retries, and logging. Rate limits come from config, never hardcoded.

## 3. Code structure & quality
- **Max 150 lines per code file** (blank/comment lines excluded). Over the limit → split
  (extract helpers/mixins/constants/models); never compress to fit.
- Docstrings on every module/class/function. Comments explain **why**, not what.
- Descriptive names, single-responsibility functions.

## 4. Testing & quality (TDD)
- Red → Green → Refactor. Tests written before/with code, never after.
- **Minimum 85% coverage**; suite fails below threshold (`fail_under = 85`).
- Every module has a test file; every public function ≥1 test; cover happy path + error cases.
- Mock external deps (DB, files, API). `conftest.py` for shared fixtures. Test files ≤150 lines.
- **Ruff: zero violations.** `line-length = 100`, `select = ["E","F","W","I","N","UP","B","C4","SIM"]`.

## 5. Configuration & security
- **No hardcoded values.** All config (URLs, rate limits, timeouts, game params like
  `grid_size`, `max_moves`, `num_games`, `max_barriers`, scoring) lives in `config/*.json`.
- **No secrets in code.** Use `os.environ.get(...)`. Commit `.env-example` with dummy values;
  `.env` is git-ignored. `.gitignore` must include `.env`, `*.key`, `*.pem`, `credentials.json`,
  `token.json`.
- Versioning starts at **1.00** (`src/<pkg>/shared/version.py`, plus `"version"` keys in JSON
  config); runtime validates config version.

## 6. Tooling — `uv` ONLY
- Forbidden: `pip`, `virtualenv`, `venv`, `python -m pip`, `requirements.txt`.
- Use: `uv sync`, `uv add <pkg>`, `uv run python ...`, `uv run pytest tests/`, `uv lock`.
- `pyproject.toml` is the single source of truth for deps; commit `uv.lock`.

## 7. Recommended project layout
```
docs/        PRD.md PLAN.md TODO.md PRD_<mechanism>.md
config/      config.json (or setup.json) rate_limits.json
src/<pkg>/   sdk/  services/  shared/(gatekeeper.py config.py version.py constants.py)  main.py
tests/       unit/  integration/  conftest.py
data/  results/  assets/  notebooks/
README.md  pyproject.toml  uv.lock  .env-example  .gitignore
```

## 8b. Reporting & evidence (REPORT EVERYTHING WE DO)
The root **[`README.md`](README.md)** is the project's **living scientific report**, not just a manual.
- **Document every change/feature/experiment/decision there as we go** — in the **`📊 Project Report /
  Results`** section (work-log table + subsections), not only at submission time.
- Include **graphs** (results, learning curves, sensitivity analysis) and **screenshots** (GUI states,
  CLI logs, MCP communication) **whenever possible**. Store images in `assets/`, generated plots & run
  outputs in `results/`, and embed them with markdown image links.
- Keep the required scientific sections current: Dec-POMDP formalization, communication-challenge
  analysis, token-cost analysis, and a **prompt-engineering log** (guidelines §8.3, §9, §11).
- After completing a task, add a **Work Log** row (date · what · why · evidence) before moving on.

## 8. Also expected at submission
- Scientific `README.md` (for ex06: Dec-POMDP formalization, communication-challenge analysis,
  GUI screenshots, CLI logs, learning curves if Q-table used).
- Prompt-engineering log, token-cost analysis, parameter/sensitivity research + visualizations.
- Clean Git history, package `__init__.py` with `__all__`/`__version__`, relative imports only,
  ISO/IEC 25010 alignment.

> A `UserPromptSubmit` hook in `.claude/settings.json` re-injects a short version of this
> directive every turn so the standards stay in context.
