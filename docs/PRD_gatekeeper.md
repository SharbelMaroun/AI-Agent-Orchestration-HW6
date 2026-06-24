# Specialized PRD — Centralized API Gatekeeper & Rate Limiting

**Mechanism:** Single chokepoint for all external API calls (LLM + Gmail)
**Document version:** 1.00
**Parent:** [`PRD.md`](PRD.md) · **Design:** [`PLAN.md`](PLAN.md)

---

## 1. Description & Theoretical Background
Per the submission guidelines, **all external API calls must pass through a centralized gatekeeper**.
No service may call a provider directly. The gatekeeper enforces **rate limiting**, **queueing on
overflow**, **retries on transient failures**, and **logging/monitoring** of every call. In this
project the gatekeeper fronts the **LLM provider** ([`PRD_nl_communication.md`](PRD_nl_communication.md))
and the **Gmail API** ([`PRD_email_reporting.md`](PRD_email_reporting.md)).

## 2. Interface
```python
class ApiGatekeeper:
    """Centralized API call manager."""
    def __init__(self, config: RateLimitConfig): ...
    def execute(self, api_call, *args, **kwargs):
        """Check rate limits -> queue if needed -> retry on transient failure -> log."""
    def get_queue_status(self) -> QueueStatus:
        """Return queue depth and stats."""
```

## 3. Inputs / Outputs / Setup

### 3.1 Input
- A callable `api_call` plus its args (e.g., the LLM request or Gmail send), and a logical `service`
  name used to select that service's limits.

### 3.2 Output
- The provider's result on success; a structured error after exhausting retries; a `QueueStatus`.

### 3.3 Setup — `config/rate_limits.json` (versioned, never hard-coded)
```json
{
  "rate_limits": {
    "version": "1.00",
    "services": {
      "default": {
        "requests_per_minute": 30,
        "requests_per_hour": 500,
        "concurrent_max": 5,
        "retry_after_seconds": 30,
        "max_retries": 3
      }
    }
  }
}
```
Per-service overrides (e.g., `llm`, `gmail`) may be added under `services`.

## 4. Required Behaviour
- **No direct API calls:** services delegate to `gatekeeper.execute`.
- **Rate limiting:** enforced *before* every call.
- **Queueing:** overflow is **queued, not rejected** — FIFO queue, max depth from config,
  **backpressure alert** when full, **drain** when the limit resets.
- **Retries:** transient failures retried up to `max_retries` with `retry_after_seconds` backoff.
- **Monitoring:** every call logged (service, latency, outcome, retry count) for cost/observability.

## 5. Performance Metrics
- **Throughput:** stays within configured RPM/RPH; zero provider-side 429s in normal runs.
- **Overhead:** gatekeeper wrapper adds < 5 ms per call (excluding network/provider time).
- **Cost tracking:** token/cost accounting available for the README's cost analysis.

## 6. Constraints & Limitations
- Limits and queue depth are **config-driven**; defaults allowed in code only as fallback constants.
- Thread-safety required if the orchestrator parallelizes calls (use locks / `queue.Queue`).

## 7. Alternatives Considered
- **Per-service ad-hoc rate limiting:** rejected — duplicated logic; violates DRY & the gatekeeper rule.
- **Reject-on-overflow:** rejected — guidelines require queueing, not crashing/rejecting.
- **Third-party API gateway service:** overkill for this scope; an in-process gatekeeper suffices.

## 8. Success Criteria & Test Scenarios
- **S1:** Calls beyond `requests_per_minute` are queued (FIFO), not rejected, then drained on reset.
- **S2:** A transient failure is retried up to `max_retries`; a permanent failure surfaces a clear error.
- **S3:** Queue-full triggers a backpressure alert via `get_queue_status`.
- **S4:** All limits load from `rate_limits.json`; changing the file changes behaviour with no code edit.
- **S5:** Every call is logged; unit tests mock the provider; ≥85% coverage; file ≤150 lines.
