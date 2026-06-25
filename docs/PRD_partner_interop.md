# Specialized PRD — Inter-Group Interop (partner `/decide` protocol)

**Mechanism:** Play the §12 inter-group match against a partner team whose servers speak a
**custom JSON-over-HTTP decision protocol** (not MCP).
**Document version:** 1.00
**Status:** Approved (2026-06-26)
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md) · related [`PRD_mcp_server.md`](PRD_mcp_server.md)

---

## 1. Description & background
The partner (`salareen`) deployed two servers (`-cop`, `-thief`) that are **stateless decision
functions**, not game hosts. Their `GET /health|/identity|/capabilities` describe the server; their
**`POST /mcp/decide`** takes a role-filtered observation with explicit `legal_actions` and returns
**exactly one** of them. *"The calling orchestrator owns the authoritative game state, creates a
role-filtered observation, sends it to `/decide`, validates the returned action, and applies it locally."*

So **we own the game** (`GameEngine`): each turn we ask **our** policy for our role and **their `/decide`**
for theirs, apply the action, and continue. This bridges our MCP-native system to their REST protocol with
no change on their side.

## 2. Their protocol (as probed live)
- Auth: `Authorization: Bearer <role-token>` (verified).
- `POST /mcp/decide` request: `{protocol_version, request_id, correlation_id, role, observation}` where
  **`observation.request_id` MUST equal the envelope `request_id`** (else `409`).
- Observation: `{grid_size, self_position, visible_opponent|null, visible_barriers, legal_actions,
  move_round, max_moves, barriers_placed, max_barriers, history_summary}`.
- Response: `{... "decision": {"action": {...}}}`; action is `{"type":"move","direction":up|down|left|right}`
  or (cop) `{"type":"place_barrier","target":[row,col]}`. **No `stay`, no diagonals, no NL messaging.**

### Coordinate & direction mapping (validated by live `/decide` probes)
Their coordinates are **`[row, col]` = our `(y, x)`**, and movement is **4-directional**:

| their direction | their delta | our `(dx, dy)` |
|---|---|---|
| `up` | row − 1 | `(0, −1)` |
| `down` | row + 1 | `(0, +1)` |
| `left` | col − 1 | `(−1, 0)` |
| `right` | col + 1 | `(+1, 0)` |

Position map: our `Position(x, y)` → their `[y, x]`. Barrier target → `[cop.y, cop.x]`.

## 3. Inputs / outputs (our modules)
- `services/partner_protocol.py` (pure): `to_partner_observation(engine, state, role, radius, request_id)`,
  `legal_partner_actions(engine, state)`, `from_partner_action(action) -> Action`.
- `services/strategy/ortho_policy.py` (pure): `ortho_action(engine, state)` — our 4-dir policy (cop closes
  in; thief flees + keeps escape room).
- `shared/partner_client.py`: `PartnerClient.decide(role, observation, request_id)` — **gatekeeper-routed**
  (CLAUDE §2), token-authenticated, transport injected (offline-testable).
- `services/interop_match.py`: `play_interop_game(...)` + `run_interop_series(...)` → the 6-game
  3-cop/3-thief swap report (`report_type: "interop_match"`).

## 4. Constraints & limitations
- The game is **4-directional, no `stay`, no NL** (their protocol's limits) — a restricted variant of our
  8-dir engine; our side plays the same orthogonal move set for fairness.
- Visibility is config-driven (`visibility_radius`); their decider receives `visible_opponent: null` when
  the opponent is out of range and must act blind.
- **We** produce the authoritative result; for the §12 bonus both teams email the *same* JSON, so the
  result/move-log is shared with the partner (mutual agreement).

## 5. Alternatives considered
- *Shared MCP host* (our `build_host_server`): rejected — their servers are stateless deciders, not hosts.
- *They adopt MCP*: rejected — more work for them; our adapter needs zero change on their side.

## 6. Security
- Partner URLs + tokens come from the environment (`PARTNER_*` in `.env`, git-ignored) — never hard-coded.
- All `/decide` HTTP calls route through the `ApiGatekeeper` (`gmail`-style service config) for rate
  limiting, retries, and logging.

## 7. Success criteria & test scenarios
- **S1:** `to_partner_observation` emits their exact schema with correct `[row,col]` mapping (unit).
- **S2:** `from_partner_action` maps every direction + `place_barrier` back to our `Action`; unknown → error.
- **S3:** `ortho_action` cop reduces distance; thief increases it; surrounded → `stay` (unit).
- **S4:** `PartnerClient.decide` routes through the gatekeeper and sends matching `request_id` (unit, fake transport).
- **S5:** `play_interop_game` drives a full game with a fake partner decider to a terminal state (unit).
- **S6:** Live smoke: one real game each way vs `salareen` ends legally (manual/script).

## 8. Open issue — protocol asymmetry & bonus reconciliation
**Status:** open (2026-06-26).

We adapted to the partner: we own the game and call their stateless `/decide` (live result **60–40**,
emailed). But their **bonus client drives the match from their side via REST `/decide`**, and **our servers
are FastMCP** — so they cannot call our agents the same way. The two stacks are asymmetric:

| | Our stack | salareen's stack |
|---|---|---|
| Transport | MCP (FastMCP, `/mcp/`) | custom REST (`/decide`) |
| Game state | server holds it (cop-mcp/thief-mcp each one game) | stateless; the caller owns the game |
| Session | one game per server, created at startup (no session endpoint) | n/a (stateless) |

**The §12 bonus needs both teams to email the *same* JSON** (mutual agreement; disagreement → 0/0). Two
resolutions:
1. **Share the authoritative result (recommended — no new infra).** We already ran the 6-game series; send
   salareen our group info + the result JSON; both email the identical JSON.
2. **Expose a REST `/decide` server mirroring their protocol (symmetric).** Wrap `ortho_policy` in a
   `/health`+`/identity`+`/capabilities`+`/decide` server, deploy it, share URLs+tokens; then their bonus
   client can drive a match against our agents independently. More robust, but a new server + deploy.

**Info salareen requested (answers):** group = **sharNamr**; students = **Sharbel, Amr**; repo =
`https://github.com/SharbelMaroun/AI-Agent-Orchestration-HW6`. Our MCP tools (a *game-hosting* model, not a
stateless `/decide`): `get_observation`, `send_message`, `receive_message`, `submit_action(kind,dx,dy)`,
`verify_location`, `get_game_status`; each server hosts **one** game created at startup (no session id).
