# Edge-Case & Fault Register

Per guidelines §6.3 — every module's boundary conditions as **boundary condition | input | expected
response**. Each row is exercised by a test (see `results/TEST_REPORT.md`); the system **never crashes** on
bad input — it degrades gracefully.

## Game engine / board (`services/game_engine.py`, `board.py`, `barriers.py`)
| Boundary condition | Input | Expected response |
|---|---|---|
| Move off the board | step beyond `[0,W)×[0,H)` | rejected as `ILLEGAL`; state unchanged |
| Move into a barrier / occupied wall cell | step onto a barrier cell | `ILLEGAL`; state unchanged |
| Non-unit / multi-cell move | `dx` or `dy` ∉ {-1,0,1} | `ILLEGAL`; state unchanged |
| Barrier budget exhausted | place beyond `max_barriers` | `ILLEGAL`; no barrier added |
| Thief attempts a barrier | thief `PLACE_BARRIER` | not a legal action for the thief |
| Action after game over | apply on a terminal state | `ILLEGAL`; winner/done preserved |
| Agent fully boxed in | no passable neighbour | only `STAY` is legal |
| Non-square board | `grid_size=[3,2]` | engine generic over W×H (no square assumption) |

## Strategy (`strategy/heuristic.py`, `smart_cop.py`, `smart_thief.py`, `evasion.py`)
| Boundary condition | Input | Expected response |
|---|---|---|
| No legal move | boxed-in agent | decider returns `STAY` (never errors) |
| Distance ties (greedy thief) | open board | **known limitation**: drifts one direction → use `smart` thief (default) |
| Smart thief at a wall/corner | edge/corner start | ranks by mobility/centrality → heads into open space |
| Unknown strategy name | `strategy.type`/`thief_type` invalid | `ValueError` with the allowed set |

## NL communication (`nl_protocol/*`)
| Boundary condition | Input | Expected response |
|---|---|---|
| Unparseable / no-coordinate message | free text without `x,y` | keep prior belief (no crash) |
| Out-of-bounds coordinate parsed | `"99,99"` on 5×5 | rejected by bounds check; keep prior belief |
| LLM provider error during interpret | backend raises | caught; keep prior belief |
| LLM returns empty/blank speech | `""` from backend | fall back to the deterministic template |
| Opponent directly visible | within `visibility_radius` | observation overrides any message |

## Gatekeeper (`shared/gatekeeper.py`, `rate_limit.py`)
| Boundary condition | Input | Expected response |
|---|---|---|
| Rate limit exceeded | calls > `requests_per_minute` | callers wait (FIFO); none rejected |
| Queue over `max_queue_depth` | bursty overflow | enqueued + **backpressure alert**; still served, then drained |
| Transient call failure | backend raises | retried with backoff up to `max_retries`, then re-raised |
| Ctrl-C while waiting | interrupt during sleep | ticket abandoned so the FIFO never stalls |
| Wrong config version | `rate_limits.json` version mismatch | `ConfigError` on load |

## Config & secrets (`shared/config.py`)
| Boundary condition | Input | Expected response |
|---|---|---|
| Missing config file | absent `config.json` | `ConfigError` (clear path) |
| Malformed JSON | invalid syntax | `ConfigError` (wraps `JSONDecodeError`) |
| Missing / mismatched `version` | no/old version key | `ConfigError` |
| Missing optional key | e.g. no `seed` | sensible default (e.g. seed 0) |

## Google agent (`services/google_agent/*`) — mocked in tests
| Boundary condition | Input | Expected response |
|---|---|---|
| Non-invite email | text without a meeting | `extract_meeting` returns `None` (no crash) |
| Missing title/start/end | partial extraction | returns `None` (no event created) |
| Empty inbox | no messages | `read_emails` returns `[]` |
| Expired/missing OAuth token | stale `token.json` | documented re-consent path (delete → re-run) |

## GUI (`gui/*`) — render-only
| Boundary condition | Input | Expected response |
|---|---|---|
| Interactive backend unavailable | no `TkAgg` | config `gui.live_backend` selects another (e.g. `QtAgg`) |
| Long NL message | many words | wrapped inside the speech bubble; margins reserved so it isn't clipped |
| Blocking turn (LLM call) in live view | slow provider | turn computed on a worker thread → window stays responsive |
