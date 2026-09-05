#!/usr/bin/env python3
"""Run every reference project in an isolated subprocess."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
projects = sorted((ROOT / "projects").glob("[0-9][0-9]-*"))
failures = []
for project in projects:
    print(f"\n== {project.name} ==", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_solution.py"],
        cwd=project,
        check=False,
    )
    if result.returncode:
        failures.append(project.name)

print(f"\n{len(projects) - len(failures)}/{len(projects)} projects passed.")
if failures:
    print("Failed:", ", ".join(failures))
    raise SystemExit(1)
