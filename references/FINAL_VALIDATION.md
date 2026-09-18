# Final validation

Root dispatches one Luna Validator after stable integration and scheduled review repair. The packet names stable inputs, acceptance criteria, required journeys, commands, environment assumptions and artifact locations. Validator confirms actual execution, skipped cases, integration assumptions and observable outcomes; UI, persistence and downstream effects are inspected when they matter.

Validator returns `PASS`, `FAIL` or `INCOMPLETE` with per-criterion evidence and bounded diagnostic facts. It does not alter product code, tests, baselines or acceptance criteria, and it does not create Scout. Root assigns repairs separately and reruns only evidence invalidated by the repair. After final validation, Root dispatches Terra Gate for final stage/capability acceptance. Gate may use Scout only for bounded factual reconnaissance, does not implement or repair, and returns the final decision for Root to act on and report.
