# Contributing

Keep every lab small, inspectable, and runnable with the Python standard
library. A change should preserve this shape:

```text
projects/NN-topic/
├── README.md
├── starter.py
├── solution.py
└── test_solution.py
```

Before opening a pull request:

```sh
python3 scripts/check_structure.py
python3 scripts/test_all.py
```

Add a failing test for the behavior you intend to change, implement the smallest
clear solution, and document what the tests do **not** prove. Use synthetic data
only; do not commit credentials, personal data, or paid-provider dependencies.
