> **The question:** When the agent misbehaves, how do you prove the model did it?

Colin McNamara runs one GH200 serving text, vision, speech, and a safety model behind a router, with Claude Code driving the text tier. His talk ["Your Harness Is the Other Half of the Model"](https://colinmcnamara.com/talks/harness) is a measurement diary of everything between the user and the weights - the serving engine, the router, the wire format, the benchmark script itself - lying to him in ways that looked, every single time, like the model's fault. This bonus chapter condenses his evidence into the guide's running theme: the harness is half the system, so attribution is a discipline, not a hunch. His full write-up, with every measurement, is linked in the sources.

## The mental model

Every failure has an address, and the default guess is wrong. When output degrades, the model is the visible suspect and the harness is the invisible one, so harness faults get filed as model findings. McNamara's list of disguises, each one measured on his own machine:

| It looked like | It was |
| --- | --- |
| The model fails long-context retrieval | His output cap |
| The model is bad at tools | A missing parser flag |
| Model A's benchmark numbers | Model B answering silently |
| A small context window | A flag with two meanings |
| The model cannot be terse | An unbounded reasoning budget |
| A memory-placement law | One machine's topology |
| The model's context budget | The engine not knowing its architecture |

Three of the first four would have been written down as findings about the model. That is the tax of skipping attribution: the field's folklore accumulates harness bugs as model weaknesses.

## The quiet failure is the expensive one

The loud failure is the easy one: the model refuses to load, you upgrade the engine, you move on. McNamara's costliest failure made no noise. A newer serving engine understood his model's hybrid attention - one full-attention layer in four, the rest cheap - and the old engine did not. Nothing errored. It passed needle retrieval at 231,000 tokens. It drove a working agent loop for weeks. He simply had three quarters less context than he thought.

The attribution came from a null result: after the engine upgrade, decode jumped 43 percent and the KV cache pool grew 3.75x - while prefill stayed flat at 6,266 versus 6,249 tokens per second. Prefill and decode load the same silicon in opposite ways, so overhead-elimination work lands on one and not the other. Had both moved, he would be hunting his own config. Because only the bandwidth-bound half moved, the serving stack took the blame. A number that did not move did the attribution.

## The instruments lie too

Two of his failures were in his own measurement. His router's complexity classifier scored 90 percent accuracy - against bare strings, a wire format no real client sends; the real client wraps prompts in literal quotes, which moved the score across his own routing boundary, and honest measurement said 75. And his cache-busting salt, appended at the end of the message, left the prefix byte-identical, so both machines served from cache and a 24x prefill gap read as near-parity. Salting the system message instead revealed the truth. Anyone can blame their tools. Both of these were his.

```python
# Pseudocode: attribution before remediation.
def diagnose(symptom, signals):
    # Signals that move together vs apart name the layer.
    if signals.prefill.flat and signals.decode.moved:
        return "serving stack"      # bandwidth-bound half changed
    if signals.endpoint.ok and not signals.agent_loop.ok:
        return "harness"            # cheap checks lie; run the full loop
    if signals.model_a_trace != signals.model_b_trace:
        return "silent swap"        # verify identity on the wire
    return "model"                  # reached only by elimination
```

## The Monday-morning rules

His practices, stated as the guide would state them. Engine version goes on the benchmark axis, not in the environment notes - it behaves like a variable, so record it like one. Test the full agent loop, not the endpoint: every cheap check passed while tool calling was silently broken. One variable at a time, even when it feels slow - two knobs he tuned partially cancel, and flipping both would have hidden that entirely. Re-test your tuning peaks when the model or the engine moves; both shifted his optimum by more than 40 percent. And the one that cost him the most: checking that a system does what it says is not checking that it is right.

His closer is the guide's first chapter wearing a hard hat: every control is a claim you are making, and the background of your benchmark is someone else's independent variable. Chapter 01's confounders do not retire when you graduate to infrastructure.

## Lab: hunt the quiet failure

Build the attribution bench: one served model behind an endpoint, with four harness faults planted under feature flags - a stale engine config that shrinks the context pool, a silent model swap at the router, a dropped nullable wire field that kills streams one event early, and a cache-salt mistake that flatters prefill numbers. Your tests get only black-box signals: endpoint checks, an agent-loop probe, prefill and decode rates, wire traces. The deliverable is a diagnosis table - for each planted fault, which signal named it, and which cheap check would have sworn everything was fine.

## Failure drills

Run the endpoint checks while the tool-calling fault is live and write down how many pass. Swap models at the router mid-suite and see whether your benchmark reports the change or the average. Move one token of salt and watch a 24x gap invert. Cap output tokens and let needle retrieval "fail" at a context length the model never reached. For each, name the signal that would have caught it - then check that signal exists in your own stack.

## Ship gate

No model finding ships without an attribution step: engine version recorded as a benchmark variable, identity verified on the wire, the full agent loop probed, and at least one signal expected to move held flat as the control. Harness faults are planted and hunted in the lab before they are diagnosed in production. The background of your benchmark gets audited like a dependency - which is the deepest version of the guide's whole method, and a fine place to attempt [the challenge](/agentic-eng/chapters/the-challenge/).

Sources: [Your Harness Is the Other Half of the Model (talk)](https://colinmcnamara.com/talks/harness), [the full write-up with every measurement](https://colinmcnamara.com/blog/engine-other-half-of-the-model) - Colin McNamara, Field CTO at AHEAD, organizer of AIMUG, Austin LangChain / AIMUG, September 2026.
