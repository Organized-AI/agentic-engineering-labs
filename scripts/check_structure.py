#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
projects = sorted((ROOT / "projects").glob("[0-9][0-9]-*"))
assert len(projects) == 23, f"expected 23 projects, found {len(projects)}"
for project in projects:
    for filename in ("README.md", "starter.py", "solution.py", "test_solution.py"):
        path = project / filename
        assert path.exists(), f"missing {path}"
    assert "TODO" in (project / "starter.py").read_text(), f"no TODO in {project}"
print("PASS: 23 projects with README, starter, solution, and tests.")
