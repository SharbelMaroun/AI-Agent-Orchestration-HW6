# Specialized PRD — Automated Email Reporting (Gmail API + JSON Schemas)

**Mechanism:** Autonomous end-of-match JSON report via the Gmail API
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)
**Setup guide:** [`../MATERIALS/main-google-api-installtion-guid_Summary.md`](../MATERIALS/main-google-api-installtion-guid_Summary.md)

---

## 1. Description & Theoretical Background
At the end of every full match (6 sub-games), the system **autonomously emails a JSON report** to
`rmisegal+uoh26b@gmail.com`. The **Gmail API** is used (not raw SMTP) for reliability and to avoid
being blocked by external mail servers. Authentication uses **token-based OAuth** rather than a
username/password: a stolen short-lived token is far less dangerous than a password. Google issues a
secret client file (`credentials.json`) and a `token.json` created on first authentication.

**Hard rule:** the email **body contains ONLY the JSON report** — no free text — so the testing system
can ingest it automatically.

## 2. Inputs / Outputs / Setup

### 2.1 Input
- Accumulated `MatchReport` data (per-sub-game results + totals), group metadata, MCP URLs, GitHub link.

### 2.2 Output
- One email to `rmisegal+uoh26b@gmail.com` whose body is exactly the JSON document (UTF-8).

### 2.3 Setup (Google Cloud, per the installation guide)
- OAuth Client of type **Desktop**; enable **Gmail API**; scope `https://www.googleapis.com/auth/gmail.modify`.
- Add the sending Gmail account as a **Test user** (Testing mode).
- Files: `credentials.json` (downloaded), `token.json` (generated on first run) — **both git-ignored**.
- Dependencies via `uv`: `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`.

> Note: the assignment requires **Gmail** for reporting. Calendar (in the setup guide) is not required.
> All Gmail sends route through the **gatekeeper** ([`PRD_gatekeeper.md`](PRD_gatekeeper.md)).

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
