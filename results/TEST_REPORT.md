# Automated Test Report

Per guidelines §6.4 — documented expected results, an automated pass/fail report, and saved run logs.

## How to run / regenerate
```bash
uv run pytest                 # runs the suite; writes the artifacts below
uv run ruff check src tests   # style gate (must be zero violations)
# optional HTML coverage:
uv run pytest --cov-report=html:results/htmlcov   # open results/htmlcov/index.html
```

## Artifacts (written to `results/` on every `uv run pytest`)
| File | Contents |
|---|---|
| `results/junit.xml` | Machine-readable JUnit report — pass/fail + timing per test (CI-consumable). *Generated; git-ignored.* |
| `results/coverage.xml` | Cobertura coverage report. *Generated; git-ignored.* |
| `results/test_run.log` | Captured console output of a successful run (committed evidence). |
| `results/htmlcov/` | Optional HTML coverage browser (on demand; git-ignored). |

## Expected result (Definition of Done)
- **189 tests, all PASS**, in ~20–25 s.
- **Coverage = 100%** statement **and** branch on all counted modules (`fail_under = 85`; suite fails below).
  Coverage-omitted (by design, see `pyproject.toml`): `main.py`, `__main__.py`, `mcp/servers.py`,
  `shared/google_auth.py`, `shared/openai_backend.py`, `gui/*` (these are entrypoints / thin I/O / drawing,
  exercised by smoke tests but not counted).
- **Ruff: 0 violations** (`E,F,W,I,N,UP,B,C4,SIM`, line-length 100, py310).

## Expected results by area (what each suite asserts)
| Area | Test files | Expected behaviour verified |
|---|---|---|
| Game engine / rules | `test_game_engine`, `test_board`, `test_barriers`, `test_scoring` | legal-move generation, capture/timeout, barrier budget, scoring table |
| Strategy | `test_heuristic`, `test_smart_cop`, `test_smart_thief` | greedy + cornering cop (100% vs greedy thief), smart thief evasion (roams, not wall-hugging) |
| Orchestration / SDK | `test_orchestrator`, `test_sdk`, `test_turn_pipeline`, `test_match_flow` | full match runs, deterministic per seed, policy selection + unknown-rejection |
| NL communication | `test_nl_protocol`, `test_nl_decider`, `test_nl_match*` | encode/interpret, LLM speech + template fallback, belief update, full NL match |
| MCP | `test_tool_service`, `test_message_bus`, `test_mcp_servers` | 6 tools/server, turn-ownership, FIFO bus |
| Gatekeeper | `test_gatekeeper*`, `test_rate_limit` | rate limit, FIFO queue/backpressure, retries, concurrency, ticket-leak safety |
| Reporting / Google | `test_reporting`, `test_google_agent` | internal + inter-group JSON, read/extract/calendar/send (mocked) |
| GUI (smoke) | `test_gui` | renderer/animator/live-viewer produce output without a display |

## Failure handling
A failing run leaves the same artifacts with the failures recorded in `junit.xml` (`<failure>` nodes) and
the console traceback in `test_run.log`; coverage below 85% fails the run regardless of test outcomes.
