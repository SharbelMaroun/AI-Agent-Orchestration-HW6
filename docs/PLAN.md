# Architecture & Design Document (PLAN)

**Project:** Dual AI Agent Race via MCP Servers — "Cop & Thief"
**Document version:** 1.00
**Status:** Draft — pending approval
**Governing standard:** [`../MATERIALS/software_submission_guidelines-V3_Summary.md`](../MATERIALS/software_submission_guidelines-V3_Summary.md)

> Companion to [`PRD.md`](PRD.md). Describes the technical architecture, decisions, data
> contracts, and deployment design.

---

## 1. C4 Model

### 1.1 Level 1 — System Context
```text
            natural-language messages (via MCP tools)
   +---------------------+        +---------------------+
   |   COP (agent side)  | <----> |  THIEF (agent side) |
   |  client + LLM +     |        |  client + LLM +     |
   |  Cop MCP server     |        |  Thief MCP server   |
   +----------+----------+        +----------+----------+
              |                              |
              +--------------+---------------+
                             v
                  +---------------------+
                  |   Course Staff      |
                  |  (Gmail JSON report)|
                  +---------------------+
```
- **Actors:** Course staff (report recipient), opponent group (bonus).
- **External systems:** LLM provider (Cloud API/Ollama), Gmail API, Cloud host (Prefect Cloud).

### 1.2 Level 2 — Containers
```text
External Consumers (GUI / CLI / Tests / Inter-group runner)
        |
        v
+--------------------------------------------------+
|  SDK  (src/marl_cop_thief/sdk/sdk.py)            |  <- single entry point for ALL logic
+--------------------------------------------------+
        |
        v
+--------------------------------------------------+
|  Domain Services                                 |
|  - Orchestrator (match/sub-game loop)            |
|  - GameEngine + Board + Scoring (state machine)  |
|  - CopAgent / ThiefAgent (belief + policy)       |
|  - NLProtocol (encode/decode free text)          |
|  - Strategy (heuristic | smart; q_table planned) |
|  - GoogleAgent (read/extract/calendar/send)      |
|  - Reporting (JSON builder -> send_email)        |
+--------------------------------------------------+
        |                         |
        v                         v
+----------------------+   +---------------------------+
| Infrastructure       |   |  MCP Layer (FastMCP)      |
| - Gatekeeper         |   |  - Cop MCP server         |
| - LLM client         |   |  - Thief MCP server       |
| - Config / Version   |   |  - Tools (send/recv/move) |
| - Google transport   |   +---------------------------+
|   (Gmail + Calendar) |
+----------------------+
```

### 1.3 Level 3 — Components (key)
- **Orchestrator** drives: init → per turn (observe → request LLM decision → tool call → apply →
  score) → end-of-subgame → accumulate → report.
- **GameEngine** owns the authoritative state; validates legality; never trusts agent input blindly.
- **Agents** hold a *belief* over opponent position; produce an outbound NL message and a chosen action.
- **NLProtocol** converts agent intent ↔ free text and parses inbound text into a structured belief update.
- **Gatekeeper** wraps every outbound API call (LLM + Gmail) with rate limiting, queueing, retries, logging.

### 1.4 Level 4 — Code
See the module layout in §4 and the per-mechanism PRDs.

---

## 2. Architectural Decision Records (ADRs)

### ADR-001 — LLM lives in the client, MCP server exposes tools only
- **Decision:** The orchestrator (client) calls the LLM; MCP servers expose tools/resources only.
- **Rationale:** Mandated by the assignment; keeps secrets out of the public server; clean separation.
- **Alternatives:** Host LLM inside the MCP server (rejected: couples secrets to public surface, violates spec).
- **Trade-off:** Extra round-trips (client↔LLM, client↔MCP) for cleaner security & portability.

### ADR-002 — Default LLM access = Cloud API (Approach 1)
- **Decision:** Use a cloud LLM API by default; support Hybrid (Approach 3) as a documented fallback.
- **Rationale:** Stable, low-latency, no inbound ports/firewall exposure; cheapest path to a working pipeline.
- **Alternatives:** Exposed local Ollama (rejected as default: cyber risk, tunneling complexity).
- **Trade-off:** Per-token cost vs. operational simplicity; the gatekeeper bounds spend & rate.

### ADR-003 — Authoritative server-side game engine
- **Decision:** The GameEngine is the single source of truth for legality, capture, and scoring;
  agents only *propose* actions.
- **Rationale:** Prevents cheating/desync; deterministic, testable rules.
- **Trade-off:** Agents cannot "force" moves; all actions validated → slightly more plumbing.

### ADR-004 — Centralized API Gatekeeper for all external calls
- **Decision:** No service calls an external API directly; everything routes through `gatekeeper.execute`.
- **Rationale:** Required by guidelines; one place for rate limits, retries, queue, logging, cost.
- **Trade-off:** Indirection; mitigated by a thin, well-tested wrapper. See [`PRD_gatekeeper.md`](PRD_gatekeeper.md).

### ADR-005 — Config-driven everything; versioned config
- **Decision:** All tunables in `config/*.json` with a `version` key validated at runtime; constants
  in `constants.py`. Version tracking starts at `1.00`.
- **Rationale:** Guidelines forbid hard-coded values; enables sanity-check sweeps (2×2→5×5) with no code change.

### ADR-006 — Natural language, not a rigid protocol
- **Decision:** Inter-agent messages are free text interpreted by the LLM; no coordinate wire-format.
- **Rationale:** Core graded capability is NL coordination under partial observation.
- **Trade-off:** Ambiguity risk → handled by belief model + defensive parsing. See [`PRD_nl_communication.md`](PRD_nl_communication.md).

### ADR-007 — Package & tooling: `uv` + `src/` layout
- **Decision:** `uv` as the only package manager/task runner; `src/marl_cop_thief/` package; Ruff; pytest-cov.
- **Rationale:** Mandated; reproducible locks; clean importable package.

### ADR-008 — Gmail/Calendar agent: config-driven recipient + external secret folder
- **Decision:** The report recipient is `reporting.recipient_email` (dev `sharbelma3@gmail.com`,
  submission `rmisegal+uoh26b@gmail.com`). `client_secret.json`/`token.json` live in a secret folder
  **outside** the repo, located via `google.secrets_dir`. The Gmail/Calendar agent uses Gmail
  read+send + Calendar scopes and a token-expiry re-consent recovery path.
- **Rationale:** No hard-coded recipient/secrets (guidelines); switching to the lecturer's address is a
  config-only change; secrets can never be committed; survives token expiry near the deadline.
- **Trade-off:** Requires a documented external path & one-time consent; mitigated by `.env-example`
  and README setup steps. See [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md).

---

## 3. Deployment Architecture

```text
        Phase 1 (local)                         Phase 2 (cloud)
  localhost:PORT_COP  (Cop MCP)          https://cop-mcp-<grp>.<cloud>   (token auth)
  localhost:PORT_THIEF(Thief MCP)        https://thief-mcp-<grp>.<cloud> (token auth)
  client + LLM local                      client + LLM local/cloud  --outbound HTTPS-->  MCP servers
```
- **Security:** token-based auth with revocation on both MCP URLs; outbound-only client requests;
  no inbound ports opened on developer machines (Hybrid). Avoid org networks that block non-standard ports.
  Token auth should also support **encryption + revocation** of MCP access tokens (assignment §6, C18).
- **Secrets:** API keys & tokens in `.env` (git-ignored); `.env-example` committed with dummy values.
  **Production:** for any real deployment, move secrets out of `.env` into a managed **secret store**
  (HashiCorp Vault or the cloud provider's Secrets Manager) — `.env` is for local/dev only (guidelines §7.4, gap37).
- **Local transport:** run the two MCP servers over **HTTP on distinct localhost ports** (not raw stdio
  pipes) during the connect-two-agents phase, to avoid stdio pipe errors (assignment Table 4 / C15).

---

## 4. Module Layout (as-built — 2026-06-25)
Reflects the actual `src/` tree. `(planned)` marks not-yet-built items.
```text
src/marl_cop_thief/
├── __init__.py                 # __all__, __version__
├── __main__.py                 # enables `python -m marl_cop_thief`
├── main.py                     # CLI: default NL run · --simple · --gui (GIF) · --live (window) -> SDK
├── sdk/sdk.py                  # single public entry point (run_match, run_nl_match)
├── services/
│   ├── orchestrator.py         # heuristic match loop
│   ├── nl_match.py             # natural-language match loop (run_nl_match)
│   ├── turn_pipeline.py        # one-turn pipeline (pluggable Decider)
│   ├── match_stream.py         # per-turn (state, caption) frame streams (live GUI + GIF)
│   ├── accumulator.py          # match summary builder
│   ├── game_engine.py          # state machine, legality, capture
│   ├── board.py                # grid, neighbours, passability
│   ├── barriers.py             # cop barrier rules
│   ├── scoring.py              # per-subgame + accumulation
│   ├── observation.py          # partial-observation snapshot
│   ├── reporting.py            # JSON report builders (internal + inter-group)
│   ├── match_reporter.py       # summary -> JSON report email (config-gated send)
│   ├── bonus.py                # inter-group bonus scoring (10/5/5 + averaging, §12.2)
│   ├── series_runner.py        # 6-game 3-cop/3-thief role-swap series -> bonus_game report
│   ├── nl_protocol/            # nl_encode, nl_decode, ambiguity_handler,
│   │                           #   prompt_templates, nl_decider
│   ├── google_agent/           # email_reader, meeting_extractor, calendar_writer (DI)
│   ├── mcp/                    # tools (ToolService, 6 tools), message_bus, servers (FastMCP)
│   └── strategy/              # heuristic.py (greedy cop+thief), smart_cop.py (cornering 1-ply),
│                              #   geometry.py (shared chebyshev); belief_model/q_table planned
├── gui/                        # theme, overlays(HUD+speech), board_renderer, match_animator(GIF), live_viewer(window); render-only, omitted from coverage
└── shared/
    ├── gatekeeper.py           # API gatekeeper (rate limit + FIFO queue + backpressure + retries + concurrency)
    ├── rate_limit.py           # RateLimitConfig, QueueStatus, SlidingWindowLimiter (config-driven)
    ├── mcp_auth.py             # TokenAuth: mint/verify/revoke HMAC bearer tokens
    ├── mcp_transport.py        # McpClient: gatekeeper-routed, token-auth remote tool calls
    ├── budget.py               # BudgetTracker: spend counter + forecast + overrun alert
    ├── llm_client.py           # LLMClient protocol + GatekeptLLM
    ├── llm_backend.py          # select OpenAI vs offline echo backend (by OPENAI_API_KEY)
    ├── openai_backend.py       # real OpenAI Chat Completions (omitted from coverage)
    ├── google_auth.py          # lazy build_services (real OAuth; omitted from coverage)
    ├── gmail_client.py         # send_email (DI service)
    ├── token_cost.py           # token accounting + cost estimate (config-driven pricing; R.7)
    ├── config.py · version.py · constants.py
    └── models.py               # Position, Action, GameState, TurnResult, SubGameResult, Message, Meeting
config/    config.json · rate_limits.json · logging_config.json   (versioned 1.00)
tests/     unit/ · integration/ · conftest.py
scripts/   make_figures.py · sensitivity.py · gatekeeper_demo.py · token_report.py · google_smoke.py · run_mcp_server.py · check_mcp.py · run_series.py
Dockerfile · render.yaml   # cloud deploy of the two MCP servers (Render blueprint; ngrok alt)

notebooks/ analysis.ipynb   # Dec-POMDP/Bellman (LaTeX), sensitivity results, references
assets/    graphs, board screenshots, match.gif        results/  run logs
```
> Every file targets **≤150 lines of code** (comments/blanks excluded); split when exceeded.
> Note: the `mcp/` package lives under `services/mcp/` (not the package root). `belief_model`/`q_table`
> remain planned.
>
> **GUI streaming design (real-time window).** The service layer exposes the game as a *per-turn frame
> stream* — `services/match_stream.py` (`heuristic_subgame_stream`) and `services/nl_match.py`
> (`nl_subgame_stream`) are generators that `yield (deepcopy(state), caption)` once before the first move
> and again after every turn; the shared `stream_subgame()` helper holds the single engine loop (DRY).
> Two consumers render the same stream: the **GIF animator** collects it into a list and writes a file
> (headless `Agg`, deterministic/CI-safe), while the **live viewer** (`gui/live_viewer.py`) switches
> matplotlib to an interactive backend at runtime (config `gui.live_backend`, default `TkAgg`) and draws
> each frame the instant it streams off the engine — so an NL match visibly advances as each LLM call
> returns. The GUI stays render-only; all game logic is in the SDK-exposed services (SDK-only).
>
> **Live-viewer threading (responsiveness).** A turn can block for seconds (the NL match makes an LLM call
> per turn), so producing frames on the GUI thread would freeze the window ("not responding"). The live
> viewer therefore runs the frame **generator on a daemon worker thread** that pushes `(state, caption)`
> onto a thread-safe `queue.Queue` (plus a sentinel when done), while the **Matplotlib/Tk event loop owns
> the main thread**. A `fig.canvas.new_timer` fires every `gui.poll_interval_ms` (default 150 ms), draining
> one frame per tick via `_render_tick` and stopping on the sentinel. The event loop never blocks, so the
> window stays responsive while turns compute in the background. `_produce`/`_render_tick` are pure helpers
> (no matplotlib), unit-tested directly; the threading/queue is a presentation concern, kept in `gui/`.
>
> **Visual style (modern dark).** `gui/theme.py` is the single source of the dark palette + a `glow()`
> helper (layered-scatter halo); `gui/overlays.py` draws the HUD (turn/winner banner, move counter, legend)
> and a rounded **speech bubble** anchored on the speaker. `board_renderer.render_state` composes them:
> dark board, faded **movement trails**, glowing cop (blue disc) / thief (amber star) tokens, barrier slabs,
> and a **capture flash** on a cop win. Trails + `max_moves` are passed in by the caller so the renderer
> stays stateless. (Matplotlib can't draw colour emoji, so agents are distinct glowing tokens, not emoji.)

### 4.1 Extension Points (extensibility)
New behaviour is added by implementing a small interface and registering it via config — **no core edits**:

| Extension point | Interface / contract | Register via | Worked example |
|---|---|---|---|
| **Strategy (cop/thief)** | `Decider = Callable[[GameEngine, GameState], Action]` | add to `COP_POLICIES` / `THIEF_POLICIES` in `orchestrator.py`; pick with `strategy.type` / `strategy.thief_type` | add `q_table`: write `q_table_action(engine, state)`, register `COP_POLICIES["q_table"]=...`, set `strategy.type:"q_table"` |
| **LLM backend** | `Callable[[str], str]` | `shared/llm_backend.select_backend` (keyed on env) | swap OpenAI for Anthropic by returning a different completion callable |
| **Speaker (NL voice)** | `Speaker = Callable[[Role, Observation, Action], str]` | inject into `NLDecider` (`encode` template or `nl_speak.llm_speaker`) | add a new persona by writing a `speak_prompt` variant |
| **GUI renderer/consumer** | consume the SDK frame stream (`(state, caption)`) | `gui/` viewers (`live_viewer`, `match_animator`) | add a web renderer that consumes `Sdk.stream_nl_frames` |
| **MCP tools** | FastMCP tool functions over `ToolService` | `services/mcp/` | expose a new verification tool |

Lifecycle seams today are the **per-turn pipeline** (`turn_pipeline.run_turn` — the natural before/after-move
hook) and the **frame stream** (`match_stream.stream_subgame` — observe each turn). A formal plugin/middleware
registry (entry-points) is a noted future enhancement; the callable-interface + config-registry pattern
above already allows adding strategies, backends, voices, renderers, and tools without touching core logic.

---

## 5. Data Contracts & Schemas

### 5.1 `config/config.json`
```json
{
  "version": "1.00",
  "grid_size": [5, 5],
  "max_moves": 25,
  "num_games": 6,
  "max_barriers": 5,
  "visibility_radius": 1,
  "scoring": { "cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5 },
  "strategy": { "type": "heuristic" },
  "llm": { "provider": "openai", "model": "gpt-4o-mini", "pricing": { "input_per_1m": 0.15, "output_per_1m": 0.60, "chars_per_token": 4, "est_output_tokens_per_call": 4 } },
  "reporting": {
    "recipient_email": "sharbelma3@gmail.com",
    "_submission_recipient": "rmisegal+uoh26b@gmail.com",
    "send_real_email": true
  },
  "google": {
    "secrets_dir": "<absolute path to a secret folder OUTSIDE the repo>",
    "credentials_file": "client_secret.json",
    "token_file": "token.json",
    "scopes": [
      "https://www.googleapis.com/auth/gmail.modify",
      "https://www.googleapis.com/auth/calendar"
    ]
  }
}
```
> `reporting.recipient_email` is **dev = `sharbelma3@gmail.com`** now; flip it to the submission
> address (tag kept verbatim) at hand-in — a config-only change. `google.secrets_dir` points outside
> the repo so `client_secret.json`/`token.json` are never committed.

### 5.2 Core domain models (conceptual)
```text
Position(x:int, y:int)
Action = MOVE(dx,dy in {-1,0,1}, not both 0) | PLACE_BARRIER | STAY
Message(sender: 'cop'|'thief', text: str)
TurnResult(actor, action, event: NONE|CAPTURE|BARRIER_PLACED|ILLEGAL|MAX_MOVES_REACHED, state)
SubGameResult(index, winner:'cop'|'thief', moves_used, cop_score, thief_score)
MatchReport(group_name, students[], github_repo, cop_mcp_url, thief_mcp_url,
            timezone, sub_games[], totals{cop,thief})
```

### 5.3 MCP tool surface (per server) — full contract in [`PRD_mcp_server.md`](PRD_mcp_server.md)
- `send_message(text)` · `receive_message()` · `get_observation()` · `submit_action(action)` ·
  `verify_location()` · `get_game_status()`.

### 5.4 Report JSON — full schemas in [`PRD_email_reporting.md`](PRD_email_reporting.md)
Internal-game and inter-group bonus structures, JSON-only email body.

---

## 6. Key Process Flows (UML-style)

### 6.1 Sub-game turn (sequence)
```text
Orchestrator -> GameEngine: get_observation(actor)
Orchestrator -> LLMClient(via Gatekeeper): decide(observation, inbox, belief)
LLMClient --> Orchestrator: {message, action}
Orchestrator -> MCP(actor): send_message(message)
Orchestrator -> GameEngine: apply(actor, action)   # validates legality
GameEngine --> Orchestrator: TurnResult (+ event)
alt CAPTURE or moves==max_moves
   Orchestrator -> Scoring: score(subgame) -> accumulate
end
```

### 6.2 Match (state machine)
```text
INIT -> RUN_SUBGAME(i) -> SCORE(i) -> [i<6 ? RUN_SUBGAME(i+1) : BUILD_REPORT]
BUILD_REPORT -> SEND_EMAIL -> DONE
RUN_SUBGAME --(technical failure)--> TECHNICAL_LOSS -> RE-RUN(i)
```

---

## 7. Testing Strategy (summary)
- TDD per module; unit tests mirror `src/`; integration tests for full local match.
- Mock LLM, MCP transport, and Gmail in unit tests (no external calls).
- Sanity sweeps on 2×2 / 3×3 / 4×4 / 5×5 grids (from the assignment's recommended stages).
- Coverage gate `fail_under = 85`; Ruff `select = ["E","F","W","I","N","UP","B","C4","SIM"]`.

---

## 8. Risks & Mitigations
| Risk | Mitigation |
|---|---|
| LLM ambiguity / unparseable message | Defensive NL parser + belief fallback; never crash (NFR). |
| Provider rate limits / cost overrun | Gatekeeper rate-limit + queue + budget alerts. |
| Cloud/firewall blocking ports | Hybrid outbound-only; avoid org networks; documented in README. |
| Non-terminating sub-game | Hard `max_moves` cap → thief win; technical-loss detection → re-run. |
| Secret leakage | `.env` git-ignored, `.env-example` only, pre-commit scan. |
