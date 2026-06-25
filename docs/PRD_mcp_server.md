# Specialized PRD — MCP Server Architecture (FastMCP Dual Servers)

**Mechanism:** Two independent MCP servers (Cop & Thief) exposing tools
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)

---

## 1. Description & Theoretical Background
The **Model Context Protocol (MCP)** is an open standard for connecting LLMs to data sources, tools,
and external servers. This project runs **two independent MCP servers** — one for the Cop, one for the
Thief — each built with **FastMCP**. A fundamental rule (see ADR-001): **the LLM is NOT hosted in the
MCP server**. The MCP server exposes *tools, resources, and prompt templates* only. The **MCP client**
(the orchestrator/game engine) holds the LLM and the dialogue logic.

**Workflow per turn:** client → queries LLM → receives a tool-call decision → calls the MCP server to
execute the tool → returns the result to the LLM to complete the environment loop.

## 2. Inputs / Outputs / Setup

### 2.1 Tool surface (each server)
| Tool | Input | Output | Purpose |
|------|-------|--------|---------|
| `get_observation` | `actor` | partial view (own cell, visible cells, barriers in view) | Partial-observation snapshot |
| `send_message` | `text` | ack | Emit a free-text NL message to the opponent channel |
| `receive_message` | — | latest `Message` | Read inbound NL message |
| `submit_action` | `Action` | `TurnResult` | Propose a move/barrier; engine validates |
| `verify_location` | — | own authoritative position | Mutual location verification |
| `get_game_status` | — | turn no., moves left, barriers left, scores | Sync game state |

### 2.2 Setup
- `PORT_COP`, `PORT_THIEF`, server base URLs, and auth tokens read from `config`/`.env`.
- Transport: HTTP(S); local phase uses distinct localhost ports; cloud phase uses public HTTPS URLs.
- **As-built:** the client transport is `shared/mcp_transport.McpClient(base_url, token, invoke, gatekeeper)`
  — every `call_tool(...)` routes through the **gatekeeper** and carries the bearer token; the low-level
  `invoke` is dependency-injected (production: a `fastmcp.Client` HTTP adapter; tests: a fake), so it is
  offline-testable. The FastMCP servers (`mcp/servers.py`) run over streamable-HTTP at deploy time.

## 3. Architecture (Client vs Server)
```text
+-------------------- MCP CLIENT (orchestrator) --------------------+
|  holds LLM + dialogue logic                                       |
|  decide() -> tool_call -> [call MCP server] -> feed result to LLM |
+-------------------------------------------------------------------+
            | HTTPS (outbound)                | HTTPS (outbound)
            v                                 v
   +------------------+              +--------------------+
   |  Cop MCP server  |              |  Thief MCP server  |
   |  tools only      |              |  tools only        |
   |  (no LLM, no key)|              |  (no LLM, no key)  |
   +------------------+              +--------------------+
```

## 4. Performance Metrics
- Tool round-trip latency target: < 200 ms intra-region (excludes LLM time).
- Each server handles the sequential turn cadence of one match; concurrency is low by design.

## 5. Constraints & Limitations
- Servers contain **no secrets** and **no business decisions** — purely tool execution + state relay.
- All outbound API calls the client makes go through the **gatekeeper** ([`PRD_gatekeeper.md`](PRD_gatekeeper.md)).
- Cloud URLs must be reachable (not firewalled); avoid org networks blocking non-standard ports.

## 6. Security
- **Token-based auth** on both MCP URLs, with the ability to **revoke** access. **As-built:**
  `shared/mcp_auth.TokenAuth` mints **HMAC-signed, tamper-evident** bearer tokens (`mint`), verifies them
  in constant time (`verify`), and supports immediate **revocation** (`revoke`); the signing secret comes
  from `MCP_AUTH_SECRET` (env, never hard-coded). Unauthorized/tampered/revoked tokens are rejected (S5).
- Prefer **Hybrid** deployment (ADR-002): client + LLM local, only MCP server public, outbound-only —
  no inbound ports opened on developer machines.
- Tokens/secret in `.env` (git-ignored); `.env-example` documents required vars with dummy values.

## 7. Alternatives Considered
- **Single shared MCP server for both agents:** rejected — assignment requires two independent servers.
- **LLM embedded in MCP server:** rejected — violates spec; couples secrets to public surface.
- **Direct socket protocol instead of MCP:** rejected — MCP tool exposure is the graded mechanism.

## 8. Success Criteria & Test Scenarios
- **S1:** Both servers start locally on distinct ports and pass a health check.
- **S2:** `send_message`/`receive_message` deliver an NL message round-trip between servers.
- **S3:** `submit_action` reaches the authoritative engine and returns a correct `TurnResult`.
- **S4:** `verify_location` returns the engine's authoritative position (not agent belief).
- **S5:** Cloud deployment exposes two authenticated HTTPS URLs; unauthorized calls are rejected.
- **S6:** Unit tests mock the MCP transport (no live servers) and still cover tool contracts; ≥85%.
