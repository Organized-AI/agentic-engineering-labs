# 10 — Vector Kernel Correctness & Speedup

[Read the Kernels & Performance chapter →](https://guide.organizedai.vip/agentic-eng/chapters/kernels-and-performance/)

Write a blocked vector-add “kernel” in ordinary Python, verify awkward boundary
sizes, and calculate the maximum whole-system impact of a local speedup.

```sh
python3 -m unittest -v test_solution.py
python3 solution.py
```

This CPU simulation teaches indexing, masks, correctness, and Amdahl-style
reasoning. The guide links to Triton as an optional GPU extension.

## Challenge

Implement blocked vector addition and `overall_speedup()` in `starter.py`.
Never claim speed from a function that has not passed the reference checks.

## Extension

Port the operation to Triton on supported hardware. Record warmup, device,
software versions, data type, synchronization, and every input size tested.
