# Specialized PRD — Natural-Language Communication & Ambiguity Handling

**Mechanism:** Free-text inter-agent messaging + belief update under partial observation
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)

---

## 1. Description & Theoretical Background
The **central graded capability** is communication & orchestration — not winning strategy. Agents are
autonomous and exchange **natural language**, not raw coordinates or a rigid protocol. As long as they
understand each other, the internal implementation is free. The setting is a **Dec-POMDP** with
**partial observation**: each agent sees only a local view and must **infer** the opponent's position
from (a) its own observation and (b) the opponent's possibly-deceptive free-text messages.

Each turn the active agent produces a message describing **intentions, observations, or attempts at
deception**. The recipient reads it via an MCP tool, interprets it with the LLM, updates its **belief**
over opponent location, and chooses its next action.

## 2. Inputs / Outputs / Setup

### 2.1 Encode (intent → text)
- **Input:** actor role, current observation, belief, chosen action/strategy hint.
- **Output:** a short free-text `Message` (may bluff/mislead for the Thief).

### 2.2 Decode (text → belief update)
- **Input:** inbound `Message`, own observation, prior belief.
- **Output:** an updated **single most-likely opponent cell** (`Position | None`) — **never a crash**.

### 2.3 Setup
- Prompt templates (system + per-role) versioned in the repo and logged in the prompt-engineering log.
- LLM access via `llm_client.py`, which calls the provider **through the gatekeeper**.

## 3. Belief Model
- Maintain the belief as a **single most-likely opponent cell** (`NLDecider.belief: Position | None`), not a distribution.
- Update by **precedence** (strongest evidence wins): `direct observation → message interpretation → prior`.
  Direct observation (opponent within the visibility radius) overrides any message; an unparseable/
  out-of-bounds message or an LLM error falls back to the prior (`nl_decode.interpret`).
- The Thief may emit deceptive messages → because observation outranks message in the precedence order,
  hard observation always dominates talk.
- *(Optional enrichment — see §7)* a full Bayesian posterior
  `belief' = normalize(prior ⊙ obs_likelihood ⊙ message_likelihood)` over all cells could replace the
  single-cell heuristic, but is **not implemented**.

## 4. Communication Challenges (addressed in README analysis)
- **Ambiguity:** vague/contradictory text → defensive parsing; fall back to prior belief; default to a
  safe action rather than failing.
- **Deception:** discount message evidence vs. direct observation; track consistency over turns.
- **No shared protocol:** rely on the LLM to map free text to structured belief; validate outputs.
- **Mutual understanding:** a brief, role-appropriate prompt contract is versioned as a template
  (`system_prompt`); note it is **not yet injected** into the live LLM call (only `interpret_prompt` is
  sent to the model today). Convergence currently relies on `interpret_prompt` + defensive parsing.

## 5. Performance Metrics
- **Parse robustness:** 100% of inbound messages produce a valid belief update (0 crashes).
- **Latency:** one decide() (encode+decode+action) within provider round-trip budget; bounded by gatekeeper.
- **Signal quality (research):** correlation between belief's top cell and true cell over turns.

## 6. Constraints & Limitations
- Output must be parseable defensively; the system tolerates malformed/empty/sarcastic messages.
- No out-of-band coordinate leakage — coordination must go through natural language.

## 7. Alternatives Considered
- **Rigid JSON coordinate protocol between agents:** rejected — defeats the assignment's purpose.
- **Rule-based keyword parser only (no LLM):** rejected — too brittle for free text; LLM is required.
- **Full Bayesian filter with exact likelihoods:** optional enrichment; heuristic belief is sufficient.

## 8. Success Criteria & Test Scenarios
- **S1:** Clear message ("I'm near the top-left, moving right") yields a belief shift toward that region.
- **S2:** Empty/garbled/contradictory message → no crash; belief falls back to prior; safe action chosen.
- **S3:** Deceptive Thief message that conflicts with Cop's direct observation → observation dominates.
- **S4:** Over a sub-game, the Cop's top-belief cell converges toward the true Thief cell before capture.
- **S5:** All LLM calls are mocked in unit tests; ≥85% coverage of encode/decode/belief branches.
