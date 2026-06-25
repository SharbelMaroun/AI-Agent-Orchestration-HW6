# Product Requirements Document (PRD)

**Project:** Dual AI Agent Race via MCP Servers — "Cop & Thief" Pursuit Game
**Course:** Orchestration of AI Agents — University of Haifa, Dept. of Computer Science
**Assignment:** Task 6 (ex06)
**Document version:** 1.00
**Status:** Draft — pending approval
**Owner:** `<TBD: team lead>`

> This PRD is the central requirements document for the project. It is governed by the
> engineering standards in [`../MATERIALS/software_submission_guidelines-V3_Summary.md`](../MATERIALS/software_submission_guidelines-V3_Summary.md)
> and derives its functional scope from [`../MATERIALS/ex06-Dual AI agent race via MCP servers_Summary.md`](../MATERIALS/ex06-Dual%20AI%20agent%20race%20via%20MCP%20servers_Summary.md).

---

## 1. Project Overview & Context

### 1.1 Summary
Build a fully autonomous, end-to-end system in which **two AI agents — a Cop and a Thief —**
play a pursuit game on a 2-D grid. Each agent is backed by its **own MCP (Model Context Protocol)
server**. The agents do **not** exchange raw coordinates; they communicate in **natural language**,
infer the opponent's position under **partial observation**, and translate inferences into grid
moves. The full match (6 sub-games) runs without manual intervention, from initialization to the
final automated email report.

The project also includes a **Gmail & Calendar agent** that acts on a real Google account — it can
**read the inbox, extract a meeting invitation, add it to Google Calendar, and send email**. When the
match finishes, the orchestrator uses this agent's `send_email` to deliver the JSON result. The game
and the Gmail/Calendar agent share one Google credential and one recipient mailbox but are otherwise
independent capabilities. See [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md).

### 1.2 The problem
Single-agent reasoning in a static, fully-observed environment does not transfer to real
multi-agent systems, where autonomous entities must make real-time decisions while coordinating
through imperfect, free-text communication. This project moves the team from single-agent thinking
to **distributed multi-agent orchestration** under uncertainty.

### 1.3 Target audience
- **Primary:** Course staff (Dr. Yoram Segal) evaluating orchestration capability.
- **Secondary:** Other student groups (for the optional inter-group bonus competition).
- **Tertiary:** Future maintainers/learners reading the scientific README.

### 1.4 What is explicitly NOT the goal
The success metric is **communication & orchestration quality**, not winning strategy or RL
sophistication. Reinforcement learning is **optional enrichment**, not a requirement.

---

## 2. Goals, KPIs & Acceptance Criteria

### 2.1 Measurable goals
| # | Goal | Metric | Target |
|---|------|--------|--------|
| G1 | Autonomous full match | Manual interventions during a 6-sub-game run | **0** |
| G2 | NL communication | Turns where a message is parsed into a valid intent | **100%** (no crash on ambiguity) |
| G3 | Correct rules engine | Illegal moves accepted by engine | **0** |
| G4 | Dual MCP servers | Independent Cop & Thief MCP servers reachable | **2/2** |
| G5 | Cloud deployment | Public, authenticated MCP URLs (cop + thief) | **2 URLs**, token-secured |
| G6 | Automated reporting | JSON-only report email delivered after 6 games | **1 email**, machine-parseable |
| G7 | Engineering quality | Ruff violations / test coverage | **0 / ≥85%** |
| G8 | Gmail/Calendar agent | read → extract meeting → add Calendar event → send, autonomously | **4/4 tools working** |

### 2.2 Acceptance criteria (Definition of Done for the product)
- A single command launches a complete match: 6 sub-games, ≤25 moves each, scored and accumulated.
- All board/scoring parameters are read from `config/config.json` (nothing hard-coded).
- Cop and Thief each run as a separate FastMCP server; the LLM lives in the **client/orchestrator**,
  never inside the MCP server.
- At match end, a **JSON-only** email (no free text) is sent to the configured
  `reporting.recipient_email` (dev: `sharbelma3@gmail.com`; submission: `rmisegal+uoh26b@gmail.com`
  verbatim) via the Gmail API using token-based auth.
- The **Gmail & Calendar agent** can read the inbox, extract a meeting invite, add a Calendar event,
  and send email; all Google API calls route through the gatekeeper.
- Repository satisfies the submission guidelines (docs-first, SDK architecture, gatekeeper,
  ≤150-line files, ≥85% coverage, Ruff clean, `uv`-managed, `.env-example`, no secrets).
- Scientific `README.md` includes the Dec-POMDP formalization, communication analysis, GUI
  screenshots, and CLI logs.

---

## 3. Functional Requirements

### FR-1 — Game rules engine
- 2-D grid, default **5×5**, size configurable via `config.json`.
- Movement in **8 directions** (orthogonal + diagonal); one move per turn.
- Turn order: thief moves first, then cop, alternating.
- **Cop win:** cop lands on the thief's exact square (capture).
- **Thief win:** thief survives `max_moves` (default 25) without being captured.
- **Barriers:** cop may, instead of moving, place a barrier on its current square; the square
  becomes impassable to both agents. Max **5 barriers/game**. Thief cannot place barriers.
- The engine is a **state machine**; state advances every turn.

### FR-2 — Match structure
- **Sub-game:** one pursuit round, ≤25 moves.
- **Game/Match:** a sequence of **6** consecutive sub-games; results accumulate and report together.
- A sub-game ending by technical failure is a **technical loss** → must be re-run to complete the quota of 6.

### FR-3 — Scoring (per sub-game, from config)
| Outcome | Cop | Thief |
|---|---|---|
| Cop wins | 20 | 5 |
| Thief wins | 5 | 10 |

Match range: **30–90** points per group.

### FR-4 — Partial observation
- Each agent observes only a limited view (e.g., a visibility radius) — never the full board.
- Agents must **infer** the opponent's location from natural-language messages + own observation.

### FR-5 — Natural-language communication
- Each turn, the active agent emits a free-text message (intention, observation, or deception).
- The recipient uses MCP **tools** to read the message, interpret it via the LLM, update its belief,
  and choose its next action. No fixed/rigid coordinate protocol.

### FR-6 — Dual MCP servers (FastMCP)
- One MCP server for the Cop, one for the Thief.
- Servers expose **tools** (send/receive message, verify location, submit move, etc.), **not** the LLM.

### FR-7 — LLM connectivity (one of three approaches)
1. **Cloud API** (recommended): client → provider API (Anthropic/OpenAI/Gemini) via API key.
2. **Local Ollama, securely tunneled** (ngrok Traffic Policy / Localtonet / Nginx reverse proxy).
3. **Hybrid:** LLM + client local, only MCP server in cloud (outbound-only requests).

### FR-8 — Deployment
- Phase 1: both servers on `localhost`, distinct ports, full local pipeline.
- Phase 2: deploy MCP servers to a public cloud (e.g., Prefect Cloud) with token-based auth & revocation.

### FR-9 — Automated reporting
- After 6 games, trigger an automated **Gmail API** send to `reporting.recipient_email`
  (dev default `sharbelma3@gmail.com`; submission `rmisegal+uoh26b@gmail.com`, tag kept verbatim).
- Email body contains **only** the JSON report (internal or inter-group schema). Token-based auth.

### FR-13 — Gmail & Calendar agent
- `read_emails()` — scan the Gmail inbox and return messages.
- `extract_meeting()` — find a meeting invitation + its time inside an email (LLM-assisted, via gatekeeper).
- `add_calendar_event()` — create the extracted meeting on Google Calendar.
- `send_email()` — actually **send** mail (not just draft); used for the end-of-match report.
- Requires Gmail **read + send** and **Calendar** scopes; `client_secret.json`/`token.json` kept in a
  secret folder **outside the repo**, with a token-expiry re-consent recovery path.
  See [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md).

### FR-10 — Configuration
- `config/config.json` includes at minimum: `version`, `grid_size`, `max_moves`, `num_games`,
  `max_barriers`, `visibility_radius`, `seed`, `scoring.{cop_win, thief_win, cop_loss, thief_loss}`,
  `strategy.type` (cop policy), `llm.{model, pricing.*}` (token-cost report), and `reporting.*` /
  `google.*` settings. Gatekeeper limits live in `config/rate_limits.json` (`rate_limits.services.*`).
  Full schema in [`PLAN.md`](PLAN.md) §5.1 and the README §5 configuration table.

### FR-11 — GUI & CLI
- GUI visualizes agent and barrier movement in real time: a **live interactive window** (`--live`) renders
  each turn the instant the engine computes it (so an NL match advances as each LLM call returns), plus an
  **animated GIF** (`--gui`) for headless/report use. Both render from SDK frame streams only (no logic in GUI).
- CLI demonstrates valid communication with the cloud MCP server (loggable).

### FR-12 — Decision strategy
- A heuristic / decision-tree / prompt-engineering strategy is sufficient. The cop policy is
  config-selectable via `strategy.type`: `"heuristic"` (greedy Chebyshev pursuit) or the delivered
  `"smart"` cornering cop (one-ply look-ahead that herds the thief; ~100% capture — Phase 4,
  `src/marl_cop_thief/services/strategy/smart_cop.py`).
- Optional Tabular Q-Learning (Bellman update, `strategy.type: "q_table"`) for academic enrichment.

---

## 4. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-1 | Reliability | A full match completes without manual intervention; technical losses are detected and re-run. |
| NFR-2 | Security | Token-based auth on MCP servers & Gmail; no secrets in code; `.env` git-ignored. |
| NFR-3 | Configurability | Grid size, moves, scoring, rate limits all config-driven. |
| NFR-4 | Maintainability | SDK architecture, OOP/DRY, files ≤150 lines, docstrings. |
| NFR-5 | Testability | TDD, ≥85% coverage, external deps mocked. |
| NFR-6 | Performance | Low-latency LLM calls; gatekeeper rate-limits & queues to avoid provider throttling. |
| NFR-7 | Portability | `uv`-managed, `pyproject.toml` + `uv.lock`, relative imports, runs on Win/macOS/Linux. |
| NFR-8 | Observability | All external API calls logged through the gatekeeper; per-game logs saved. |
| NFR-9 | Standards | ISO/IEC 25010 alignment; Ruff zero-violation. |

---

## 5. User Stories
- **US-1 (Evaluator):** As course staff, I run one command and watch two agents autonomously play
  6 games and email me a machine-readable JSON result, so I can grade orchestration objectively.
- **US-2 (Cop agent):** As the Cop, I read the Thief's messages, infer its likely cell, and move/
  place barriers to corner it, so I maximize capture probability.
- **US-3 (Thief agent):** As the Thief, I emit possibly-deceptive messages and evade, so I survive 25 moves.
- **US-4 (Developer):** As a developer, I change `grid_size` in config and re-run sanity checks
  (2×2 → 3×3 → 4×4 → 5×5) without touching code.
- **US-5 (Competitor):** As a participating group, I run a cloud match vs. another group and submit a
  matching JSON report for the bonus.

---

## 6. Assumptions, Dependencies & Out-of-Scope

### 6.1 Assumptions
- Each group has at least one usable LLM access path (cloud API key or local Ollama).
- Cloud platform (e.g., Prefect Cloud) account and a network allowing non-standard outbound ports.

### 6.2 Dependencies
- FastMCP, an LLM provider/Ollama, **Gmail API + Google Calendar API**
  (`google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`),
  a cloud host, `uv`, Ruff, pytest/pytest-cov.
  (See [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md) and [`PRD_email_reporting.md`](PRD_email_reporting.md) for Google setup.)

### 6.3 Out of scope
- Beating any specific opponent / guaranteed win rate.
- Deep RL / neural networks (tabular Q-learning is the optional ceiling).
- Persisting match history to an external database.

---

## 7. Timeline & Milestones
Aligned with the assignment's recommended development order (see [`TODO.md`](TODO.md) and
[`PLAN.md`](PLAN.md)). The inter-group bonus requires submission **within one week** of assignment
publication.

| Milestone | Deliverable |
|---|---|
| M1 | Game logic & rules engine + config |
| M2 | Dual MCP communication infrastructure (local) |
| M3 | Full local autonomous match (6 games) |
| M4 | Decision strategy (heuristic / Q-table) |
| M5 | Natural-language integration |
| M6 | GUI + CLI logs |
| M7 | Cloud deployment with auth |
| M8 | Gmail API reporting + scientific README |

---

## 8. Related specialized PRDs
- [`PRD_game_engine.md`](PRD_game_engine.md) — board, state machine, scoring, barriers.
- [`PRD_mcp_server.md`](PRD_mcp_server.md) — FastMCP dual-server design & tools.
- [`PRD_nl_communication.md`](PRD_nl_communication.md) — natural-language protocol & ambiguity handling.
- [`PRD_decision_strategy.md`](PRD_decision_strategy.md) — heuristic, config-selectable `smart` cornering cop, & optional Q-learning.
- [`PRD_gatekeeper.md`](PRD_gatekeeper.md) — centralized API gatekeeper & rate limiting.
- [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md) — Gmail/Calendar agent (read, extract, calendar, send).
- [`PRD_email_reporting.md`](PRD_email_reporting.md) — end-of-match JSON report content, schema & timing.
