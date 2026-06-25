# Prompt-Engineering Log

**Project:** Dual AI Agent Race via MCP Servers — "Cop & Thief"
**Required by:** [`../MATERIALS/software_submission_guidelines-V3_Summary.md`](../MATERIALS/software_submission_guidelines-V3_Summary.md) §8.3 (Prompt Engineering Log) and the final checklists (§17.1, §20.7 — "documented prompt book").

> Log every **significant** prompt used to build the project: its **context/goal**, an **example of the
> output**, **improvements** made, and **recommended practices** learned. Keep newest first.
> Two kinds of prompts belong here: (1) prompts used to **develop** the project (to an AI coding agent),
> and (2) the **runtime LLM prompts** the agents use in-game (the system/cop/thief templates).

---

## A. Development prompts (building the project)

| # | Date | Context / Goal | Prompt (summary) | Output / Result | Improvement & lesson |
|---|------|----------------|------------------|-----------------|----------------------|
| A1 | 2026-06-24 | Bootstrap the repo to the guidelines | "Analyze MATERIALS; create the docs the V3 guidelines require." | Full `docs/` suite (PRD/PLAN/TODO + per-mechanism PRDs) | Be explicit that the standards file is authoritative → fewer omissions. |
| A2 | 2026-06-25 | Integrate the Gmail/Calendar agent | "Integrate the Gmail/Calendar guide; send to sharbelma3@gmail.com for now." | New PRD + config-driven recipient | Make the recipient config-driven → switching to the lecturer is a 1-line change. |
| A3 | 2026-06-25 | Lecturer rule: 550+ tasks | "Rewrite TODO with 550+ tasks." | `docs/TODO.md` = 689 granular tasks | Generate via template (per-module TDD lifecycle) for consistent IDs. |
| A4 | 2026-06-25 | Implement phases 0/1/3/2/5 | "Implement phase X, check, commit." | Tested modules, 100% cov | Route LLM via gatekeeper; keep deciders pluggable; fake LLM keeps tests offline. |
| A5 | 2026-06-25 | Phase 9 full gatekeeper | "Upgrade gatekeeper: config-driven rate limit + FIFO queue + backpressure + drain + retries + concurrency; offline tests." | `shared/{gatekeeper,rate_limit}.py` + 15 tests | Inject `clock`/`sleep` so rate limiting is deterministic offline; split the limiter out to stay ≤150 LOC. |
| A6 | 2026-06-25 | Adversarially review Phase 9 | Workflow: 4 review lenses (concurrency/spec/coverage/regression) → each finding independently verified vs the real code | 12 findings → 6 confirmed, 6 refuted; all 6 fixed | Multi-agent adversarial review caught a Ctrl-C ticket-leak deadlock + a prod path that never loaded `rate_limits.json` — bugs the green 100%-cov suite missed. Verify findings before acting. |
| A7 | 2026-06-25 | Greedy cop limit-cycles (R.3) | "Add a cornering 'smart' cop (1-ply look-ahead), config-selectable via `strategy.type`; refresh the comparison graphs." | `services/strategy/smart_cop.py` + `geometry.py`: capture 0.72→1.00 on 5×5, 100% on 3×3–7×7 (commit fd11906) | Rank actions by `(distance, thief escape-options)` after the thief's reply; keep it pluggable so the greedy baseline stays for the R.3 comparison. |
| A8 | 2026-06-25 | Required token-cost analysis (R.7) | "Capture real prompts from an offline match and price them at config-driven gpt-4o-mini rates." | `shared/token_cost.py` + `scripts/token_report.py` → `results/token_cost.txt` (66 calls, 3310 tokens, $0.000615/match) (commit 6aa0d24) | Estimate offline (~4 chars/token, no tokenizer download); keep prices in `config.json → llm.pricing` (never hardcode). |
| A9 | 2026-06-25 | See the NL run, not just text | "Make `cop-thief --gui` animate the NL sub-game with each turn's NL message overlaid." | `gui/match_animator.animate_nl_match` + `services/nl_match.nl_subgame_frames` + bus `peek_last` → `assets/match_nl.gif` (commit dec7d05) | Read the spoken message off the bus (`peek_last`) so the GUI reuses the live match and stays free of business logic (SDK-only). |
| A10 | 2026-06-25 | Confirm a real OpenAI run | "Print the active LLM backend + gatekeeper call count for NL runs." | `main.py` shows `LLM backend: OpenAI (gpt-4o-mini)` + `LLM calls via gatekeeper: N` (commit 979d029) | Surface the backend so a silent offline fallback can't be mistaken for a keyed run. |
| A11 | 2026-06-25 | "The GUI isn't real-time" — add a live window | "Run the app so I can see the GUI and all the flow" → the GIF is a recording, not a live view; build a real-time interactive window (T6.39–48). | `gui/live_viewer.py` (`--live`) renders service-layer per-turn frame streams (`match_stream.py` + `nl_subgame_stream`) live; GIF reuses the same stream (DRY); SDK-exposed; 166 tests, 100% cov | Refactor the game loop into a *generator* so one stream feeds both the live window (consume lazily) and the GIF (collect to list); keep matplotlib backend config-driven and switch to interactive at runtime so headless/CI stays on `Agg`. |
| A12 | 2026-06-25 | Live window freezes ("not responding") while waiting for a turn | "If I press the GUI while it's waiting for the other player it says 'not responding' — maybe use another thread per task." | Threaded the live viewer: frame generator on a daemon worker thread → `queue.Queue`; Tk event loop on the main thread drains via `fig.canvas.new_timer` (`gui.poll_interval_ms`); pure `_produce`/`_render_tick` helpers (T6.49–52). | A blocking call (the per-turn LLM request) must never run on the GUI thread — produce on a worker, render on the event-loop thread, hand off via a thread-safe queue + timer poll. Keep the blocking-vs-render split in pure helpers so it's unit-testable without a display. |
| A13 | 2026-06-25 | Set up cloud + tokens via a browser agent | Step-by-step prompt to an "Open Claude" browser extension: create Google Cloud project, enable Gmail+Calendar APIs, configure External/Testing OAuth (2 scopes + test user), create a Desktop OAuth client → download `client_secret.json`; create an OpenAI key; create a Prefect workspace + token. | Project `cop-thief-agent`, both APIs enabled, OAuth Desktop client `624232608258-…`, OpenAI key, Prefect workspace URL + token. | Constrain the agent: one project end-to-end, **OAuth client ID (not API key/service account)**, never paste secrets into the repo, download `client_secret.json` to an external folder. Caveat surfaced: Google forces the **support email = logged-in account**, so consent must be done as a listed **Test user**. |
| A14 | 2026-06-26 | Live inter-group match vs partner `salareen` (custom REST `/decide`, not MCP) | "Play the 6-game match vs the partner; they sent server URLs/tokens — build the adapter and run it; email the result." | `services/{partner_protocol,interop_match}.py` + `shared/partner_client.py` + `strategy/ortho_policy.py`; live **60–40**, JSON emailed; their cop `/decide` 500s on `place_barrier` → moves-only | Probe the live server to learn the *undocumented* coord/direction mapping (`[row,col]`=our `(y,x)`); we own the engine and call their stateless `/decide`; gate `place_barrier` off after observing a live 500. Two different protocols interoperate cleanly when one side is a stateless decision function. |
| _…_ | | | | | |

## B. Runtime agent prompts (in-game LLM)
> Runtime LLM templates — implemented and tracked with versions below (B1/B2 in `prompt_templates.py`,
> B3 in `nl_encode.py`, B4 in `meeting_extractor.py`).

Implemented in `src/marl_cop_thief/services/nl_protocol/prompt_templates.py`.

| # | Template | Version | Goal | Notes / improvements |
|---|----------|---------|------|----------------------|
| B1 | `system_prompt(role)` | 1.0 | Frame the partial-observation pursuit, NL-only, role+goal | Allows vagueness so the thief can bluff |
| B2 | `interpret_prompt(message)` | 1.0 | Extract opponent position as `x,y` or `unknown` from a message | Paired with defensive `parse_position`; falls back to prior on failure |
| B3 | encode (deterministic) | 1.0 | Cop reveals its cell; thief stays vague (partial deception) | Template-based in `nl_encode.py`; the offline/default speaker and the fallback for B5 |
| B4 | meeting-extraction prompt | 1.0 | Extract `title\|start_iso\|end_iso` from an email | In `services/google_agent/meeting_extractor.py`; defensive parse → `Meeting` or `None` |
| B5 | `speak_prompt(role, obs, action)` | 1.0 | LLM writes a fresh **in-character** line each turn (cop heroic + implies its cell; thief sly + cryptic) | In `nl_protocol/{prompt_templates,nl_speak}.py`; enabled with a real key + `llm.creative_speech`; falls back to B3 on empty/error. Lesson: constrain length + position-disclosure per role so the opponent's B2 interpret still works while phrasing stays varied. |

## C. Recommended practices (running list)
- Treat the submission guidelines as authoritative; restate constraints in each prompt.
- Prefer config-driven values over hardcoding (recipients, scopes, ports, limits).
- Ask for tests-first (TDD) and ≤150-line files explicitly.
- Keep secrets out of prompts and out of the repo.
