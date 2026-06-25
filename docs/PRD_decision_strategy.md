# Specialized PRD — Decision Strategy (Heuristic + Optional Tabular Q-Learning)

**Mechanism:** Action-selection policy for Cop and Thief
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)

---

## 1. Description & Theoretical Background
Each agent must choose an action each turn from its belief + observation. Per the assignment, a
**heuristic / decision-tree / prompt-engineering** strategy is fully acceptable; reinforcement
learning is **optional enrichment**. We specify a default **heuristic** policy and an **optional
Tabular Q-Learning** policy behind a common `Strategy` interface (Template Method), so either can be
selected from config without code changes.

### 1.1 Optional RL background (Tabular Q-Learning)
- **State (s):** agent's discretized situation (e.g., own cell + belief summary of opponent cell).
- **Action (a):** a legal move/barrier.
- **Reward (r):** small step cost; large reward for capture (cop) / survival (thief).
- **Bellman update:** `Q(s,a) ← Q(s,a) + α · [ r + γ · maxₐ' Q(s',a') − Q(s,a) ]`.
- **Policy:** ε-greedy (explore vs. exploit). Hyper-params: `α ∈ [0.01, 0.5]`, `γ ∈ [0,1]`.

## 2. Inputs / Outputs / Setup

### 2.1 Interface (`Strategy`)
- **Input:** `observation`, `belief`, `legal_actions`, `game_status`.
- **Output:** a single chosen `Action` (+ optional message hint for the NL layer).

### 2.2 Setup (from config)
- `strategy.type ∈ {"heuristic", "smart"}` (default `heuristic`) selects the **cop**;
  `strategy.thief_type ∈ {"greedy", "smart"}` (default `smart`) selects the **thief**. A Tabular
  Q-Learning policy (`q_table`) with RL hyper-params is **design-only / pending** — not wired into the
  `Orchestrator`. The `Orchestrator`/`select_*_policy` reject any unknown value with a clear error.
  Defaults documented; nothing hard-coded.

## 3. Default Heuristic Policy
- **Cop (`heuristic`):** move to minimize Chebyshev distance to the belief's most-likely Thief cell.
- **Thief (`greedy`):** move to maximize Chebyshev distance from the Cop. **Limitation:** distance ties
  on an open board are common, and a fixed direction-order tie-break makes the Thief **hug one wall**
  ("always goes left") — visibly un-smart. Superseded as the default by §3.2.

### 3.1 Cornering Cop Policy (`smart`, implemented Phase 4)
The greedy cop above only minimizes distance, so against an equal-speed evader on an open board the two
**mirror each other into a limit cycle** and the Thief survives the move cap (README R.3; greedy ≈ 0.72
on 5×5, dropping to ≈ 0.62 on 6×6). The `smart` cop fixes this with a **one-ply look-ahead**:
- For each legal Cop action, simulate it, then simulate the **Thief's greedy evasion**, and rank the
  resulting position **lexicographically by `(Chebyshev distance, Thief escape-options)`** — where an
  *escape option* is a Thief move that strictly increases its distance from the Cop. An immediate
  capture short-circuits to that action.
- Minimizing escape options **herds the Thief into a corner**, where the board edges act as walls and
  its mobility collapses, so the Cop closes the final gap. Measured **capture rate = 1.00** on 3×3–7×7.

### 3.2 Smart Thief Evasion (`smart`, implemented; default thief)
The greedy thief (§3) drifts into a wall because every distance-tie resolves to the same direction.
`smart_thief_action` (and the NL thief's `_choose`) instead rank candidate cells by
**`evade_key = (distance from cop, own mobility, centrality)`** (`strategy/evasion.py`): flee the cop,
break ties toward **open space** (most passable neighbours), then toward the **centre** (most escape
room). The thief now uses the whole board and is markedly harder to corner. It is the **default**
(`strategy.thief_type = "smart"`); the `greedy` thief is retained as the controlled baseline for the
cop comparison in §4 / README R.3.

**Barrier analysis (why cornering, not walls).** In this engine `place_barrier` seals the **Cop's own
cell** and costs a full turn (the Cop does not move). It therefore cannot block the cell a fleeing Thief
is moving *toward*, so wall-building is a weak, tempo-negative lever; geometric cornering dominates. The
`smart` policy still includes `place_barrier` in its action search, so it is used only if it ever scores
best. (Stronger barrier use would need an engine that lets the Cop place barriers on adjacent cells.)

## 4. Performance Metrics
- **Measured today (README R.3):** greedy `heuristic` cop ≈ 0.72 capture and the cornering `smart` cop
  **1.00** vs. the **greedy** thief (5×5; 100% on 3×3–7×7) — the controlled baseline comparison.
- **Cornering cop vs. the new `smart` thief (default):** the smarter evader is genuinely harder to corner —
  capture drops to **1.00 (3×3), 1.00 (4×4), 0.90 (5×5), 0.88 (6×6), 0.47 (7×7)** (40 seeds each). The
  cop's one-ply look-ahead still *models* a greedy thief; making it model the smart thief is noted future work.
- **Decision latency:** action chosen in O(grid cells) time, negligible vs. LLM latency.
- **(RL) learning curve — contingent on the optional Q-learning track (§1.1, §7):** if `q_table` is
  implemented, average reward per episode should trend upward and the curve would be recorded in the
  README. _Not implemented, so no learning curve is recorded yet._

## 5. Constraints & Limitations
- RL is **optional**; the project must be fully functional with the heuristic alone.
- Q-table size grows with the discretized state space → keep the state compact (esp. on 5×5).
- Strategy proposes; the **engine validates** legality (no illegal action can be forced).

## 6. Alternatives Considered
- **Deep RL / DQN:** rejected — out of scope; tabular is the optional ceiling; no heavy compute needed.
- **Pure LLM prompt-only decisions:** acceptable variant; we keep a deterministic heuristic for
  testability and as a fallback when the LLM is unavailable.
- **Minimax/expectimax search:** the `smart` cop (§3.1) is a shallow (one-ply) instance of this —
  deeper search is possible enrichment but unnecessary once capture rate is already 1.00.

## 7. Success Criteria & Test Scenarios
- **S1:** With a known belief, the Cop heuristic strictly decreases distance to the target cell.
- **S2:** The Thief heuristic never steps into a one-cell dead-end when an alternative exists.
- **S3:** Strategy selection switches between `heuristic` and `smart` purely via config; an unknown
  type (e.g. `"q_table"`, not yet implemented) is rejected with a clear error.
- **S4:** The `smart` cop captures the greedy Thief within the move cap on every sampled seed (5×5);
  it takes an immediate capture when one is available and stays when fully boxed in.
- **S5 (optional):** Q-update matches the Bellman formula on a hand-computed example (unit test).
- **S6:** All policy branches covered; module ≥85% coverage; files ≤150 lines.
