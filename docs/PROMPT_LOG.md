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
| A3 | 2026-06-25 | Lecturer rule: 550+ tasks | "Rewrite TODO with 550+ tasks." | `docs/TODO.md` = 604 granular tasks | Generate via template (per-module TDD lifecycle) for consistent IDs. |
| _…_ | | | | | |

## B. Runtime agent prompts (in-game LLM)
> Filled when `prompt_templates.py` is implemented (Phase 5). Track each template + version.

| # | Template | Version | Goal | Notes / improvements |
|---|----------|---------|------|----------------------|
| B1 | system prompt | _TBD_ | Frame the Dec-POMDP pursuit, partial observation, NL-only rule | _TBD_ |
| B2 | cop prompt | _TBD_ | Infer thief cell, pursue/place barrier | _TBD_ |
| B3 | thief prompt | _TBD_ | Evade, optionally deceive | _TBD_ |
| B4 | meeting-extraction prompt | _TBD_ | Extract meeting + time from an email | _TBD_ |

## C. Recommended practices (running list)
- Treat the submission guidelines as authoritative; restate constraints in each prompt.
- Prefer config-driven values over hardcoding (recipients, scopes, ports, limits).
- Ask for tests-first (TDD) and ≤150-line files explicitly.
- Keep secrets out of prompts and out of the repo.
