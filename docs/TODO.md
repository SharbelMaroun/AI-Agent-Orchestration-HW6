# TODO — Task Tracking

**Project:** Dual AI Agent Race via MCP Servers — "Cop & Thief"
**Document version:** 1.00
**Governing standard:** [`../MATERIALS/software_submission_guidelines-V3_Summary.md`](../MATERIALS/software_submission_guidelines-V3_Summary.md)

**Legend — Status:** ⬜ Not Started · 🟦 In Progress · ✅ Completed
**Priority:** P0 (critical) · P1 (high) · P2 (medium) · P3 (low)

> Update this file continuously as work progresses (mandated by the guidelines).
> Each task lists its **Definition of Done (DoD)**. Owner placeholders: `<TBD>`.

---

## Phase 0 — Project setup & documentation (Milestone: M0)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T0.1 | Author `docs/PRD.md`, `PLAN.md`, `TODO.md` | P0 | ✅ | `<TBD>` | Three docs exist, reviewed, version 1.00 |
| T0.2 | Author specialized PRDs (game/mcp/nl/strategy/gatekeeper/email) | P0 | ✅ | `<TBD>` | One PRD per central mechanism |
| T0.3 | Get all docs **approved** before coding | P0 | ⬜ | `<TBD>` | Sign-off recorded here |
| T0.4 | Init `uv` project: `pyproject.toml`, `uv.lock`, `src/` package | P0 | ⬜ | `<TBD>` | `uv sync` works; package imports |
| T0.5 | Add `.gitignore`, `.env-example`, Ruff & coverage config | P0 | ⬜ | `<TBD>` | `.env`, `client_secret.json`, `token.json` ignored; Ruff/pytest configured |
| T0.6 | Create `config/config.json` (+ `rate_limits.json`) with `version` 1.00 | P0 | ⬜ | `<TBD>` | Params load (incl. `reporting`/`google` blocks); version validated at runtime |

## Phase 1 — Game logic & rules engine (Milestone: M1) — *do first* 
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T1.1 | `board.py`: grid, cells, 8-dir neighbours, barriers, bounds | P0 | ⬜ | `<TBD>` | Unit-tested; illegal cells rejected |
| T1.2 | `game_engine.py`: state machine, legality, capture detection | P0 | ⬜ | `<TBD>` | Capture & survival outcomes correct |
| T1.3 | Barrier rules: cop-only, ≤5/game, square impassable | P0 | ⬜ | `<TBD>` | Tests for limit & impassability |
| T1.4 | `scoring.py`: per-subgame + match accumulation (config-driven) | P0 | ⬜ | `<TBD>` | 30–90 range verified |
| T1.5 | `models.py`: Position/Action/Message/GameState/Result | P1 | ⬜ | `<TBD>` | Typed, validated, ≤150 lines |
| Ref | See [`PRD_game_engine.md`](PRD_game_engine.md) | — | — | — | — |

## Phase 2 — MCP communication infrastructure (Milestone: M2)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T2.1 | `mcp/tools.py`: tool contracts (send/recv/observe/submit/verify/status) | P0 | ⬜ | `<TBD>` | Schemas defined & documented |
| T2.2 | `cop_server.py` / `thief_server.py` (FastMCP), distinct ports | P0 | ⬜ | `<TBD>` | Both servers start locally |
| T2.3 | Mutual location verification + message passing | P0 | ⬜ | `<TBD>` | Round-trip message exchange works |
| Ref | See [`PRD_mcp_server.md`](PRD_mcp_server.md) | — | — | — | — |

## Phase 3 — Full local autonomous match (Milestone: M3)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T3.1 | `orchestrator.py`: match loop (6 sub-games, ≤25 moves) | P0 | ⬜ | `<TBD>` | Runs end-to-end on localhost |
| T3.2 | Technical-loss detection + re-run to fill quota of 6 | P1 | ⬜ | `<TBD>` | Failed game auto re-run |
| T3.3 | `sdk/sdk.py`: single public entry point | P0 | ⬜ | `<TBD>` | GUI/CLI/tests call SDK only |
| T3.4 | Integration test: full local match | P0 | ⬜ | `<TBD>` | Deterministic seeded test passes |

## Phase 4 — Decision strategy (Milestone: M4)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T4.1 | `strategy/heuristic.py`: default cop/thief policies | P0 | ⬜ | `<TBD>` | Beats random baseline in tests |
| T4.2 | Belief model over opponent position (partial obs) | P1 | ⬜ | `<TBD>` | Belief updates from observation+message |
| T4.3 | *(Optional)* `strategy/q_table.py`: Bellman update + ε-greedy | P3 | ⬜ | `<TBD>` | Learning curve produced |
| Ref | See [`PRD_decision_strategy.md`](PRD_decision_strategy.md) | — | — | — | — |

## Phase 5 — Natural-language integration (Milestone: M5)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T5.1 | `nl_protocol.py`: intent→text + text→belief parsing | P0 | ⬜ | `<TBD>` | Never crashes on ambiguous text |
| T5.2 | `llm_client.py`: LLM calls **via gatekeeper** | P0 | ⬜ | `<TBD>` | Mockable; logged; retried |
| T5.3 | Deception/ambiguity handling + prompt templates | P1 | ⬜ | `<TBD>` | Documented prompts; tested |
| Ref | See [`PRD_nl_communication.md`](PRD_nl_communication.md) | — | — | — | — |

## Phase 6 — GUI & CLI (Milestone: M6)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T6.1 | Real-time GUI of agents + barriers | P1 | ⬜ | `<TBD>` | Renders state from SDK; screenshots saved |
| T6.2 | CLI runner with structured logs of MCP communication | P1 | ⬜ | `<TBD>` | Logs prove valid cloud comms |

## Phase 7 — Cloud deployment (Milestone: M7)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T7.1 | Deploy Cop & Thief MCP servers to cloud (e.g., Prefect) | P0 | ⬜ | `<TBD>` | Two public URLs reachable |
| T7.2 | Token-based auth + revocation on both URLs | P0 | ⬜ | `<TBD>` | Unauthorized access rejected |
| T7.3 | Firewall/port/tunneling notes in README | P1 | ⬜ | `<TBD>` | Documented & reproducible |

## Phase 8 — Gmail/Calendar agent, reporting & scientific README (Milestone: M8)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T8.1 | Google OAuth Desktop client; enable **Gmail + Calendar API**; scopes; test user | P0 | ⬜ | `<TBD>` | `token.json` generated; both APIs enabled |
| T8.2 | `google_auth.py`: token load/refresh + **expiry re-consent recovery**; secrets in external folder | P0 | ⬜ | `<TBD>` | Delete-token → re-consent path tested |
| T8.3 | `email_reader.py` → `read_emails()` (via gatekeeper) | P0 | ⬜ | `<TBD>` | Returns inbox messages; Gmail mocked in tests |
| T8.4 | `meeting_extractor.py` → `extract_meeting()` (LLM-assisted) | P0 | ⬜ | `<TBD>` | Correct meeting / `None` on non-invite, no crash |
| T8.5 | `calendar_writer.py` → `add_calendar_event()` | P0 | ⬜ | `<TBD>` | Event start matches extracted time |
| T8.6 | `gmail_client.send_email()`: real send (not draft) to `reporting.recipient_email` | P0 | ⬜ | `<TBD>` | Email sent to `sharbelma3@gmail.com` (dev) |
| T8.7 | `reporting.py`: build JSON + send via `send_email` (gatekeeper) | P0 | ⬜ | `<TBD>` | JSON-only email delivered |
| T8.8 | Internal + inter-group JSON schemas | P1 | ⬜ | `<TBD>` | Matches spec; validated |
| T8.9 | Flip `recipient_email` → `rmisegal+uoh26b@gmail.com` (verbatim) **at submission** | P0 | ⬜ | `<TBD>` | Config-only change; tag kept |
| T8.10 | Scientific `README.md` (Dec-POMDP, comms analysis, screenshots, logs) | P0 | 🟦 | `<TBD>` | Skeleton + Report/Results section created; fill all required sections |
| Ref | See [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md), [`PRD_email_reporting.md`](PRD_email_reporting.md) | — | — | — | — |

## Phase 9 — Quality gates & submission (cross-cutting)
| ID | Task | Pri | Status | Owner | DoD |
|----|------|-----|--------|-------|-----|
| T9.1 | All external calls via gatekeeper (rate limit + queue + log) | P0 | ⬜ | `<TBD>` | No direct API calls in code |
| T9.2 | ≥85% test coverage; coverage gate enforced | P0 | ⬜ | `<TBD>` | `fail_under=85` passes |
| T9.3 | Ruff zero violations | P0 | ⬜ | `<TBD>` | `uv run ruff check` clean |
| T9.4 | All files ≤150 lines; docstrings present | P1 | ⬜ | `<TBD>` | Verified |
| T9.5 | No secrets; `.env-example` present; `.gitignore` complete | P0 | ⬜ | `<TBD>` | Secret scan clean |
| T9.6 | Parameter/sensitivity research + visualizations notebook | P2 | ⬜ | `<TBD>` | `notebooks/` analysis with graphs |
| T9.7 | Prompt-engineering log + token-cost analysis | P2 | ⬜ | `<TBD>` | Documented |
| T9.8 | *(Optional bonus)* inter-group match + matching JSON reports | P3 | ⬜ | `<TBD>` | Both reports agree |
| T9.9 | **Report everything continuously** in `README.md` Report/Results (work log + graphs + screenshots) | P0 | 🟦 | `<TBD>` | A Work Log row + evidence added per task; images in `assets/`/`results/` |

---

## Milestone summary
| Milestone | Phase | Gate |
|---|---|---|
| M0 | 0 | Docs approved |
| M1 | 1 | Rules engine tested |
| M2 | 2 | Dual MCP servers local |
| M3 | 3 | Autonomous local match |
| M4 | 4 | Strategy beats baseline |
| M5 | 5 | NL comms robust |
| M6 | 6 | GUI + CLI logs |
| M7 | 7 | Cloud + auth |
| M8 | 8 | Report + README |
