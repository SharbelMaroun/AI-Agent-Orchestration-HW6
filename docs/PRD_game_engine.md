# Specialized PRD — Game Engine (Board, State Machine, Scoring, Barriers)

**Mechanism:** Authoritative pursuit-game rules engine
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)

---

## 1. Description & Theoretical Background
The game engine is the **single source of truth** for the Cop-&-Thief pursuit. It is a deterministic
**finite state machine** over a 2-D grid: state advances every turn as agents move or place barriers.
Formally the dynamics correspond to the transition function `P` of the Dec-POMDP
`⟨n, S, {Aᵢ}, P, R, {Oᵢ}, O, γ⟩` (n=2). The engine validates legality, detects capture/survival,
and computes reward `R` (the scoring table). Agents only *propose* actions; the engine accepts or
rejects them, preventing desync or cheating.

## 2. Inputs / Outputs / Setup

### 2.1 Input
- `actor ∈ {cop, thief}` and a proposed `Action`:
  `MOVE(dx, dy)` with `dx,dy ∈ {-1,0,1}` (not both 0) · `PLACE_BARRIER` (cop only) · `STAY`.
- Current authoritative `GameState`.

### 2.2 Output
- `TurnResult(actor, action, event, state)` where
  `event ∈ {NONE, CAPTURE, BARRIER_PLACED, ILLEGAL, MAX_MOVES_REACHED}`.
- `SubGameResult(index, winner, moves_used, cop_score, thief_score)`.

### 2.3 Setup (from `config/config.json`, never hard-coded)
`grid_size` (default `[5,5]`) · `max_moves` (25) · `num_games` (6) · `max_barriers` (5) ·
`scoring.{cop_win:20, thief_win:10, cop_loss:5, thief_loss:5}`.

## 3. Rules (authoritative)
1. **Grid:** `W×H` cells; coordinates `(x,y)`, `0 ≤ x < W`, `0 ≤ y < H`.
2. **Movement:** 8-directional (orthogonal + diagonal), one cell per turn; cannot enter a barrier or
   leave the board.
3. **Turn order:** thief moves first, then cop, alternating.
4. **Barriers (the cop's "special action"):** a turn is either a relocation (`MOVE`) **or** a special
   action; the engine's one special action is `PLACE_BARRIER` — the cop seals its current cell *instead*
   of moving; that cell becomes impassable to both agents. Max `max_barriers` per game; thief cannot place
   barriers. (The assignment's generic "change location or perform a special action" maps to MOVE vs
   PLACE_BARRIER here; additional special actions are a documented extension point — C14.)
5. **Cop win:** cop occupies the thief's exact cell (capture).
6. **Thief win:** thief survives `max_moves` turns without capture.
7. **Sub-game:** ≤ `max_moves` moves. **Match:** `num_games` sub-games; scores accumulate.

## 4. Scoring
| Outcome | Cop | Thief |
|---|---|---|
| Cop wins | `cop_win` (20) | `thief_loss` (5) |
| Thief wins | `cop_loss` (5) | `thief_win` (10) |

Match total range: **30–90**. Scoring reads values from config; no literals in code.

### 4.1 Match role structure (⚠️ confirm with course staff)
The assignment derives the **max 90 = 3×20 (cop) + 3×10 (thief)**, which implies that within one
internal 6-sub-game match the group is credited for **Cop performance in 3 sub-games and Thief
performance in 3** (mirroring the inter-group bonus's 3+3 role swap), and totals are tracked
**separately** as `totals.cop` and `totals.thief`. The engine must therefore support a **per-sub-game
role assignment** (which of the group's two agents is scored as cop vs thief), config-driven, rather
than assuming one fixed Cop vs one fixed Thief for all 6. The exact internal-match accumulation rule is
ambiguous in the source — **verify with staff** before finalizing `scoring.py`/`accumulator.py`.

## 5. Performance Metrics
- Single `apply()` is O(1) w.r.t. grid size (constant-time neighbour/bounds/barrier checks).
- A full 5×5, 25-move sub-game completes engine-side in well under 1 ms (excluding LLM latency).

## 6. Constraints & Limitations
- Engine is synchronous and deterministic given a seed (random start positions use a seeded RNG for reproducibility).
- No diagonal "corner cutting" rule beyond barrier-occupied target cells (documented assumption).
- Generic over grid size to support sanity sweeps (2×2 → 3×3 → 4×4 → 5×5).

## 7. Alternatives Considered
- **Agent-authoritative state** (each agent tracks its own board): rejected — desync & cheating risk.
- **4-directional movement:** rejected — assignment permits diagonal movement.
- **Continuous space:** rejected — out of scope; grid is specified.

## 8. Success Criteria & Test Scenarios
- **S1:** Cop adjacent (incl. diagonal) to thief can capture in one move → `event=CAPTURE`, cop_win scored.
- **S2:** Thief reaches `max_moves` uncaptured → `event=MAX_MOVES_REACHED`, thief_win scored.
- **S3:** Illegal move (off-board / into barrier / both deltas 0 when MOVE) → `event=ILLEGAL`, state unchanged.
- **S4:** 6th barrier attempt rejected; barrier cell blocks both agents.
- **S5:** Match of 6 sub-games accumulates a total within [30, 90].
- **S6:** Sanity sweep: engine behaves correctly at 2×2, 3×3, 4×4, 5×5 from config alone.
- Coverage for this module ≥85%, including all `event` branches and boundary cells.
