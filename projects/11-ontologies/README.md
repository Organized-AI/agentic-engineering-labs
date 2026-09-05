# 11 — Source-Backed Domain Graph

Resolve canonical event facts from explicit relationships, provenance, approval,
and effective time. Keep authorization outside the graph.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

## Challenge

Implement canonical venue resolution in `starter.py`. A fluent label match is
not enough: use the event relationship and select an approved fact valid at the
requested time.

## Extension

Represent the graph as RDF, add SHACL validation, and compare it with a simple
relational schema. Document which concrete query justifies each new technology.
