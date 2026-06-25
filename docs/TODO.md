# TODO — Task Tracking (Granular)

**Project:** Dual AI Agent Race via MCP Servers — "Cop & Thief"  
**Document version:** 2.00  
**Governing standard:** [`../MATERIALS/software_submission_guidelines-V3_Summary.md`](../MATERIALS/software_submission_guidelines-V3_Summary.md)

> **Lecturer requirement:** this task list is maintained at fine granularity — **665 tasks** (≥550).  
> **Status:** ⬜ Not Started · 🟦 In Progress · ✅ Completed — **Priority:** P0–P3. Owner: `<TBD>`.  
> Update statuses continuously; add a README Work-Log row + evidence (graph/screenshot) per task.

> **Implementation status (code, 2026-06-25):** Phase 0 ✅ · Phase 1 ✅ · Phase 2 🟦 (tool layer + 2 FastMCP servers done; MCP transport/auth pending) · Phase 3 ✅ · Phase 5 ✅ (NL agents; the default `cop-thief` run) · Phase 6 🟦 (GUI renderer + **NL match animation with message overlay** via --gui; --simple --gui for heuristic/smart) · Phase 8 🟦 (report builder + Gmail/Calendar agent tools done; real OAuth send pending) · Phase 4 ✅ (greedy + **cornering "smart" cop**, config-selectable, 100% capture on 3×3–7×7) · Phase 9 🟦 (**full API gatekeeper done** — config-driven rate limiting + FIFO queue + backpressure + drain + retries/backoff + concurrency + `get_queue_status`; research/submission tasks pending) — all green (ruff clean, pytest 154 passing, 100% coverage). Phases 7/10 mostly pending.

---

## Phase & milestone overview

| Phase | Title | Milestone | Tasks |
|---|---|---|---|
| 0 | Project setup, tooling & documentation | M0 | 36 |
| 1 | Game logic & rules engine | M1 | 68 |
| 2 | MCP communication infrastructure | M2 | 63 |
| 3 | Orchestrator & full local match | M3 | 60 |
| 4 | Decision strategy | M4 | 70 |
| 5 | Natural-language integration | M5 | 60 |
| 6 | GUI & CLI | M6 | 52 |
| 7 | Cloud deployment & security | M7 | 27 |
| 8 | Gmail/Calendar agent & reporting | M8 | 104 |
| 9 | Gatekeeper, quality gates, research & submission | M9 | 85 |
| 10 | Audit closure (requirements coverage gaps) | M10 | 54 |
| — | **Total** | — | **679** |

---

## Phase 0 — Project setup, tooling & documentation (Milestone: M0)
_Foundations: uv project, package skeleton, config, quality tooling, docs approval._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T0.1 | Install `uv` (Windows PowerShell / macOS / Linux) | P0 | ✅ | `<TBD>` | `uv --version` works |
| T0.2 | `uv init` the project | P0 | ✅ | `<TBD>` | Project initialized |
| T0.3 | Author `pyproject.toml` (name, version 0.1.0, requires-python >=3.10) | P0 | ✅ | `<TBD>` | Valid pyproject |
| T0.4 | Declare deps (fastmcp, google-api-python-client, google-auth-oauthlib, google-auth-httplib2, llm sdk) | P0 | ⬜ | `<TBD>` | `uv sync` resolves |
| T0.5 | Generate & commit `uv.lock` | P0 | ✅ | `<TBD>` | Lockfile under VCS |
| T0.6 | Create `src/marl_cop_thief/` package | P0 | ✅ | `<TBD>` | Importable package |
| T0.7 | Add `__init__.py` with `__all__` + `__version__` | P0 | ✅ | `<TBD>` | Exports defined |
| T0.8 | Create `shared/version.py` = `1.00` | P0 | ✅ | `<TBD>` | Version constant present |
| T0.9 | Create `shared/constants.py` (enums, no magic numbers) | P0 | ✅ | `<TBD>` | Constants centralized |
| T0.10 | Create `config/` directory | P0 | ✅ | `<TBD>` | Exists |
| T0.11 | Author `config/config.json` (game + reporting + google) version 1.00 | P0 | ✅ | `<TBD>` | Loads at runtime |
| T0.12 | Author `config/rate_limits.json` version 1.00 | P0 | ✅ | `<TBD>` | Loads at runtime |
| T0.13 | Author `config/logging_config.json` | P0 | ✅ | `<TBD>` | Logging configured |
| T0.14 | Add `.gitignore` (.env, client_secret.json, token.json, *.key, *.pem) | P0 | ✅ | `<TBD>` | Secrets ignored |
| T0.15 | Add `.env-example` with dummy values | P0 | ✅ | `<TBD>` | Committed; no real secrets |
| T0.16 | Configure Ruff in pyproject (line-length 100; E,F,W,I,N,UP,B,C4,SIM) | P0 | ✅ | `<TBD>` | Ruff configured |
| T0.17 | Configure coverage (`fail_under = 85`, omit gui/main) | P0 | ✅ | `<TBD>` | Gate set |
| T0.18 | Configure pytest (testpaths, addopts) | P0 | ✅ | `<TBD>` | pytest runs |
| T0.19 | Create `tests/unit/` + `tests/integration/` | P0 | ✅ | `<TBD>` | Mirrors src/ |
| T0.20 | Add `tests/conftest.py` shared fixtures | P0 | ✅ | `<TBD>` | Fixtures importable |
| T0.21 | Choose LLM access approach (Cloud API / Ollama / Hybrid) | P0 | ⬜ | `<TBD>` | Recorded in PLAN |
| T0.22 | Store LLM API key in `.env` (git-ignored) | P0 | ⬜ | `<TBD>` | Key not committed |
| T0.23 | Approve `docs/PRD.md` | P0 | ⬜ | `<TBD>` | Sign-off recorded |
| T0.24 | Approve `docs/PLAN.md` | P0 | ⬜ | `<TBD>` | Sign-off recorded |
| T0.25 | Approve `docs/TODO.md` | P0 | ⬜ | `<TBD>` | Sign-off recorded |
| T0.26 | Approve specialized PRDs (game/mcp/nl/strategy/gatekeeper/gmail/email) | P0 | ⬜ | `<TBD>` | All approved |
| T0.27 | Create `assets/` and `results/` folders | P1 | ✅ | `<TBD>` | Folders present |
| T0.28 | Create `README.md` skeleton + Report/Results section | P0 | 🟦 | `<TBD>` | Skeleton committed |
| T0.29 | Add engineering-standards `CLAUDE.md` | P0 | ✅ | `<TBD>` | Present |
| T0.30 | Configure `UserPromptSubmit` reminder hook | P0 | ✅ | `<TBD>` | Hook fires |
| T0.31 | Set up `Sharbel` working branch | P0 | ✅ | `<TBD>` | Branch pushed |
| T0.32 | Create `docs/PROMPT_LOG.md` (prompt-engineering log) | P1 | ⬜ | `<TBD>` | Log file exists |
| T0.33 | Add secret-scan baseline (pre-commit / gitleaks optional) | P2 | ⬜ | `<TBD>` | Scan green |
| T0.34 | Add `Makefile`/`justfile` shortcuts (optional) | P3 | ⬜ | `<TBD>` | Targets run |
| T0.35 | Confirm team name + students placeholders | P1 | ⬜ | `<TBD>` | Filled or TBD |
| T0.36 | Confirm submission team-size rule with course staff | P1 | ⬜ | `<TBD>` | Clarified externally |

## Phase 1 — Game logic & rules engine (Milestone: M1)
_Authoritative deterministic state machine. See PRD_game_engine.md._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T1.1 | Spec & single-concern interface for `services/board.py` — grid, cells, 8-dir neighbours, bounds, barriers | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T1.2 | Define typed models/signatures for `services/board.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T1.3 | RED: write failing unit tests for `services/board.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T1.4 | GREEN: implement `services/board.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T1.5 | Edge-case & boundary tests for `services/board.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T1.6 | Defensive error handling in `services/board.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T1.7 | Refactor `services/board.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T1.8 | Docstrings + why-comments for `services/board.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T1.9 | Ruff clean `services/board.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T1.10 | Mock external deps in `services/board.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T1.11 | Coverage ≥85% for `services/board.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T1.12 | Spec & single-concern interface for `shared/models.py` — Position/Action/Message/GameState/results | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T1.13 | Define typed models/signatures for `shared/models.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T1.14 | RED: write failing unit tests for `shared/models.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T1.15 | GREEN: implement `shared/models.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T1.16 | Edge-case & boundary tests for `shared/models.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T1.17 | Defensive error handling in `shared/models.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T1.18 | Refactor `shared/models.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T1.19 | Docstrings + why-comments for `shared/models.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T1.20 | Ruff clean `shared/models.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T1.21 | Mock external deps in `shared/models.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T1.22 | Coverage ≥85% for `shared/models.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T1.23 | Spec & single-concern interface for `services/game_engine.py` — state machine, apply(), legality, capture | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T1.24 | Define typed models/signatures for `services/game_engine.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T1.25 | RED: write failing unit tests for `services/game_engine.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T1.26 | GREEN: implement `services/game_engine.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T1.27 | Edge-case & boundary tests for `services/game_engine.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T1.28 | Defensive error handling in `services/game_engine.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T1.29 | Refactor `services/game_engine.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T1.30 | Docstrings + why-comments for `services/game_engine.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T1.31 | Ruff clean `services/game_engine.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T1.32 | Mock external deps in `services/game_engine.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T1.33 | Coverage ≥85% for `services/game_engine.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T1.34 | Spec & single-concern interface for `services/scoring.py` — per-subgame + match accumulation (config-driven) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T1.35 | Define typed models/signatures for `services/scoring.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T1.36 | RED: write failing unit tests for `services/scoring.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T1.37 | GREEN: implement `services/scoring.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T1.38 | Edge-case & boundary tests for `services/scoring.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T1.39 | Defensive error handling in `services/scoring.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T1.40 | Refactor `services/scoring.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T1.41 | Docstrings + why-comments for `services/scoring.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T1.42 | Ruff clean `services/scoring.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T1.43 | Mock external deps in `services/scoring.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T1.44 | Coverage ≥85% for `services/scoring.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T1.45 | Spec & single-concern interface for `services/barriers.py` — cop barrier placement, <=max, impassable | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T1.46 | Define typed models/signatures for `services/barriers.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T1.47 | RED: write failing unit tests for `services/barriers.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T1.48 | GREEN: implement `services/barriers.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T1.49 | Edge-case & boundary tests for `services/barriers.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T1.50 | Defensive error handling in `services/barriers.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T1.51 | Refactor `services/barriers.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T1.52 | Docstrings + why-comments for `services/barriers.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T1.53 | Ruff clean `services/barriers.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T1.54 | Mock external deps in `services/barriers.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T1.55 | Coverage ≥85% for `services/barriers.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T1.56 | Seeded RNG for reproducible start positions | P1 | ⬜ | `<TBD>` | Deterministic with fixed seed |
| T1.57 | Turn order (thief first, then cop, alternating) | P0 | ⬜ | `<TBD>` | Alternation verified |
| T1.58 | Diagonal + orthogonal movement only | P0 | ⬜ | `<TBD>` | 8-dir legal moves |
| T1.59 | Reject off-board / into-barrier / no-op MOVE | P0 | ⬜ | `<TBD>` | event=ILLEGAL, state unchanged |
| T1.60 | Capture detection (cop on thief cell) | P0 | ⬜ | `<TBD>` | event=CAPTURE |
| T1.61 | Survival detection (max_moves reached) | P0 | ⬜ | `<TBD>` | event=MAX_MOVES_REACHED |
| T1.62 | Sanity check on 2x2 grid | P1 | ⬜ | `<TBD>` | Correct at 2x2 |
| T1.63 | Sanity check on 3x3 grid | P1 | ⬜ | `<TBD>` | Correct at 3x3 |
| T1.64 | Sanity check on 4x4 grid | P1 | ⬜ | `<TBD>` | Correct at 4x4 |
| T1.65 | Sanity check on 5x5 grid | P1 | ⬜ | `<TBD>` | Correct at 5x5 |
| T1.66 | Integration test: full sub-game ending in capture | P0 | ⬜ | `<TBD>` | cop_win scored |
| T1.67 | Integration test: full sub-game ending in evasion | P0 | ⬜ | `<TBD>` | thief_win scored |
| T1.68 | Verify match total range 30-90 | P1 | ⬜ | `<TBD>` | Bounds hold |

## Phase 2 — MCP communication infrastructure (Milestone: M2)
_Two FastMCP servers exposing tools (no LLM in server). See PRD_mcp_server.md._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T2.1 | Spec & single-concern interface for `mcp/mcp_tools.py` — tool contracts: observe/send/recv/action/verify/status | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T2.2 | Define typed models/signatures for `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T2.3 | RED: write failing unit tests for `mcp/mcp_tools.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T2.4 | GREEN: implement `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T2.5 | Edge-case & boundary tests for `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T2.6 | Defensive error handling in `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T2.7 | Refactor `mcp/mcp_tools.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T2.8 | Docstrings + why-comments for `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T2.9 | Ruff clean `mcp/mcp_tools.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T2.10 | Mock external deps in `mcp/mcp_tools.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T2.11 | Coverage ≥85% for `mcp/mcp_tools.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T2.12 | Spec & single-concern interface for `mcp/cop_server.py` — FastMCP cop server | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T2.13 | Define typed models/signatures for `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T2.14 | RED: write failing unit tests for `mcp/cop_server.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T2.15 | GREEN: implement `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T2.16 | Edge-case & boundary tests for `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T2.17 | Defensive error handling in `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T2.18 | Refactor `mcp/cop_server.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T2.19 | Docstrings + why-comments for `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T2.20 | Ruff clean `mcp/cop_server.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T2.21 | Mock external deps in `mcp/cop_server.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T2.22 | Coverage ≥85% for `mcp/cop_server.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T2.23 | Spec & single-concern interface for `mcp/thief_server.py` — FastMCP thief server | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T2.24 | Define typed models/signatures for `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T2.25 | RED: write failing unit tests for `mcp/thief_server.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T2.26 | GREEN: implement `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T2.27 | Edge-case & boundary tests for `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T2.28 | Defensive error handling in `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T2.29 | Refactor `mcp/thief_server.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T2.30 | Docstrings + why-comments for `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T2.31 | Ruff clean `mcp/thief_server.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T2.32 | Mock external deps in `mcp/thief_server.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T2.33 | Coverage ≥85% for `mcp/thief_server.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T2.34 | Spec & single-concern interface for `shared/mcp_transport.py` — HTTP(S) client transport (via gatekeeper) | P0 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T2.35 | Define typed models/signatures for `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T2.36 | RED: write failing unit tests for `shared/mcp_transport.py` (happy path) | P0 | ⬜ | `<TBD>` | Failing tests committed |
| T2.37 | GREEN: implement `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | Happy-path tests pass |
| T2.38 | Edge-case & boundary tests for `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T2.39 | Defensive error handling in `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T2.40 | Refactor `shared/mcp_transport.py`: DRY, ≤150 lines, single responsibility | P0 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T2.41 | Docstrings + why-comments for `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | Module/functions documented |
| T2.42 | Ruff clean `shared/mcp_transport.py` | P0 | ⬜ | `<TBD>` | 0 ruff violations |
| T2.43 | Mock external deps in `shared/mcp_transport.py` tests | P0 | ⬜ | `<TBD>` | No live external calls |
| T2.44 | Coverage ≥85% for `shared/mcp_transport.py` + add README Work Log row | P0 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T2.45 | Spec & single-concern interface for `shared/mcp_auth.py` — token-based auth + revocation | P0 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T2.46 | Define typed models/signatures for `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T2.47 | RED: write failing unit tests for `shared/mcp_auth.py` (happy path) | P0 | ⬜ | `<TBD>` | Failing tests committed |
| T2.48 | GREEN: implement `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | Happy-path tests pass |
| T2.49 | Edge-case & boundary tests for `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T2.50 | Defensive error handling in `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T2.51 | Refactor `shared/mcp_auth.py`: DRY, ≤150 lines, single responsibility | P0 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T2.52 | Docstrings + why-comments for `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | Module/functions documented |
| T2.53 | Ruff clean `shared/mcp_auth.py` | P0 | ⬜ | `<TBD>` | 0 ruff violations |
| T2.54 | Mock external deps in `shared/mcp_auth.py` tests | P0 | ⬜ | `<TBD>` | No live external calls |
| T2.55 | Coverage ≥85% for `shared/mcp_auth.py` + add README Work Log row | P0 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T2.56 | Distinct localhost ports for cop/thief from config | P0 | ⬜ | `<TBD>` | Ports config-driven |
| T2.57 | `get_observation` returns partial view | P0 | ⬜ | `<TBD>` | Visibility radius honoured |
| T2.58 | `send_message`/`receive_message` round-trip | P0 | ⬜ | `<TBD>` | NL message delivered |
| T2.59 | `submit_action` reaches authoritative engine | P0 | ⬜ | `<TBD>` | Correct TurnResult |
| T2.60 | `verify_location` returns authoritative position | P0 | ⬜ | `<TBD>` | Not agent belief |
| T2.61 | `get_game_status` returns turn/moves/barriers/score | P0 | ⬜ | `<TBD>` | Accurate |
| T2.62 | Health-check for both servers | P1 | ⬜ | `<TBD>` | Both healthy |
| T2.63 | Integration test: tool round-trip via mocked transport | P0 | ⬜ | `<TBD>` | Contracts covered |

## Phase 3 — Orchestrator & full local match (Milestone: M3)
_Match/sub-game loop and single SDK entry point._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T3.1 | Spec & single-concern interface for `services/orchestrator.py` — match & sub-game loop | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T3.2 | Define typed models/signatures for `services/orchestrator.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T3.3 | RED: write failing unit tests for `services/orchestrator.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T3.4 | GREEN: implement `services/orchestrator.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T3.5 | Edge-case & boundary tests for `services/orchestrator.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T3.6 | Defensive error handling in `services/orchestrator.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T3.7 | Refactor `services/orchestrator.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T3.8 | Docstrings + why-comments for `services/orchestrator.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T3.9 | Ruff clean `services/orchestrator.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T3.10 | Mock external deps in `services/orchestrator.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T3.11 | Coverage ≥85% for `services/orchestrator.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T3.12 | Spec & single-concern interface for `services/turn_pipeline.py` — observe->decide->tool->apply->score | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T3.13 | Define typed models/signatures for `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T3.14 | RED: write failing unit tests for `services/turn_pipeline.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T3.15 | GREEN: implement `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T3.16 | Edge-case & boundary tests for `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T3.17 | Defensive error handling in `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T3.18 | Refactor `services/turn_pipeline.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T3.19 | Docstrings + why-comments for `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T3.20 | Ruff clean `services/turn_pipeline.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T3.21 | Mock external deps in `services/turn_pipeline.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T3.22 | Coverage ≥85% for `services/turn_pipeline.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T3.23 | Spec & single-concern interface for `services/accumulator.py` — accumulate sub-game results | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T3.24 | Define typed models/signatures for `services/accumulator.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T3.25 | RED: write failing unit tests for `services/accumulator.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T3.26 | GREEN: implement `services/accumulator.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T3.27 | Edge-case & boundary tests for `services/accumulator.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T3.28 | Defensive error handling in `services/accumulator.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T3.29 | Refactor `services/accumulator.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T3.30 | Docstrings + why-comments for `services/accumulator.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T3.31 | Ruff clean `services/accumulator.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T3.32 | Mock external deps in `services/accumulator.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T3.33 | Coverage ≥85% for `services/accumulator.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T3.34 | Spec & single-concern interface for `sdk/sdk.py` — single public entry point for all logic | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T3.35 | Define typed models/signatures for `sdk/sdk.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T3.36 | RED: write failing unit tests for `sdk/sdk.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T3.37 | GREEN: implement `sdk/sdk.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T3.38 | Edge-case & boundary tests for `sdk/sdk.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T3.39 | Defensive error handling in `sdk/sdk.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T3.40 | Refactor `sdk/sdk.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T3.41 | Docstrings + why-comments for `sdk/sdk.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T3.42 | Ruff clean `sdk/sdk.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T3.43 | Mock external deps in `sdk/sdk.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T3.44 | Coverage ≥85% for `sdk/sdk.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T3.45 | Spec & single-concern interface for `main.py` — thin entrypoint -> sdk | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T3.46 | Define typed models/signatures for `main.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T3.47 | RED: write failing unit tests for `main.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T3.48 | GREEN: implement `main.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T3.49 | Edge-case & boundary tests for `main.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T3.50 | Defensive error handling in `main.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T3.51 | Refactor `main.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T3.52 | Docstrings + why-comments for `main.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T3.53 | Ruff clean `main.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T3.54 | Mock external deps in `main.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T3.55 | Coverage ≥85% for `main.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T3.56 | Run 6 consecutive sub-games (<=25 moves each) | P0 | ⬜ | `<TBD>` | Full match runs |
| T3.57 | Technical-loss detection + re-run to fill quota of 6 | P1 | ⬜ | `<TBD>` | Failed game re-run |
| T3.58 | CLI/GUI/tests call SDK only | P0 | ⬜ | `<TBD>` | No business logic outside |
| T3.59 | Deterministic seeded full-match integration test | P0 | ⬜ | `<TBD>` | Reproducible |
| T3.60 | Autonomous run: init -> report, zero manual steps | P0 | ⬜ | `<TBD>` | No intervention |

## Phase 4 — Decision strategy (Milestone: M4)
_Heuristic policies + optional tabular Q-learning. See PRD_decision_strategy.md._
> **As-built (2026-06-25):** greedy cop+thief live together in `services/strategy/heuristic.py`
> (one module, not separate `heuristic_cop.py`/`heuristic_thief.py`); the **cornering "smart" cop** is
> `services/strategy/smart_cop.py` with shared distance in `geometry.py`. The `Strategy` interface is the
> lightweight `Decider` Callable (`turn_pipeline.py`) + the `COP_POLICIES` registry in the orchestrator,
> not a Template-Method base class. `belief_model.py`/`q_table.py` remain optional/pending.

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T4.1 | Spec & single-concern interface for `services/strategy/strategy_base.py` — Strategy interface (Template Method) | P0 | 🟦 | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.2 | Define typed models/signatures for `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | Typed inputs/outputs defined |
| T4.3 | RED: write failing unit tests for `services/strategy/strategy_base.py` (happy path) | P0 | 🟦 | `<TBD>` | Failing tests committed |
| T4.4 | GREEN: implement `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | Happy-path tests pass |
| T4.5 | Edge-case & boundary tests for `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | Empty/invalid/limit inputs covered |
| T4.6 | Defensive error handling in `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | Graceful failure + clear message |
| T4.7 | Refactor `services/strategy/strategy_base.py`: DRY, ≤150 lines, single responsibility | P0 | 🟦 | `<TBD>` | No duplication; ≤150 LOC |
| T4.8 | Docstrings + why-comments for `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | Module/functions documented |
| T4.9 | Ruff clean `services/strategy/strategy_base.py` | P0 | 🟦 | `<TBD>` | 0 ruff violations |
| T4.10 | Mock external deps in `services/strategy/strategy_base.py` tests | P0 | 🟦 | `<TBD>` | No live external calls |
| T4.11 | Coverage ≥85% for `services/strategy/strategy_base.py` + add README Work Log row | P0 | 🟦 | `<TBD>` | ≥85% coverage; Work Log updated |
| T4.12 | Spec & single-concern interface for cop pursuit policy (as-built: `heuristic.cop_action`) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.13 | Define typed models/signatures for the cop policy | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T4.14 | RED: write failing unit tests for the cop policy (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T4.15 | GREEN: implement the cop policy (`heuristic.cop_action`) | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T4.16 | Edge-case & boundary tests for the cop policy | P0 | ✅ | `<TBD>` | Boxed-in/no-move cases covered |
| T4.17 | Defensive error handling in the cop policy | P0 | ✅ | `<TBD>` | Falls back to STAY; engine validates |
| T4.18 | Refactor cop policy: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | Shared `geometry.chebyshev`; ≤150 LOC |
| T4.19 | Docstrings + why-comments for the cop policy | P0 | ✅ | `<TBD>` | Module/functions documented |
| T4.20 | Ruff clean the cop policy module | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T4.21 | Mock external deps in cop-policy tests | P0 | ✅ | `<TBD>` | Pure/offline; no live external calls |
| T4.22 | Coverage ≥85% for the cop policy + add README Work Log row | P0 | ✅ | `<TBD>` | 100% coverage; Work Log updated |
| T4.23 | Spec & single-concern interface for thief evasion policy (as-built: `heuristic.thief_action`) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.24 | Define typed models/signatures for the thief policy | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T4.25 | RED: write failing unit tests for the thief policy (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T4.26 | GREEN: implement the thief policy (`heuristic.thief_action`) | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T4.27 | Edge-case & boundary tests for the thief policy | P0 | ✅ | `<TBD>` | Boxed-in stay case covered |
| T4.28 | Defensive error handling in the thief policy | P0 | ✅ | `<TBD>` | Falls back to STAY; engine validates |
| T4.29 | Refactor thief policy: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | Shared `geometry.chebyshev`; ≤150 LOC |
| T4.30 | Docstrings + why-comments for the thief policy | P0 | ✅ | `<TBD>` | Module/functions documented |
| T4.31 | Ruff clean the thief policy module | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T4.32 | Mock external deps in thief-policy tests | P0 | ✅ | `<TBD>` | Pure/offline; no live external calls |
| T4.33 | Coverage ≥85% for the thief policy + add README Work Log row | P0 | ✅ | `<TBD>` | 100% coverage; Work Log updated |
| T4.34 | Spec & single-concern interface for `services/strategy/belief_model.py` — belief over opponent cell (partial obs) | P1 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.35 | Define typed models/signatures for `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T4.36 | RED: write failing unit tests for `services/strategy/belief_model.py` (happy path) | P1 | ⬜ | `<TBD>` | Failing tests committed |
| T4.37 | GREEN: implement `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | Happy-path tests pass |
| T4.38 | Edge-case & boundary tests for `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T4.39 | Defensive error handling in `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T4.40 | Refactor `services/strategy/belief_model.py`: DRY, ≤150 lines, single responsibility | P1 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T4.41 | Docstrings + why-comments for `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | Module/functions documented |
| T4.42 | Ruff clean `services/strategy/belief_model.py` | P1 | ⬜ | `<TBD>` | 0 ruff violations |
| T4.43 | Mock external deps in `services/strategy/belief_model.py` tests | P1 | ⬜ | `<TBD>` | No live external calls |
| T4.44 | Coverage ≥85% for `services/strategy/belief_model.py` + add README Work Log row | P1 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T4.45 | Spec & single-concern interface for `services/strategy/q_table.py` — optional tabular Q-learning | P3 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.46 | Define typed models/signatures for `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T4.47 | RED: write failing unit tests for `services/strategy/q_table.py` (happy path) | P3 | ⬜ | `<TBD>` | Failing tests committed |
| T4.48 | GREEN: implement `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | Happy-path tests pass |
| T4.49 | Edge-case & boundary tests for `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T4.50 | Defensive error handling in `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T4.51 | Refactor `services/strategy/q_table.py`: DRY, ≤150 lines, single responsibility | P3 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T4.52 | Docstrings + why-comments for `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | Module/functions documented |
| T4.53 | Ruff clean `services/strategy/q_table.py` | P3 | ⬜ | `<TBD>` | 0 ruff violations |
| T4.54 | Mock external deps in `services/strategy/q_table.py` tests | P3 | ⬜ | `<TBD>` | No live external calls |
| T4.55 | Coverage ≥85% for `services/strategy/q_table.py` + add README Work Log row | P3 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T4.56 | Strategy selection via config (heuristic\|smart\|q_table) | P1 | ✅ | `<TBD>` | `select_cop_policy` (via `COP_POLICIES` registry) switches with no code change |
| T4.57 | Heuristic beats random baseline | P1 | ⬜ | `<TBD>` | Win-rate > 50% |
| T4.58 | Chebyshev/distance utilities | P1 | ✅ | `<TBD>` | `services/strategy/geometry.py`, unit-tested |
| T4.59 | (Opt) Q-state encoding compact for 5x5 | P3 | ⬜ | `<TBD>` | State space bounded |
| T4.60 | (Opt) Q-update matches Bellman on hand example | P3 | ⬜ | `<TBD>` | Unit test passes |
| T4.61 | (Opt) Epsilon-greedy explore/exploit | P3 | ⬜ | `<TBD>` | Policy implemented |
| T4.62 | (Opt) Training loop over episodes | P3 | ⬜ | `<TBD>` | Q-table improves |
| T4.63 | (Opt) Learning-curve plot saved to results/ | P3 | ⬜ | `<TBD>` | Curve in README |
| T4.64 | Spec & single-concern interface for `services/strategy/smart_cop.py` — cornering 1-ply cop | P1 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T4.65 | RED+GREEN: implement `smart_cop.smart_cop_action` (lexicographic `(distance, escape-options)` eval after thief reply) | P1 | ✅ | `<TBD>` | Tests pass; breaks the greedy limit cycle |
| T4.66 | Edge/boundary tests for smart cop (immediate capture, boxed-in stay, determinism) | P1 | ✅ | `<TBD>` | 100% coverage |
| T4.67 | Empirical capture-rate ≥ greedy (100% on 3×3–7×7, 60 seeds) | P1 | ✅ | `<TBD>` | Measured; `test_corners_thief_on_every_sampled_seed` |
| T4.68 | Config-driven `smart` selection in `Orchestrator` + reject unknown strategy | P1 | ✅ | `<TBD>` | `test_smart_strategy_is_selected_and_dominates` / `test_unknown_strategy_is_rejected` |
| T4.69 | Refresh comparison graphs (greedy vs smart vs NL; grid-size overlay) via `make_figures.py` | P1 | ✅ | `<TBD>` | `assets/heuristic_vs_nl.png`, `assets/winrate_vs_gridsize.png` |
| T4.70 | Update `PRD_decision_strategy.md` §3.1 + README R.3 (cornering policy + barrier analysis) | P1 | ✅ | `<TBD>` | Docs reflect as-built |

## Phase 5 — Natural-language integration (Milestone: M5)
_Free-text protocol + belief update; robust to ambiguity/deception. See PRD_nl_communication.md._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T5.1 | Spec & single-concern interface for `services/nl_protocol/nl_encode.py` — intent -> free text | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T5.2 | Define typed models/signatures for `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T5.3 | RED: write failing unit tests for `services/nl_protocol/nl_encode.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T5.4 | GREEN: implement `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T5.5 | Edge-case & boundary tests for `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T5.6 | Defensive error handling in `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T5.7 | Refactor `services/nl_protocol/nl_encode.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T5.8 | Docstrings + why-comments for `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T5.9 | Ruff clean `services/nl_protocol/nl_encode.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T5.10 | Mock external deps in `services/nl_protocol/nl_encode.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T5.11 | Coverage ≥85% for `services/nl_protocol/nl_encode.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T5.12 | Spec & single-concern interface for `services/nl_protocol/nl_decode.py` — free text -> belief update | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T5.13 | Define typed models/signatures for `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T5.14 | RED: write failing unit tests for `services/nl_protocol/nl_decode.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T5.15 | GREEN: implement `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T5.16 | Edge-case & boundary tests for `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T5.17 | Defensive error handling in `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T5.18 | Refactor `services/nl_protocol/nl_decode.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T5.19 | Docstrings + why-comments for `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T5.20 | Ruff clean `services/nl_protocol/nl_decode.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T5.21 | Mock external deps in `services/nl_protocol/nl_decode.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T5.22 | Coverage ≥85% for `services/nl_protocol/nl_decode.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T5.23 | Spec & single-concern interface for `services/nl_protocol/prompt_templates.py` — system/cop/thief prompts | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T5.24 | Define typed models/signatures for `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T5.25 | RED: write failing unit tests for `services/nl_protocol/prompt_templates.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T5.26 | GREEN: implement `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T5.27 | Edge-case & boundary tests for `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T5.28 | Defensive error handling in `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T5.29 | Refactor `services/nl_protocol/prompt_templates.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T5.30 | Docstrings + why-comments for `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T5.31 | Ruff clean `services/nl_protocol/prompt_templates.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T5.32 | Mock external deps in `services/nl_protocol/prompt_templates.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T5.33 | Coverage ≥85% for `services/nl_protocol/prompt_templates.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T5.34 | Spec & single-concern interface for `shared/llm_client.py` — LLM transport via gatekeeper | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T5.35 | Define typed models/signatures for `shared/llm_client.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T5.36 | RED: write failing unit tests for `shared/llm_client.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T5.37 | GREEN: implement `shared/llm_client.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T5.38 | Edge-case & boundary tests for `shared/llm_client.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T5.39 | Defensive error handling in `shared/llm_client.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T5.40 | Refactor `shared/llm_client.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T5.41 | Docstrings + why-comments for `shared/llm_client.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T5.42 | Ruff clean `shared/llm_client.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T5.43 | Mock external deps in `shared/llm_client.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T5.44 | Coverage ≥85% for `shared/llm_client.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T5.45 | Spec & single-concern interface for `services/nl_protocol/ambiguity_handler.py` — defensive parse, never crash | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T5.46 | Define typed models/signatures for `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T5.47 | RED: write failing unit tests for `services/nl_protocol/ambiguity_handler.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T5.48 | GREEN: implement `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T5.49 | Edge-case & boundary tests for `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T5.50 | Defensive error handling in `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T5.51 | Refactor `services/nl_protocol/ambiguity_handler.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T5.52 | Docstrings + why-comments for `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T5.53 | Ruff clean `services/nl_protocol/ambiguity_handler.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T5.54 | Mock external deps in `services/nl_protocol/ambiguity_handler.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T5.55 | Coverage ≥85% for `services/nl_protocol/ambiguity_handler.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T5.56 | Deception handling: weight observation over message | P1 | ✅ | `<TBD>` | Obs dominates conflict |
| T5.57 | Belief convergence over a sub-game | P1 | ⬜ | `<TBD>` | Top cell -> true cell |
| T5.58 | 100% of inbound messages -> valid belief update | P0 | ✅ | `<TBD>` | 0 crashes on ambiguity |
| T5.59 | Maintain prompt-engineering log entries | P1 | 🟦 | `<TBD>` | PROMPT_LOG.md updated |
| T5.60 | Mock LLM in all NL unit tests | P0 | ✅ | `<TBD>` | No live calls |

## Phase 6 — GUI & CLI (Milestone: M6)
_Real-time visualization and CLI logs (read state from SDK only)._
> **As-built (2026-06-25):** the GUI shipped as `gui/board_renderer.py` (`render_state` + `save_state_png`)
> and `gui/match_animator.py` (`animate_match` / `animate_nl_match` → animated GIF, with NL message overlay
> for the NL match), **not** `gui/gui_renderer.py` / `gui/gui_realtime.py`. T6.1–T6.22 are re-mapped to
> those two modules. The **live interactive window** now ships as `gui/live_viewer.py` (`--live`): it renders
> the service-layer per-turn frame stream (`services/match_stream.py` + `nl_subgame_stream`) live, drawing
> each turn the instant the engine computes it (T6.39–T6.48). The **GIF animation** remains for headless/report use.

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T6.1 | Spec & single-concern interface for `gui/board_renderer.py` — draw grid/agents/barriers | P1 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T6.2 | Define typed models/signatures for `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T6.3 | RED: write failing unit tests for `gui/board_renderer.py` (happy path) | P1 | ✅ | `<TBD>` | Failing tests committed |
| T6.4 | GREEN: implement `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | Happy-path tests pass |
| T6.5 | Edge-case & boundary tests for `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T6.6 | Defensive error handling in `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | Graceful failure + clear message |
| T6.7 | Refactor `gui/board_renderer.py`: DRY, ≤150 lines, single responsibility | P1 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T6.8 | Docstrings + why-comments for `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | Module/functions documented |
| T6.9 | Ruff clean `gui/board_renderer.py` | P1 | ✅ | `<TBD>` | 0 ruff violations |
| T6.10 | Mock external deps in `gui/board_renderer.py` tests | P1 | ✅ | `<TBD>` | No live external calls |
| T6.11 | Coverage ≥85% for `gui/board_renderer.py` + add README Work Log row | P1 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T6.12 | Spec & single-concern interface for `gui/match_animator.py` — animated GIF of each turn (live interactive window pending) | P1 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T6.13 | Define typed models/signatures for `gui/match_animator.py` | P1 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T6.14 | RED: write failing unit tests for `gui/match_animator.py` (happy path) | P1 | ✅ | `<TBD>` | Failing tests committed |
| T6.15 | GREEN: implement `gui/match_animator.py` | P1 | ✅ | `<TBD>` | Happy-path tests pass |
| T6.16 | Edge-case & boundary tests for `gui/match_animator.py` | P1 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T6.17 | Defensive error handling in `gui/match_animator.py` | P1 | ✅ | `<TBD>` | Graceful failure + clear message |
| T6.18 | Refactor `gui/match_animator.py`: DRY, ≤150 lines, single responsibility | P1 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T6.19 | Docstrings + why-comments for `gui/match_animator.py` | P1 | ✅ | `<TBD>` | Module/functions documented |
| T6.20 | Ruff clean `gui/match_animator.py` | P1 | ✅ | `<TBD>` | 0 ruff violations |
| T6.21 | Mock external deps in `gui/match_animator.py` tests | P1 | ✅ | `<TBD>` | No live external calls |
| T6.22 | Coverage ≥85% for `gui/match_animator.py` + add README Work Log row | P1 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T6.23 | Spec & single-concern interface for `cli/cli_runner.py` — CLI match runner + structured logs | P1 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T6.24 | Define typed models/signatures for `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T6.25 | RED: write failing unit tests for `cli/cli_runner.py` (happy path) | P1 | ⬜ | `<TBD>` | Failing tests committed |
| T6.26 | GREEN: implement `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | Happy-path tests pass |
| T6.27 | Edge-case & boundary tests for `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T6.28 | Defensive error handling in `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T6.29 | Refactor `cli/cli_runner.py`: DRY, ≤150 lines, single responsibility | P1 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T6.30 | Docstrings + why-comments for `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | Module/functions documented |
| T6.31 | Ruff clean `cli/cli_runner.py` | P1 | ⬜ | `<TBD>` | 0 ruff violations |
| T6.32 | Mock external deps in `cli/cli_runner.py` tests | P1 | ⬜ | `<TBD>` | No live external calls |
| T6.33 | Coverage ≥85% for `cli/cli_runner.py` + add README Work Log row | P1 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T6.34 | Capture GUI screenshots of key states -> assets/ | P1 | 🟦 | `<TBD>` | Screenshots in README |
| T6.35 | CLI structured logs of MCP communication | P1 | ⬜ | `<TBD>` | Logs prove comms |
| T6.36 | GUI reads state from SDK only | P0 | ✅ | `<TBD>` | No logic in GUI |
| T6.37 | Clear labels/legend + accessible colors | P2 | ⬜ | `<TBD>` | Readable |
| T6.38 | Record short demo run (gif/video link) | P2 | ⬜ | `<TBD>` | Linked in README |
| T6.39 | Spec & single-concern interface for `services/match_stream.py` — per-turn `(state, caption)` streams | P1 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T6.40 | RED: failing unit tests for `services/match_stream.py` (heuristic stream + shared loop) | P1 | ✅ | `<TBD>` | Failing tests committed |
| T6.41 | GREEN: implement `services/match_stream.py` (`stream_subgame`, `heuristic_subgame_stream`) | P1 | ✅ | `<TBD>` | Tests pass; 100% cov |
| T6.42 | Refactor `nl_match.py` to a generator (`nl_subgame_stream`) reusing `stream_subgame` (DRY) | P1 | ✅ | `<TBD>` | No duplicated engine loop; tests pass |
| T6.43 | Refactor `gui/match_animator.py` to consume the shared stream (drop in-GUI game loop) | P1 | ✅ | `<TBD>` | GIF unchanged; no logic in GUI |
| T6.44 | Spec & interface for `gui/live_viewer.py` — interactive real-time window (render-only) | P1 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T6.45 | GREEN: implement `gui/live_viewer.py` (`play_live`, runtime interactive backend) | P1 | ✅ | `<TBD>` | Renders each frame as it streams |
| T6.46 | Smoke test `gui/live_viewer.py` headlessly (mock matplotlib; no window) | P1 | ✅ | `<TBD>` | No live window in tests |
| T6.47 | Expose streams via SDK (`stream_simple_frames`, `stream_nl_frames`) + `--live` CLI flag | P0 | ✅ | `<TBD>` | SDK-only; CLI delegates |
| T6.48 | Config `gui.live_backend` + `gui.poll_interval_ms` (no hardcoded values) | P1 | ✅ | `<TBD>` | Config-driven; defaults documented |
| T6.49 | RED: tests for live-viewer threading helpers (`_produce` enqueue+sentinel, `_render_tick` render/empty/done) | P1 | ✅ | `<TBD>` | Failing tests committed |
| T6.50 | GREEN: run frame generator on a daemon worker thread → `queue.Queue` (no blocking on GUI thread) | P1 | ✅ | `<TBD>` | Producer thread feeds queue + sentinel |
| T6.51 | GREEN: drain queue on `fig.canvas.new_timer` tick on the main thread; stop on sentinel | P1 | ✅ | `<TBD>` | Event loop never blocks; window responsive |
| T6.52 | Fix "not responding" freeze during per-turn LLM wait + document threading (PLAN §4, README R.4, PROMPT_LOG A12) | P1 | ✅ | `<TBD>` | Window stays responsive while turns compute |

## Phase 7 — Cloud deployment & security (Milestone: M7)
_Deploy both MCP servers with token auth (deployment tasks, not modules)._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T7.1 | Choose cloud platform (Prefect Cloud / similar) | P0 | ⬜ | `<TBD>` | Decision recorded |
| T7.2 | Package/containerize cop MCP server | P0 | ⬜ | `<TBD>` | Deployable artifact |
| T7.3 | Package/containerize thief MCP server | P0 | ⬜ | `<TBD>` | Deployable artifact |
| T7.4 | Deploy cop MCP server | P0 | ⬜ | `<TBD>` | Running in cloud |
| T7.5 | Deploy thief MCP server | P0 | ⬜ | `<TBD>` | Running in cloud |
| T7.6 | Obtain public HTTPS URL for cop | P0 | ⬜ | `<TBD>` | URL reachable |
| T7.7 | Obtain public HTTPS URL for thief | P0 | ⬜ | `<TBD>` | URL reachable |
| T7.8 | Token-based auth on cop URL | P0 | ⬜ | `<TBD>` | Unauthorized rejected |
| T7.9 | Token-based auth on thief URL | P0 | ⬜ | `<TBD>` | Unauthorized rejected |
| T7.10 | Token revocation mechanism | P1 | ⬜ | `<TBD>` | Revoke works |
| T7.11 | Verify URLs not firewalled / not public-blocked | P0 | ⬜ | `<TBD>` | Reachable as required |
| T7.12 | Hybrid: client+LLM local, outbound-only requests | P1 | ⬜ | `<TBD>` | No inbound ports |
| T7.13 | Document ngrok Traffic Policy option | P2 | ⬜ | `<TBD>` | In README |
| T7.14 | Document Localtonet option | P2 | ⬜ | `<TBD>` | In README |
| T7.15 | Document Nginx reverse proxy + SSL (Certbot) | P2 | ⬜ | `<TBD>` | In README |
| T7.16 | Store URLs/tokens in `.env` (git-ignored) | P0 | ⬜ | `<TBD>` | Not committed |
| T7.17 | Latency check intra-region (<200ms round-trip) | P2 | ⬜ | `<TBD>` | Within budget |
| T7.18 | Retry/backoff on cloud calls via gatekeeper | P1 | ⬜ | `<TBD>` | Transient retried |
| T7.19 | End-to-end cloud match (6 games) | P0 | ⬜ | `<TBD>` | Completes autonomously |
| T7.20 | README deployment section + screenshots | P1 | ⬜ | `<TBD>` | Documented |
| T7.21 | Firewall/non-standard-port caveat documented | P1 | ⬜ | `<TBD>` | In README |
| T7.22 | Rotate tokens before submission | P2 | ⬜ | `<TBD>` | Rotated |
| T7.23 | Monitor usage / minimal permissions | P2 | ⬜ | `<TBD>` | Least privilege |
| T7.24 | Health checks on cloud URLs | P1 | ⬜ | `<TBD>` | Monitored |
| T7.25 | Rollback / redeploy procedure | P2 | ⬜ | `<TBD>` | Documented |
| T7.26 | Cloud cost note | P3 | ⬜ | `<TBD>` | Estimated |
| T7.27 | Capture CLI logs from a cloud run | P1 | ⬜ | `<TBD>` | Saved to results/ |

## Phase 8 — Gmail/Calendar agent & reporting (Milestone: M8)
_Google setup + read/extract/calendar/send agent + JSON report. See PRD_gmail_calendar_agent.md & PRD_email_reporting.md._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T8.1 | Spec & single-concern interface for `shared/google_auth.py` — OAuth flow, token load/refresh/recovery | P0 | 🟦 | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.2 | Define typed models/signatures for `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | Typed inputs/outputs defined |
| T8.3 | RED: write failing unit tests for `shared/google_auth.py` (happy path) | P0 | 🟦 | `<TBD>` | Failing tests committed |
| T8.4 | GREEN: implement `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | Happy-path tests pass |
| T8.5 | Edge-case & boundary tests for `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.6 | Defensive error handling in `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | Graceful failure + clear message |
| T8.7 | Refactor `shared/google_auth.py`: DRY, ≤150 lines, single responsibility | P0 | 🟦 | `<TBD>` | No duplication; ≤150 LOC |
| T8.8 | Docstrings + why-comments for `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | Module/functions documented |
| T8.9 | Ruff clean `shared/google_auth.py` | P0 | 🟦 | `<TBD>` | 0 ruff violations |
| T8.10 | Mock external deps in `shared/google_auth.py` tests | P0 | 🟦 | `<TBD>` | No live external calls |
| T8.11 | Coverage ≥85% for `shared/google_auth.py` + add README Work Log row | P0 | 🟦 | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.12 | Spec & single-concern interface for `shared/gmail_client.py` — Gmail read + send (via gatekeeper) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.13 | Define typed models/signatures for `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T8.14 | RED: write failing unit tests for `shared/gmail_client.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T8.15 | GREEN: implement `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T8.16 | Edge-case & boundary tests for `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.17 | Defensive error handling in `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T8.18 | Refactor `shared/gmail_client.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T8.19 | Docstrings + why-comments for `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T8.20 | Ruff clean `shared/gmail_client.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T8.21 | Mock external deps in `shared/gmail_client.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T8.22 | Coverage ≥85% for `shared/gmail_client.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.23 | Spec & single-concern interface for `shared/calendar_client.py` — Google Calendar events (via gatekeeper) | P0 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.24 | Define typed models/signatures for `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T8.25 | RED: write failing unit tests for `shared/calendar_client.py` (happy path) | P0 | ⬜ | `<TBD>` | Failing tests committed |
| T8.26 | GREEN: implement `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | Happy-path tests pass |
| T8.27 | Edge-case & boundary tests for `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.28 | Defensive error handling in `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T8.29 | Refactor `shared/calendar_client.py`: DRY, ≤150 lines, single responsibility | P0 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T8.30 | Docstrings + why-comments for `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | Module/functions documented |
| T8.31 | Ruff clean `shared/calendar_client.py` | P0 | ⬜ | `<TBD>` | 0 ruff violations |
| T8.32 | Mock external deps in `shared/calendar_client.py` tests | P0 | ⬜ | `<TBD>` | No live external calls |
| T8.33 | Coverage ≥85% for `shared/calendar_client.py` + add README Work Log row | P0 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.34 | Spec & single-concern interface for `services/google_agent/email_reader.py` — read_emails() | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.35 | Define typed models/signatures for `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T8.36 | RED: write failing unit tests for `services/google_agent/email_reader.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T8.37 | GREEN: implement `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T8.38 | Edge-case & boundary tests for `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.39 | Defensive error handling in `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T8.40 | Refactor `services/google_agent/email_reader.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T8.41 | Docstrings + why-comments for `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T8.42 | Ruff clean `services/google_agent/email_reader.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T8.43 | Mock external deps in `services/google_agent/email_reader.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T8.44 | Coverage ≥85% for `services/google_agent/email_reader.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.45 | Spec & single-concern interface for `services/google_agent/meeting_extractor.py` — extract_meeting() (LLM-assisted) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.46 | Define typed models/signatures for `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T8.47 | RED: write failing unit tests for `services/google_agent/meeting_extractor.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T8.48 | GREEN: implement `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T8.49 | Edge-case & boundary tests for `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.50 | Defensive error handling in `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T8.51 | Refactor `services/google_agent/meeting_extractor.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T8.52 | Docstrings + why-comments for `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T8.53 | Ruff clean `services/google_agent/meeting_extractor.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T8.54 | Mock external deps in `services/google_agent/meeting_extractor.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T8.55 | Coverage ≥85% for `services/google_agent/meeting_extractor.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.56 | Spec & single-concern interface for `services/google_agent/calendar_writer.py` — add_calendar_event() | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.57 | Define typed models/signatures for `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T8.58 | RED: write failing unit tests for `services/google_agent/calendar_writer.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T8.59 | GREEN: implement `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T8.60 | Edge-case & boundary tests for `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.61 | Defensive error handling in `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T8.62 | Refactor `services/google_agent/calendar_writer.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T8.63 | Docstrings + why-comments for `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T8.64 | Ruff clean `services/google_agent/calendar_writer.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T8.65 | Mock external deps in `services/google_agent/calendar_writer.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T8.66 | Coverage ≥85% for `services/google_agent/calendar_writer.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.67 | Spec & single-concern interface for `services/reporting.py` — build JSON report + send via send_email | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T8.68 | Define typed models/signatures for `services/reporting.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined |
| T8.69 | RED: write failing unit tests for `services/reporting.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T8.70 | GREEN: implement `services/reporting.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T8.71 | Edge-case & boundary tests for `services/reporting.py` | P0 | ✅ | `<TBD>` | Empty/invalid/limit inputs covered |
| T8.72 | Defensive error handling in `services/reporting.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message |
| T8.73 | Refactor `services/reporting.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | No duplication; ≤150 LOC |
| T8.74 | Docstrings + why-comments for `services/reporting.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T8.75 | Ruff clean `services/reporting.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T8.76 | Mock external deps in `services/reporting.py` tests | P0 | ✅ | `<TBD>` | No live external calls |
| T8.77 | Coverage ≥85% for `services/reporting.py` + add README Work Log row | P0 | ✅ | `<TBD>` | ≥85% coverage; Work Log updated |
| T8.78 | Create Google Cloud project (snake_case name) | P0 | ⬜ | `<TBD>` | Project exists |
| T8.79 | Enable Gmail API | P0 | ⬜ | `<TBD>` | Enabled |
| T8.80 | Enable Google Calendar API | P0 | ⬜ | `<TBD>` | Enabled |
| T8.81 | Configure OAuth consent (External, Testing) | P0 | ⬜ | `<TBD>` | Consent configured |
| T8.82 | Set app name + user-support email | P0 | ⬜ | `<TBD>` | Filled |
| T8.83 | Add developer contact email | P0 | ⬜ | `<TBD>` | Filled |
| T8.84 | Create OAuth client of type Desktop | P0 | ⬜ | `<TBD>` | Client created |
| T8.85 | Add scope gmail.modify (read+send) | P0 | ⬜ | `<TBD>` | Scope present |
| T8.86 | Add scope calendar | P0 | ⬜ | `<TBD>` | Scope present |
| T8.87 | Download `client_secret.json` to external secret folder | P0 | ⬜ | `<TBD>` | Outside repo |
| T8.88 | Add sending Gmail as Test user | P0 | ⬜ | `<TBD>` | Consent allowed |
| T8.89 | Add teammates as Test users | P1 | ⬜ | `<TBD>` | All can authenticate |
| T8.90 | `.gitignore` client_secret.json/token.json | P0 | ⬜ | `<TBD>` | Ignored |
| T8.91 | Env/config for `secrets_dir` | P0 | ⬜ | `<TBD>` | Located via config |
| T8.92 | First-run consent -> `token.json` created | P0 | ⬜ | `<TBD>` | Token generated |
| T8.93 | Token-expiry recovery (delete -> re-consent) | P0 | ⬜ | `<TBD>` | Path tested |
| T8.94 | Handle 'unverified app' warning (test user) | P1 | ⬜ | `<TBD>` | Flow proceeds |
| T8.95 | Build internal-game JSON report | P0 | ✅ | `<TBD>` | Matches schema |
| T8.96 | Build inter-group bonus JSON report | P1 | ✅ | `<TBD>` | Matches schema |
| T8.97 | Validate JSON against schema before send | P1 | ⬜ | `<TBD>` | Validation passes |
| T8.98 | Email body is JSON-only (no free text) | P0 | ✅ | `<TBD>` | Machine-parseable |
| T8.99 | Recipient from config (dev sharbelma3@gmail.com) | P0 | ⬜ | `<TBD>` | Config-driven |
| T8.100 | send_email performs real SEND (not draft) | P0 | ⬜ | `<TBD>` | Email received |
| T8.101 | End-to-end: 6 games -> report email sent | P0 | ⬜ | `<TBD>` | One email delivered |
| T8.102 | Demo read_emails -> extract_meeting -> add_calendar_event | P0 | ⬜ | `<TBD>` | Event from email |
| T8.103 | Technical-loss requeue reflected in totals | P1 | ⬜ | `<TBD>` | 6 completed games |
| T8.104 | Flip recipient to rmisegal+uoh26b@gmail.com (verbatim) at submission | P0 | ⬜ | `<TBD>` | Config-only; tag kept |

## Phase 9 — Gatekeeper, quality gates, research & submission (Milestone: M9)
_Cross-cutting infra, quality gates, research/visualization, final checklist & submission._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T9.1 | Spec & single-concern interface for `shared/gatekeeper.py` — centralized API gatekeeper (rate-limit/queue/retry/log) | P0 | ✅ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T9.2 | Define typed models/signatures for `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | Typed inputs/outputs defined (`RateLimitConfig`, `QueueStatus`) |
| T9.3 | RED: write failing unit tests for `shared/gatekeeper.py` (happy path) | P0 | ✅ | `<TBD>` | Failing tests committed |
| T9.4 | GREEN: implement `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | Happy-path tests pass |
| T9.5 | Edge-case & boundary tests for `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | Overflow/backpressure/exhausted-retry/concurrency covered |
| T9.6 | Defensive error handling in `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | Graceful failure + clear message; never rejects/crashes |
| T9.7 | Refactor `shared/gatekeeper.py`: DRY, ≤150 lines, single responsibility | P0 | ✅ | `<TBD>` | 137 code LOC; limiter split to `rate_limit.py` |
| T9.8 | Docstrings + why-comments for `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | Module/functions documented |
| T9.9 | Ruff clean `shared/gatekeeper.py` | P0 | ✅ | `<TBD>` | 0 ruff violations |
| T9.10 | Mock external deps in `shared/gatekeeper.py` tests | P0 | ✅ | `<TBD>` | Injected fake clock/sleep; no live external calls |
| T9.11 | Coverage ≥85% for `shared/gatekeeper.py` + add README Work Log row | P0 | ✅ | `<TBD>` | 100% coverage; Work Log updated |
| T9.12 | Spec & single-concern interface for `shared/config.py` — config loader + version validation | P0 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T9.13 | Define typed models/signatures for `shared/config.py` | P0 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T9.14 | RED: write failing unit tests for `shared/config.py` (happy path) | P0 | ⬜ | `<TBD>` | Failing tests committed |
| T9.15 | GREEN: implement `shared/config.py` | P0 | ⬜ | `<TBD>` | Happy-path tests pass |
| T9.16 | Edge-case & boundary tests for `shared/config.py` | P0 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T9.17 | Defensive error handling in `shared/config.py` | P0 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T9.18 | Refactor `shared/config.py`: DRY, ≤150 lines, single responsibility | P0 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T9.19 | Docstrings + why-comments for `shared/config.py` | P0 | ⬜ | `<TBD>` | Module/functions documented |
| T9.20 | Ruff clean `shared/config.py` | P0 | ⬜ | `<TBD>` | 0 ruff violations |
| T9.21 | Mock external deps in `shared/config.py` tests | P0 | ⬜ | `<TBD>` | No live external calls |
| T9.22 | Coverage ≥85% for `shared/config.py` + add README Work Log row | P0 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T9.23 | Spec & single-concern interface for `shared/version_check.py` — runtime config-version validation | P1 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T9.24 | Define typed models/signatures for `shared/version_check.py` | P1 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T9.25 | RED: write failing unit tests for `shared/version_check.py` (happy path) | P1 | ⬜ | `<TBD>` | Failing tests committed |
| T9.26 | GREEN: implement `shared/version_check.py` | P1 | ⬜ | `<TBD>` | Happy-path tests pass |
| T9.27 | Edge-case & boundary tests for `shared/version_check.py` | P1 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T9.28 | Defensive error handling in `shared/version_check.py` | P1 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T9.29 | Refactor `shared/version_check.py`: DRY, ≤150 lines, single responsibility | P1 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T9.30 | Docstrings + why-comments for `shared/version_check.py` | P1 | ⬜ | `<TBD>` | Module/functions documented |
| T9.31 | Ruff clean `shared/version_check.py` | P1 | ⬜ | `<TBD>` | 0 ruff violations |
| T9.32 | Mock external deps in `shared/version_check.py` tests | P1 | ⬜ | `<TBD>` | No live external calls |
| T9.33 | Coverage ≥85% for `shared/version_check.py` + add README Work Log row | P1 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T9.34 | Spec & single-concern interface for `shared/logging_setup.py` — structured logging from config | P1 | ⬜ | `<TBD>` | Interface + docstring agreed; ≤150-LOC plan |
| T9.35 | Define typed models/signatures for `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | Typed inputs/outputs defined |
| T9.36 | RED: write failing unit tests for `shared/logging_setup.py` (happy path) | P1 | ⬜ | `<TBD>` | Failing tests committed |
| T9.37 | GREEN: implement `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | Happy-path tests pass |
| T9.38 | Edge-case & boundary tests for `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | Empty/invalid/limit inputs covered |
| T9.39 | Defensive error handling in `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | Graceful failure + clear message |
| T9.40 | Refactor `shared/logging_setup.py`: DRY, ≤150 lines, single responsibility | P1 | ⬜ | `<TBD>` | No duplication; ≤150 LOC |
| T9.41 | Docstrings + why-comments for `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | Module/functions documented |
| T9.42 | Ruff clean `shared/logging_setup.py` | P1 | ⬜ | `<TBD>` | 0 ruff violations |
| T9.43 | Mock external deps in `shared/logging_setup.py` tests | P1 | ⬜ | `<TBD>` | No live external calls |
| T9.44 | Coverage ≥85% for `shared/logging_setup.py` + add README Work Log row | P1 | ⬜ | `<TBD>` | ≥85% coverage; Work Log updated |
| T9.45 | All external calls routed through gatekeeper (audit) | P0 | 🟦 | `<TBD>` | LLM gatekept (`GatekeptLLM`); Gmail/Calendar wrapping ready, wired at OAuth time (Phase 8) |
| T9.46 | FIFO queue on overflow (no reject/crash) | P0 | ✅ | `<TBD>` | Ticket-gated FIFO; queued + drained on window reset (`test_overflow_is_queued_and_drained_not_rejected`) |
| T9.47 | Backpressure alert when queue full | P1 | ✅ | `<TBD>` | `get_queue_status().backpressure` + logged event |
| T9.48 | Retry transient failures up to max_retries | P0 | ✅ | `<TBD>` | Backoff `retry_after_seconds` honoured (`test_backoff_sleeps_retry_after_between_attempts`) |
| T9.49 | Enforce concurrent_max + thread-safety (locks) | P1 | ✅ | `<TBD>` | `BoundedSemaphore` + single `RLock`; no lost increments under 25-thread load |
| T9.50 | Rate limits read from rate_limits.json (versioned) | P0 | ✅ | `<TBD>` | `gatekeeper_from_config`; no hardcoded limits |
| T9.51 | Coverage gate >=85% passes | P0 | ⬜ | `<TBD>` | fail_under met |
| T9.52 | Ruff zero violations across repo | P0 | ⬜ | `<TBD>` | Clean |
| T9.53 | File-size <=150 LOC check (all code files) | P1 | ⬜ | `<TBD>` | None exceed |
| T9.54 | Docstrings on modules/classes/functions | P1 | ⬜ | `<TBD>` | Documented |
| T9.55 | Secret scan clean; `.env-example` present | P0 | ⬜ | `<TBD>` | No secrets |
| T9.56 | `pyproject.toml` single source of deps | P0 | ⬜ | `<TBD>` | No requirements.txt |
| T9.57 | `uv.lock` committed; tools via `uv run` | P0 | ⬜ | `<TBD>` | No pip/python -m |
| T9.58 | Package `__init__` exports + relative imports | P1 | ⬜ | `<TBD>` | No absolute paths |
| T9.59 | Enums for actions/events; no magic numbers | P1 | ⬜ | `<TBD>` | constants.py used |
| T9.60 | (Opt) CI runs tests + ruff | P2 | ⬜ | `<TBD>` | Pipeline green |
| T9.61 | Parameter research (grid/visibility/hyper-params) | P2 | ⬜ | `<TBD>` | Experiments logged |
| T9.62 | OAT (one-at-a-time) sensitivity analysis | P2 | ⬜ | `<TBD>` | Documented |
| T9.63 | Variance-based / partial-derivative analysis | P3 | ⬜ | `<TBD>` | Documented |
| T9.64 | Results analysis notebook (Jupyter) with LaTeX | P2 | ⬜ | `<TBD>` | Notebook in notebooks/ |
| T9.65 | Bar chart (comparisons) | P2 | ⬜ | `<TBD>` | In assets/ |
| T9.66 | Line chart (trends / learning curve) | P2 | ⬜ | `<TBD>` | In assets/ |
| T9.67 | Scatter plot (correlations) | P3 | ⬜ | `<TBD>` | In assets/ |
| T9.68 | Heatmap (parameter sensitivity) | P2 | ⬜ | `<TBD>` | In assets/ |
| T9.69 | Box plot (distributions) | P3 | ⬜ | `<TBD>` | In assets/ |
| T9.70 | Waterfall chart (variance analysis) | P3 | ⬜ | `<TBD>` | In assets/ |
| T9.71 | Token-cost analysis table | P2 | ✅ | `<TBD>` | README R.7 filled from `scripts/token_report.py` (3046 in / 264 out / $0.000615 per match) |
| T9.72 | Maintain prompt-engineering log | P1 | 🟦 | `<TBD>` | PROMPT_LOG.md / README R.8 |
| T9.73 | ISO/IEC 25010 self-assessment | P2 | ⬜ | `<TBD>` | Documented |
| T9.74 | Dec-POMDP formalization in README | P0 | ⬜ | `<TBD>` | Tuple + spaces defined |
| T9.75 | Communication-challenge analysis in README | P0 | ⬜ | `<TBD>` | Written |
| T9.76 | Clean git history / meaningful commits | P1 | ⬜ | `<TBD>` | Reviewed |
| T9.77 | LICENSE + third-party attribution | P1 | ⬜ | `<TBD>` | Present |
| T9.78 | Package-organization checklist (PRD section 14) | P1 | ⬜ | `<TBD>` | Passed |
| T9.79 | Continuous README Work Log per task | P0 | 🟦 | `<TBD>` | Row added each task |
| T9.80 | Final checklist (guidelines section 17) pass | P0 | ⬜ | `<TBD>` | All items checked |
| T9.81 | Final checklist (guidelines section 20.9) pass | P0 | ⬜ | `<TBD>` | All items checked |
| T9.82 | Prepare submission: GitHub link + 2 MCP URLs | P0 | ⬜ | `<TBD>` | Report assembled |
| T9.83 | Send final report email to lecturer | P0 | ⬜ | `<TBD>` | Submitted |
| T9.84 | (Bonus) Inter-group series (3+3 role swap) | P3 | ⬜ | `<TBD>` | Both reports agree |
| T9.85 | (Bonus) Confirm mutual-agreement JSON match | P3 | ⬜ | `<TBD>` | Identical results |

## Phase 10 — Audit closure (requirements coverage gaps) (Milestone: M10)
_Close every gap from the 2026-06-25 multi-agent audit (see docs/AUDIT-2026-06-25.md). DONE = fixed in docs this pass; the rest are tracked for implementation._

| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T10.1 | README full Installation: sys reqs, steps, env/secret config, troubleshooting [gap1,4] | P0 | ✅ | `<TBD>` | README section 2 substantive |
| T10.2 | README Usage: run modes/flags + worked example [gap7,8,19,20] | P0 | ✅ | `<TBD>` | README section 3 substantive |
| T10.3 | README Configuration Guide table of keys+effects [gap9,21] | P0 | ✅ | `<TBD>` | README section 5 |
| T10.4 | README Dec-POMDP formalization R.2 [gap5,6] | P0 | ✅ | `<TBD>` | Tuple per-element defined |
| T10.5 | README token-cost table skeleton R.7 [gap26] | P1 | ✅ | `<TBD>` | Table present |
| T10.6 | LICENSE file + README License/Credits [gap22,32] | P1 | ✅ | `<TBD>` | MIT LICENSE; credits listed |
| T10.7 | Preserve audit findings in repo [meta] | P1 | ✅ | `<TBD>` | docs/AUDIT-2026-06-25.md |
| T10.8 | Automated test report (junit-xml + HTML coverage) + save success/fail run logs to results/ [gap2,25,C10] | P0 | ⬜ | `<TBD>` | Report + logs artifacts |
| T10.9 | Document expected results per test [gap2] | P1 | ⬜ | `<TBD>` | Expected outcomes recorded |
| T10.10 | Enable branch coverage (branch=true, --cov-branch) in pyproject [gap24] | P0 | 🟦 | `<TBD>` | CLAUDE/PLAN updated; configure in pyproject |
| T10.11 | Tiered coverage: critical modules >=95% [gap23] | P1 | 🟦 | `<TBD>` | CLAUDE rule added; tag tasks |
| T10.12 | Exact ruff: target-version py310 + ignore E501 [gap35,36] | P1 | ✅ | `<TBD>` | CLAUDE updated; mirror in pyproject |
| T10.13 | Exact coverage omit block in pyproject [gap34] | P2 | ⬜ | `<TBD>` | source=src; omit gui/main/tests |
| T10.14 | docs/EDGE_CASES.md register (boundary|input|expected) [gap11] | P1 | ⬜ | `<TBD>` | Edge-case table per module |
| T10.15 | Capture fault screenshots for edge cases once code exists [gap11,C10] | P2 | ⬜ | `<TBD>` | In README R.4/R.5 |
| T10.16 | __init__.py in every sub-package (services/mcp/shared/strategy/google_agent/nl_protocol/gui/tests) [gap16] | P1 | ⬜ | `<TBD>` | All dirs have __init__ |
| T10.17 | pyproject [project]: name,version,description,authors,license,deps (6 fields) [gap52] | P1 | ⬜ | `<TBD>` | All fields present |
| T10.18 | Relative file I/O for in-repo paths; secrets_dir sole external [gap53,C21] | P1 | ⬜ | `<TBD>` | No absolute in-repo paths |
| T10.19 | Per-environment config templates (.env.dev/.env.prod) [gap60] | P2 | ⬜ | `<TBD>` | Templates shipped |
| T10.20 | Pin Google client lib versions in pyproject (version churn) [C26] | P2 | ⬜ | `<TBD>` | Versions pinned |
| T10.21 | Thread-safety: deadlock avoidance + context managers + queue.Queue [gap17] | P1 | ✅ | `<TBD>` | Single `RLock` (consistent order ⇒ no deadlock) + `with` blocks + `deque` FIFO; noted in PRD_gatekeeper §6 |
| T10.22 | Classify ops I/O vs CPU-bound; threads for I/O, no CPU hot path [gap54,55,56] | P2 | ✅ | `<TBD>` | Rationale in PRD_gatekeeper §6 (LLM/Gmail are I/O-bound → threads) |
| T10.23 | Notebook includes LaTeX + academic references [gap12] | P2 | ⬜ | `<TBD>` | Bibliography present |
| T10.24 | Graph quality 5-part (labels,legend,colors,caption,>=150dpi) [gap13] | P2 | ⬜ | `<TBD>` | DoD on viz tasks |
| T10.25 | Name viz stack (Matplotlib/Seaborn/Plotly) + add deps [gap42] | P2 | ⬜ | `<TBD>` | Deps added |
| T10.26 | Budget mgmt: forecast + real-time spend counter + overrun alert [gap14,C20] | P2 | 🟦 | `<TBD>` | Forecast + token-cost util (`token_cost.py`) + design in README R.7; live gatekeeper spend counter/alert pending |
| T10.27 | Usability NFR + Nielsen 10 heuristics mapping + accessibility [gap15,43,44,46,47,C8] | P1 | ⬜ | `<TBD>` | PRD NFR + README UI section |
| T10.28 | User-workflow + interactions/feedback documentation [gap45] | P2 | ⬜ | `<TBD>` | README section 3 / PRD_ui |
| T10.29 | ISO/IEC 25010 per-characteristic self-assessment table [gap50,51] | P2 | ⬜ | `<TBD>` | 8-char mapping |
| T10.30 | Standards alignment: cite all five (ISO,MIT SQA,Google,MS,Nielsen) [gap59] | P2 | 🟦 | `<TBD>` | README section 4 note; expand |
| T10.31 | Extension points/plugin architecture + lifecycle hooks + worked example [gap48,49,58,C11] | P2 | ⬜ | `<TBD>` | PLAN section + example |
| T10.32 | C4 Level-4 (Code) view + labeled deployment diagram [C22] | P2 | ⬜ | `<TBD>` | Diagrams in assets/ |
| T10.33 | Building-block contract: Input/Output/Setup + DI testability [C9] | P2 | ⬜ | `<TBD>` | Contract documented |
| T10.34 | Production secret-management note (Vault/Secrets Manager) [gap37] | P3 | ⬜ | `<TBD>` | PLAN section 3 note |
| T10.35 | Adopt PR-based review + feature branches + version tags [gap38,39,40,C23] | P2 | 🟦 | `<TBD>` | CLAUDE git workflow; practice it |
| T10.36 | Match role structure: 3 cop + 3 thief per internal match; per-subgame role config [C1] CONFIRM w/ staff | P0 | 🟦 | `<TBD>` | PRD note added; engine support + confirm |
| T10.37 | Non-square sanity grids 3x2 and 4x3 [gap61,C6] | P1 | ⬜ | `<TBD>` | Sweeps include non-square |
| T10.38 | Sanity-stage goals (msg-transmission/coordination/ambiguity/analysis) [C7] | P2 | ⬜ | `<TBD>` | Per-stage objective |
| T10.39 | Strategic (non-random) start-position option [C16] | P3 | ⬜ | `<TBD>` | Config/strategy choice |
| T10.40 | Clarify special-action generality vs barrier [C14] | P3 | ⬜ | `<TBD>` | Documented |
| T10.41 | Local-phase MCP transport avoids stdio pipe errors (use HTTP ports) [C15] | P2 | ⬜ | `<TBD>` | No pipe errors |
| T10.42 | Bonus scoring math: 10/5/5 + average across series + multi-group [gap62,63,C5] | P3 | ⬜ | `<TBD>` | PRD_email_reporting section 4 |
| T10.43 | Google: one project + two work areas + new Auth Platform + OAuth-client-id-not-API-key [gap27,28,64,65,66,C2] | P1 | ✅ | `<TBD>` | PRD note added |
| T10.44 | OAuth combined troubleshooting gate (test user+scopes+both APIs) [gap31,C3] | P1 | ✅ | `<TBD>` | PRD note added |
| T10.45 | Standalone main.py Google smoke test via uv run main.py (draft+event) [gap30,71,72,74,75] | P1 | ⬜ | `<TBD>` | Smoke test passes |
| T10.46 | End-to-end real-run check: consent no-error, real draft, real event, token.json [gap29,C13] | P1 | ⬜ | `<TBD>` | 4 checks pass |
| T10.47 | Interactive first-run vs autonomous runs reconciled [C4] | P0 | ✅ | `<TBD>` | PRD section 1.2 added |
| T10.48 | Calendar timezone Asia/Jerusalem populated + config-driven [C12,C19] | P1 | 🟦 | `<TBD>` | PRD note; implement |
| T10.49 | MCP token encryption + revocation (not just auth) [C18] | P2 | ⬜ | `<TBD>` | Encrypt + revoke |
| T10.50 | Tunneling specifics: ngrok ollama.yaml+Authz, Localtonet, Nginx htpasswd+SSL [C17] | P3 | ⬜ | `<TBD>` | Documented |
| T10.51 | Test-users 100 cap + unverified-mode short token TTL note [C25] | P3 | ⬜ | `<TBD>` | Documented |
| T10.52 | Google snake_case naming (project/app/client, unique number) [C24] | P3 | ✅ | `<TBD>` | PRD note added |
| T10.53 | Optional Gmail test label 0-bio [gap76] | P3 | ⬜ | `<TBD>` | Optional note |
| T10.54 | PRD section 1.5 Market/landscape analysis [gap10,18] | P2 | ⬜ | `<TBD>` | Subsection added |

