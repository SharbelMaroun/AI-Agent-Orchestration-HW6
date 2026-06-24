# Specialized PRD — Gmail & Calendar Agent

**Mechanism:** AI agent that reads Gmail, extracts meeting invites, writes Calendar events, and sends email
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)
**Sources:** [`../MATERIALS/Gmail_calendar_agent_guide.md`](../MATERIALS/Gmail_calendar_agent_guide.md) ·
[`../MATERIALS/main-google-api-installtion-guid_Summary.md`](../MATERIALS/main-google-api-installtion-guid_Summary.md)
**Related:** [`PRD_email_reporting.md`](PRD_email_reporting.md) (the end-of-match JSON report uses this agent's `send_email`).

---

## 1. Description & Theoretical Background
Beyond the pursuit game, the project must demonstrate an **AI agent that acts on a real Google
account** rather than only chatting. The agent reads the Gmail inbox, finds a **meeting invitation**
inside an email, **adds that meeting to Google Calendar**, and **sends email** (including the
end-of-match completion/report email to the lecturer). This exercises the full agent loop:
**perceive (read) → reason (extract) → act (calendar + send)**.

**Mental model (from the guide):** `client secret → user consent → token → API calls`. A Google Cloud
OAuth *client* identifies the app; after the user consents, a *token* grants the app the right to act
as that user.

### 1.1 Relation to the game
The agent is **triggered by the orchestrator when the full match (6 sub-games) finishes**: it builds
the JSON result and calls `send_email` to deliver it. The read/extract/calendar tools are the same
Google competency demonstrated on real inbox data. The game and the email/calendar agent share **one
Google credential** and **one recipient mailbox**; they are otherwise independent capabilities.

## 2. Tools (Inputs / Outputs)
| Tool | Input | Output | Notes |
|------|-------|--------|-------|
| `read_emails(query, max_results)` | optional Gmail query, count | `list[EmailMessage]` | Scans inbox; needs read scope |
| `extract_meeting(email)` | one `EmailMessage` | `Meeting{title, start, end, location}` or `None` | LLM-assisted parse **via gatekeeper** |
| `add_calendar_event(meeting)` | `Meeting` | `(event_id, html_link)` | Creates event on `primary` calendar |
| `send_email(to, subject, body)` | recipient, subject, body | `message_id` | Real **send** (not draft); used for the report email |

`EmailMessage(id, sender, subject, body, received_at)` · `Meeting(title, start_dt, end_dt, location?)`.

## 3. Setup, Scopes & Configuration
- **Google Cloud (per the install guide):** OAuth **Desktop** client; enable **Gmail API** *and*
  **Google Calendar API**; add the authenticating Gmail as a **Test user** (External app, Testing mode).
- **Scopes (least-privilege, config-driven — never hard-coded):**
  - `https://www.googleapis.com/auth/gmail.modify` — read + send + drafts (covers `read_emails` & `send_email`), **or** the stricter pair `gmail.readonly` + `gmail.send`.
  - `https://www.googleapis.com/auth/calendar` — create/update Calendar events.
- **Recipient (config-driven):** `reporting.recipient_email`.
  - **Now (development/testing):** `sharbelma3@gmail.com`.
  - **At submission:** switch the config value to `rmisegal+uoh26b@gmail.com` **verbatim** — keep the
    `+uoh26b` plus-address tag (it routes to the lecturer's filtered folder; stripping it may drop the submission).
- **Dependencies (`uv`):** `google-api-python-client`, `google-auth-oauthlib`, `google-auth-httplib2`.

## 4. Security & Secrets
- Keep `client_secret.json` and `token.json` in a **secret folder OUTSIDE the repository** (not in
  `src/` or the project tree). Their location is read from config/env, never hard-coded.
- `.gitignore` must exclude `client_secret.json`, `token.json`, `credentials.json`, `.env`.
- **Token expiry / recovery (the deadline trap):** tokens expire. Build the recovery path in from the
  start — `if token missing/expired/invalid → delete token.json → re-run → browser re-consent → new token`.
- All Gmail/Calendar API calls route through the **gatekeeper** ([`PRD_gatekeeper.md`](PRD_gatekeeper.md)).

## 5. Performance Metrics
- `read_emails` returns within the gatekeeper's latency/retry budget; pagination bounded by `max_results`.
- `extract_meeting` precision/recall measured on a small labelled sample of invite emails (research note).
- A full "read → extract → add event → send" cycle completes in one autonomous run with 0 manual steps.

## 6. Constraints & Limitations
- Demo (setup guide) only creates a **draft** and a **fixed** event; the assignment requires real
  **send** and a **parsed** event time → this PRD covers that gap.
- Testing-mode "unverified app" warning is expected while the sender is a registered Test user.
- Meeting extraction depends on the LLM; ambiguous emails may yield `None` → handle gracefully (no crash).

## 7. Alternatives Considered
- **Raw SMTP / password login:** rejected — block-prone and insecure vs. token-based Gmail API.
- **Regex-only meeting parsing:** rejected as sole method — brittle on free-text invites; LLM-assisted extraction with a validation step is used.
- **Service account:** not suitable for acting on a real personal mailbox here; OAuth Desktop client is used.
- **Secrets inside the repo:** rejected — credentials/token live in an external secret folder.

## 8. Success Criteria & Test Scenarios
- **S1:** `read_emails` returns inbox messages for a known query (Gmail mocked in unit tests).
- **S2:** `extract_meeting` returns the correct `Meeting` for an invite email; returns `None` (no crash) for a non-invite.
- **S3:** `add_calendar_event` creates an event whose start matches the extracted time (Calendar mocked in unit tests).
- **S4:** `send_email` performs a real send to `reporting.recipient_email`; in dev that is `sharbelma3@gmail.com`.
- **S5:** Switching `recipient_email` to `rmisegal+uoh26b@gmail.com` requires **no code change**.
- **S6:** Expired/missing token triggers the documented re-consent path without leaking secrets to logs.
- **S7:** Module files ≤150 lines; external APIs mocked; ≥85% coverage of all four tools' branches.
