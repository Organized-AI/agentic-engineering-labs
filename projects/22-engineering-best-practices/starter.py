BLOCKS = ("versioned", "loud_tests", "reversible_deploys", "review", "adrs", "telemetry", "secrets")

def check_block(block, repo_report):
    """Score one block from evidence in the repo report. Returns (ok, evidence)."""
    evidence = {
        "versioned": repo_report.get("prompt_in_git", False),
        "loud_tests": repo_report.get("tests_run_in_ci", False),
        "reversible_deploys": repo_report.get("rollback_documented", False),
        "review": repo_report.get("reviewed_commits_pct", 0) >= 80,
        "adrs": repo_report.get("adr_count", 0) > 0,
        "telemetry": repo_report.get("alerts_have_owners", False),
        "secrets": repo_report.get("secrets_in_manager", False),
    }
    ok = evidence[block]
    return ok, f"{block}: {'evidence found' if ok else 'no evidence'}"

def audit(repo_report, blocks=BLOCKS, threshold=1.0):
    """TODO: score every block, return weakest block and the fix-first list."""
    raise NotImplementedError
