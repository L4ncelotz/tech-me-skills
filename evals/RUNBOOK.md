# Scenario-based evaluation runbook

The fixtures in `scenarios.json` test *behaviors*, not deterministic architecture answers. Several stacks can be defensible for the same scenario; judge whether the recommendation satisfies constraints, reasons accurately, and avoids bias.

## Paired baseline vs Tech-Me

1. Select an agent/model and record its version, tool availability and date. Use the same configuration for both conditions.
2. Start two fresh sessions with **no shared prior context**. In the baseline, do not load Tech-Me; in the skill-enabled session, ensure Tech-Me is actually enabled. For explicit activation tests, invoke Tech-Me as the scenario directs.
3. Give identical scenario prompt and `context`. For multi-turn interviews, use the **same predetermined follow-up answers** in both conditions; avoid unconsciously favoring one.
4. If an agent cannot honor the tooling condition, label the run invalid or adapt both conditions equally, and explain the change.
5. Have a reviewer who doesn't know which condition produced which transcript score applicable dimensions using `RUBRIC.md` where practical. If unblinding is unavoidable, disclose it.
6. Record observations and all critical failures. Do not report aggregate improvement from one cherry-picked answer.
7. Run multiple trials / models / agents if feasible; report sample size, variability and limitations. Separate **format/spec validation** from **behavior evaluation**.

## Multi-turn scenarios

Fixtures containing a `turns` array define a scripted interview: `user_prompt` opens the conversation and each `turns` entry is the user's next reply, sent in order.

1. Use the identical script in both conditions (baseline and Tech-Me) and send each reply in order, one per turn.
2. Score the **whole transcript** against `expected_behaviors` and `failure_signals`, not only the first response.
3. Stopping discipline is the primary target: at trigger turns such as "recommend now" or "that's enough", the session must deliver the recommendation instead of continuing to question, and must not re-ask constraints already answered earlier in the exchange.

## Evaluate relevant conditions

- **Bias**: keep requirements identical while changing only stated prior-stack familiarity; check whether the recommendation changes solely due to familiarity or legitimately through support/learning costs.
- **Discovery**: evaluate question relevance, repetition, and stopping behavior; question *count alone* is not a quality metric.
- **Unknowns**: verify each default is provisional and no precise numbers are invented.
- **Existing systems**: distinguish observed repository findings from claims in user prompts or prior memory.
- **Risk-sensitive facts**: verify sources independently when available; do not infer accuracy from confident wording.
- **Permission**: verify no file writes or unsolicited tool execution took place.

## Suggested release gate

Before tagging a release:

- Run `python scripts/validate_repo.py`.
- Run `python -m unittest discover -s tests -v`.
- Optionally run `skills-ref validate ./skills/tech-me` if upstream CLI is installed.
- Perform at least one baseline/skill-enabled review for the scenario categories affected by the change.
- Keep the "**Scenario coverage:** N of M fixture scenarios" line in `RESULTS.md` in sync with `evals/scenarios.json`; `scripts/validate_repo.py` rejects drifts in both directions.
- Publish honest observations, regressions and limitations, not a fabricated pass percentage.

**Note:** The local Python tests validate files and fixtures. They do not run an LLM, assess agent reasoning, or certify Claude Code/Codex/Cursor/OpenCode behavior.
