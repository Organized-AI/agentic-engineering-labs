# 04 — Policy-Aware Model Router

[Read the LLM Gateways chapter →](https://guide.organizedai.vip/agentic-eng/chapters/llm-gateways/)

Route fake model requests only among endpoints that satisfy the data policy,
reserve budget atomically, and use a fallback only when time and policy permit.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

No real provider is called. The fake providers let you test failures without
spending money or transmitting data.

## Challenge

Implement eligibility, budget reservation, and the route loop in `starter.py`.
An ineligible endpoint must receive zero calls—even as a fallback.

## Extension

Add quality-suite eligibility and uncertain-cost reconciliation after a timeout.
