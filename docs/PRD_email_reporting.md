# Specialized PRD — Automated Email Reporting (Gmail API + JSON Schemas)

**Mechanism:** Autonomous end-of-match JSON report via the Gmail API
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)
**Setup guide:** [`../MATERIALS/main-google-api-installtion-guid_Summary.md`](../MATERIALS/main-google-api-installtion-guid_Summary.md)
**Uses:** [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md) — the `send_email` tool and the
shared Google OAuth client/scopes are defined there; this PRD covers the **report content, schema, and timing**.

---

## 1. Description & Theoretical Background
At the end of every full match (6 sub-games), the system **autonomously emails a JSON report** via the
Gmail/Calendar agent's `send_email` tool. The **Gmail API** is used (not raw SMTP) for reliability and
to avoid being blocked by external mail servers. Authentication uses **token-based OAuth** rather than a
username/password: a stolen short-lived token is far less dangerous than a password. Google issues a
secret client file (`client_secret.json`) and a `token.json` created on first authentication.

> **Status (2026-06-25):** the **report builders** (`services/reporting.py`) and the **end-of-match send
> wiring** are implemented and tested. `services/match_reporter.send_match_report` builds the internal JSON
> report from the match summary + `reporting.report_meta` and emails it via an injected sender, **gated by
> `reporting.send_real_email`** (default `false`); the SDK exposes `Sdk.send_match_report`, and the CLI
> (`main._maybe_send_report`) builds the real Gmail service and sends after a full match when the flag is on.
> Real send (`send_email`) is **verified on live Gmail** (README R.1). Still pending: the inter-group
> **bonus arithmetic** (10/5/5 + averaging) and the **cloud series** (assignment §12).

**Recipient (config-driven — `reporting.recipient_email`, never hard-coded):**
- **Now (development/testing):** `sharbelma3@gmail.com`.
- **At submission:** switch the config value to `rmisegal+uoh26b@gmail.com` **verbatim** — keep the
  `+uoh26b` plus-address tag (it routes to the lecturer's filtered folder; stripping it may drop the submission).
Switching recipients is a **one-line config change, no code edit**.

**Hard rule:** the email **body contains ONLY the JSON report** — no free text — so the testing system
can ingest it automatically.

## 2. Inputs / Outputs / Setup

### 2.1 Input
- Accumulated `MatchReport` data (per-sub-game results + totals), group metadata, MCP URLs, GitHub link.

### 2.2 Output
- One email to `reporting.recipient_email` (dev: `sharbelma3@gmail.com`) whose body is exactly the JSON document (UTF-8).

### 2.3 Setup (Google Cloud) — shared with the agent
- OAuth Client of type **Desktop**; enable **Gmail API** **and Google Calendar API**.
- Scopes (config-driven): `https://www.googleapis.com/auth/gmail.modify` (read + send) +
  `https://www.googleapis.com/auth/calendar`. Full rationale in [`PRD_gmail_calendar_agent.md`](PRD_gmail_calendar_agent.md) §3.
- Add the sending Gmail account as a **Test user** (Testing mode).
- Files: `client_secret.json` (downloaded) + `token.json` (generated on first run) live in a **secret
  folder OUTSIDE the repo** — **both git-ignored**; include a token-expiry re-consent recovery path.
- Dependencies via `uv`: `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`.

> _Planned:_ Gmail/Calendar sends will route through the **gatekeeper**
> ([`PRD_gatekeeper.md`](PRD_gatekeeper.md)) once OAuth is wired (the LLM path is gatekept today — see
> README R.9); they are not gatekept yet.

## 3. JSON Schemas

### 3.1 Internal game report (single group)
```json
{
  "group_name": "Team-Alpha",
  "students": [],
  "github_repo": "https://github.com/<org>/marl-cop-thief",
  "cop_mcp_url": "https://cop-mcp-<grp>.<cloud>",
  "thief_mcp_url": "https://thief-mcp-<grp>.<cloud>",
  "timezone": "Asia/Jerusalem",
  "sub_games": [],
  "totals": { "cop": 90, "thief": 40 }
}
```

### 3.2 Inter-group bonus report (two groups)
```json
{
  "report_type": "bonus_game",
  "groups": { "group_1": "Team-Alpha", "group_2": "Team-Beta" },
  "github_repo_group_1": "https://github.com/<org-a>/marl-cop-thief",
  "github_repo_group_2": "https://github.com/<org-b>/marl-cop-thief",
  "mcp_url_group_1_cop": "https://cop-mcp-alpha.<cloud>",
  "mcp_url_group_1_thief": "https://thief-mcp-alpha.<cloud>",
  "mcp_url_group_2_cop": "https://cop-mcp-beta.<cloud>",
  "mcp_url_group_2_thief": "https://thief-mcp-beta.<cloud>",
  "timezone": "Asia/Jerusalem",
  "students_group_1": [],
  "students_group_2": [],
  "sub_games": [],
  "totals_by_group": { "Team-Alpha": 60, "Team-Beta": 80 },
  "bonus_claim": { "Team-Alpha": 7, "Team-Beta": 10 },
  "mutual_agreement": true
}
```

## 4. Reporting Rules
- **JSON-only body**, no free text (automated ingestion).
- A game that did not conclude due to a **technical loss** is failed → **re-run** to complete the quota of 6.
- **Inter-group bonus:** both groups email reports with the **exact same result** (mutual agreement).
  Disagreement/mismatch → bonus cancelled (0 for both for that series). Submit within **one week**.
- **Bonus arithmetic (as-built — `services/bonus.py`, §12.2):** per series the higher accumulated score
  wins **10**, the loser **5**, a tie **5/5**; a non-mutual-agreement series is **void (0/0)**.
  `series_awards(series)` produces the report's `bonus_claim`; `final_bonus(group, series_list)` averages a
  group's awards over all valid series (e.g. 10 & 5 → 7.5). Exposed via `Sdk.bonus_awards` / `Sdk.bonus_final`.
  Award values are **parameters** (defaults from the spec) — the spec's 8.5 example needs a per-series rule
  the docs state inconsistently, so the exact values stay **confirmable with course staff** (audit C5). The
  6-game **3-cop/3-thief role-swap** *runner* is built — `services/series_runner.run_series(config, a, b)`
  (also `Sdk.run_series` / `scripts/run_series.py`) plays the series, accumulates `totals_by_group`, and
  assembles this `bonus_game` report incl. `bonus_claim`; `Sdk.send_report` emails any report (JSON-only,
  gated). For a **live cross-group** match the opponent's agents are driven over their remote MCP servers
  (`McpClient`) instead of local policies — same scoring + report. (Internal single-group role split = C1,
  staff-confirm.)

## 5. Performance Metrics
- Single send succeeds within the gatekeeper's retry budget; delivery confirmed via Gmail API response.
- Report build is O(num_games) and validates against the schema before sending.

## 6. Constraints & Limitations
- No secrets in code: `credentials.json`/`token.json` are git-ignored; `.env-example` documents config.
- Stale scopes → delete `token.json` and re-auth (documented troubleshooting).
- Testing-mode "unverified app" warning is expected while the sender is a registered Test user.

## 7. Alternatives Considered
- **Raw SMTP / password login:** rejected — block-prone and insecure vs. token-based Gmail API.
- **Free-text + JSON attachment:** rejected — spec requires the body itself to be JSON-only.
- **Service account:** not suitable for sending as a real user mailbox here; OAuth Desktop client is used.

## 8. Success Criteria & Test Scenarios
- **S1:** After 6 sub-games, exactly one email is sent to the target address with a JSON-only body.
- **S2:** Built JSON validates against the internal (and, when applicable, inter-group) schema.
- **S3:** A technical-loss game is detected and re-run so totals reflect 6 completed games.
- **S4:** Gmail transport is mocked in unit tests (no live send); ≥85% coverage; file ≤150 lines.
- **S5:** Missing/expired token triggers a clean re-auth path without leaking secrets to logs.
