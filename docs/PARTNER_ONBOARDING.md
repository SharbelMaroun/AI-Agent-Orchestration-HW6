# Partner Onboarding — how to play `sharNamr` in the inter-group match

> This is written for the **partner team's coding agent (Codex)**. It explains (1) the architecture
> problem, (2) what the assignment actually requires, and (3) **two concrete ways** to play against us —
> over our **REST `/decide`** (least work) or over our **MCP** (spec-correct). Pick one.
> Our group: **sharNamr** (Sharbel, Amr) · repo: https://github.com/SharbelMaroun/AI-Agent-Orchestration-HW6

---

## 1. The problem (read first)

The two teams built **different architectures**, and only one matches the assignment:

| | **Assignment (ex06 §5.2, §7)** | **sharNamr (us)** | **salareen (you)** |
|---|---|---|---|
| Transport | **MCP / FastMCP** | ✅ FastMCP | ❌ custom REST |
| Where the decision lives | **in the CLIENT** (orchestrator) | ✅ client | ❌ in the server (`/decide`) |
| What the server exposes | **tools only** | ✅ tools only | ❌ a decision |

Because your server **decides**, it's easy to *call* — that's how we already played a series (we hosted and
called your `/decide`). But the assignment says the **MCP server must be tools-only** and the **brain must be
in the client**. Your `/decide`-server design deviates from that, and it's also **not MCP**. That mismatch is
why your game-hosting client can't drive our agents directly: a spec-compliant tools-only MCP server (ours)
has **no decision to hand out** — our brain is in our client, exactly as the spec requires.

## 2. What the assignment requires (target architecture)

1. **Two MCP servers per group** — one Cop, one Thief — built with **FastMCP**, deployed to a public HTTPS
   URL with **token auth**.
2. **MCP server = tools only.** No LLM/decision inside the server. It exposes tools (read observation, send/
   receive NL message, submit a move, query status).
3. **The brain is in the CLIENT** (the orchestrator/game engine). The client calls the LLM/policy, then calls
   MCP tools to act.
4. **Agents coordinate in natural language**, under partial observation (Dec-POMDP).
5. For the **inter-group bonus**: play **6 games** (3 as Cop / 3 as Thief, role-swapped); both groups email the
   **identical JSON** result to the lecturer (`rmisegal+uoh26b@gmail.com`).

**Recommended refactor for you:** move your decision logic out of the HTTP server into your **client**, and
re-expose your agents as **FastMCP tools** (`get_observation`, `submit_action`, …). Then either side can host a
shared game and both clients drive their own role — the model in Option B below.

---

## 3. How to play `sharNamr` — pick ONE option

### Option A — call our REST `/decide` (least work; ready now)
**You host the authoritative game; when it's *our* turn, ask our `/decide` for our move.** Our endpoint speaks
**your exact protocol v1.0**, so you need almost no new code.

- Base URL: `<OUR_DECIDE_URL>` (e.g. `https://decide-sharnamr.onrender.com`)
- Auth: `Authorization: Bearer <OUR_DECIDE_TOKEN>`
- `GET {base}/health` · `GET {base}/identity` · `GET {base}/capabilities` — sanity checks.
- `POST {base}/decide`:
  ```json
  { "protocol_version":"1.0", "request_id":"<uuid>", "correlation_id":"<uuid>",
    "role":"<the role WE play this game>",
    "observation": { "protocol_version":"1.0", "request_id":"<same uuid>", "role":"<same>",
      "grid_size":[5,5], "self_position":[row,col], "visible_opponent":[row,col]|null,
      "visible_barriers":[[row,col]], "legal_actions":[{"type":"move","direction":"up|down|left|right"}],
      "move_round":int, "max_moves":25, "barriers_placed":int, "max_barriers":5, "history_summary":[] } }
  ```
  → returns `{ "decision": { "action": {"type":"move","direction":"..."} } }` — exactly one of the
  `legal_actions` you sent.

**Rules to match (or you get 4xx/5xx):**
- `observation.request_id` **must equal** the envelope `request_id` (else `409`).
- Coordinates are `[row, col]`; directions `up/down/left/right` (same as yours — **no conversion**).
- **Send moves only** (no `place_barrier`) — keep the match moves-only (your own cop `/decide` returns `500`
  on `place_barrier`).
- `role` you pass us = whichever side **we** play: your group cop ⇒ pass `role:"thief"`; your group thief ⇒
  pass `role:"cop"`. One URL handles both (role comes from the observation).

### Option B — drive our MCP (the spec-correct way; more setup)
**We run a shared FastMCP *host* server** (one authoritative game, role-parameterized). **You write a FastMCP
client** that connects and drives **only your role**; we drive ours; the host is authoritative. This is the
assignment's intended cross-team model.

- Host URL: `<OUR_HOST_URL>/mcp/` (FastMCP **streamable-HTTP**), e.g. `https://host-sharnamr.onrender.com/mcp/`
- Auth: `Authorization: Bearer <OUR_HOST_TOKEN>` (FastMCP `BearerAuth`).
- Client (Python): `from fastmcp import Client; from fastmcp.client.auth import BearerAuth` →
  `async with Client(url, auth=BearerAuth(token)) as c: await c.call_tool("get_game_status", {})`.
- **Tools (role passed explicitly; coords are OUR `[x, y]` = `[col, row]`, 8-directional):**

  | Tool | Params | Returns |
  |---|---|---|
  | `get_game_status` | — | `{to_move, moves_used, moves_left, barriers_left, done, winner}` |
  | `get_observation` | `role` | `{role, self:[x,y], opponent:[x,y]\|null, visible_cells:[[x,y]], visible_barriers:[[x,y]]}` |
  | `submit_action` | `role, kind, dx, dy` | `{event, done, winner}` — `kind∈{move,stay,place_barrier}`; `dx,dy∈{-1,0,1}` (8-dir) |
  | `send_message` | `role, text` | `{ok:true}` |
  | `receive_message` | `role` | `{sender, text}` or `null` |
  | `verify_location` | `role` | `{x, y}` |

- **Driver loop (per your role):** poll `get_game_status`; if `done` → stop; if `to_move == your_role` →
  `get_observation(your_role)` → decide → `submit_action(your_role, "move", dx, dy)`; else wait and poll again.
  Thief moves first. (This mirrors our `scripts/play_remote.py`.)
- **Coordinate note:** unlike Option A, MCP uses **our** convention — position `[x, y]` (x=column, y=row) and
  **8-directional** `dx,dy` deltas (diagonals allowed). Convert to/from your internal grid.

> Option B requires us to deploy the host server and you to add a FastMCP client. Tell us if you want this —
> it's the spec-correct path but the heavier lift. Option A is ready immediately.

---

## 4. The report (both options)

After the 6-game series, **both groups email the *identical* JSON** (JSON body only, no free text) to
`rmisegal+uoh26b@gmail.com`:

```json
{ "report_type":"bonus_game",
  "groups":{ "group_1":"sharNamr", "group_2":"salareen" },
  "github_repo_group_1":"https://github.com/SharbelMaroun/AI-Agent-Orchestration-HW6",
  "github_repo_group_2":"<your repo>",
  "students_group_1":["Sharbel","Amr"], "students_group_2":["<your names>"],
  "timezone":"Asia/Jerusalem",
  "sub_games":[ /* per-game cop/thief/winner/scores */ ],
  "totals_by_group":{ "sharNamr":<n>, "salareen":<n> },
  "bonus_claim":{ "sharNamr":<10|5>, "salareen":<10|5> },
  "mutual_agreement": true }
```

Whoever hosts produces the authoritative result; the other side reports the **same** numbers. Mismatch ⇒ 0 for
both, so confirm before sending.
