"""Token-cost report for a natural-language match (README R.7).

Reproducible & offline: `uv run python scripts/token_report.py`. It runs a real NL
match with a *recording* backend that captures every prompt actually sent to the LLM
(`interpret_prompt`), counts input tokens from those prompts, models the short
interpret replies as output tokens, and prices the total at the config-driven
gpt-4o-mini rates. Writes results/token_cost.txt + a Markdown row for the README.

Exact billing should be read from the OpenAI API ``usage`` field on a keyed run;
this offline estimate uses the ~4-chars/token heuristic so it needs no network.
"""

from __future__ import annotations

from marl_cop_thief.services.nl_match import run_nl_match
from marl_cop_thief.shared.config import load_config
from marl_cop_thief.shared.token_cost import TokenUsage, cost_usd, estimate_tokens


def measure(config: dict) -> tuple[TokenUsage, dict]:
    """Run an offline match, capturing prompts, and return usage + the pricing block."""
    pricing = config["llm"]["pricing"]
    prompts: list[str] = []

    def recording(prompt: str) -> str:
        prompts.append(prompt)
        return prompt  # echo: realistic interpretation, so gameplay is representative

    run_nl_match(config, backend=recording)
    cpt = pricing["chars_per_token"]
    input_tokens = sum(estimate_tokens(p, cpt) for p in prompts)
    output_tokens = len(prompts) * pricing["est_output_tokens_per_call"]
    return TokenUsage(len(prompts), input_tokens, output_tokens), pricing


def main() -> None:
    config = load_config()
    usage, pricing = measure(config)
    model = config["llm"]["model"]
    total = cost_usd(usage, pricing)
    per_match = total  # one full match (num_games sub-games)

    row = (
        f"| {model} | {usage.input_tokens} | {usage.output_tokens} | "
        f"{pricing['input_per_1m']:.2f} | {pricing['output_per_1m']:.2f} | ${total:.6f} |"
    )
    lines = [
        "Token-cost report (offline estimate, ~4 chars/token; gpt-4o-mini list price)",
        "=" * 70,
        f"LLM calls (interpret) per match : {usage.calls}",
        f"Input tokens  (sum of prompts)  : {usage.input_tokens}",
        f"Output tokens (modelled replies): {usage.output_tokens}",
        f"Total tokens                    : {usage.total_tokens}",
        f"Cost per match                  : ${per_match:.6f}",
        f"Cost per 1000 matches           : ${per_match * 1000:.2f}",
        "",
        "README R.7 row:",
        row,
    ]
    with open("results/token_cost.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nWrote results/token_cost.txt")


if __name__ == "__main__":
    main()
