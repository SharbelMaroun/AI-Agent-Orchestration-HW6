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
- `strategy.type ∈ {"heuristic", "q_table"}`, plus RL hyper-params (`learning_rate`, `discount_factor`,
  `epsilon`) when `q_table` is selected. Defaults documented; nothing hard-coded.

## 3. Default Heuristic Policy
- **Cop:** move to minimize Chebyshev distance to the belief's most-likely Thief cell; place a barrier
  when it provably reduces the Thief's escape options and barriers remain.
- **Thief:** move to maximize minimum distance to the Cop / toward the largest open region; avoid
  dead-ends created by barriers.

## 4. Performance Metrics
- **Baseline dominance:** heuristic beats a random policy in head-to-head tests (win-rate > 50%).
- **Decision latency:** action chosen in O(grid cells) time, negligible vs. LLM latency.
- **(RL) learning curve:** average reward per episode trends upward; recorded for the README.

## 5. Constraints & Limitations
- RL is **optional**; the project must be fully functional with the heuristic alone.
- Q-table size grows with the discretized state space → keep the state compact (esp. on 5×5).
- Strategy proposes; the **engine validates** legality (no illegal action can be forced).

## 6. Alternatives Considered
- **Deep RL / DQN:** rejected — out of scope; tabular is the optional ceiling; no heavy compute needed.
- **Pure LLM prompt-only decisions:** acceptable variant; we keep a deterministic heuristic for
  testability and as a fallback when the LLM is unavailable.
- **Minimax/expectimax search:** possible enrichment; heuristic chosen first for simplicity & speed.

## 7. Success Criteria & Test Scenarios
- **S1:** With a known belief, the Cop heuristic strictly decreases distance to the target cell.
- **S2:** The Thief heuristic never steps into a one-cell dead-end when an alternative exists.
- **S3:** Strategy selection switches between `heuristic` and `q_table` purely via config.
- **S4 (optional):** Q-update matches the Bellman formula on a hand-computed example (unit test).
- **S5:** All policy branches covered; module ≥85% coverage; files ≤150 lines.
