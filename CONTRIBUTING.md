# Contributing to Tech-Me

Contributions are welcome, particularly focused improvements to question quality, bias resistance, architecture evaluation, and real-world test cases.

## Guidelines

1. Open an [issue](https://github.com/L4ncelotz/tech-me-skills/issues) describing the decision failure or missed scenario, when practical.
2. Keep `skills/tech-me/SKILL.md` focused and portable. Put lengthy guidance under `references/` instead.
3. Do not add a framework, cloud vendor, language, or MCP server requirement without a compelling cross-agent reason.
4. Add or update an `evals/scenarios.json` case for meaningful behavioral changes (tagging the `mode` field when adding or updating an invocation mode), including expected and undesired behavior.
5. Run `python scripts/validate_repo.py` and `python -m unittest discover -s tests -v` before opening a PR (the validator also enforces `.claude-plugin/plugin.json` version parity with the latest released `CHANGELOG.md` entry).
6. If the change alters behavior, summarize which human evaluation runs you performed; do not call lint results behavioral proof.

Please avoid real credentials, confidential project information, proprietary code, unlicensed third-party material, or personal data in example fixtures. Prefer a small reproducible scenario and avoid inventing current benchmark results.

## Pull requests

Describe the issue, proposed behavioral change, expected improvement, and possible regression. If your change introduces a new dependency or tool integration, explain the compatibility/fallback behavior.

## Documentation and localization

The core instructions are in English for broad compatibility. Tech-Me should respond in the user's language. Translated documentation contributions are welcome if they preserve technical meaning.
