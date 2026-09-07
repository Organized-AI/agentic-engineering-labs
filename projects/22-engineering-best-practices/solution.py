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
    """Score every block on evidence; name the weakest and the fix-first list."""
    results = []
    for block in blocks:
        ok, evidence = check_block(block, repo_report)
        results.append({"block": block, "ok": ok, "evidence": evidence})
    failing = [r["block"] for r in results if not r["ok"]]
    return {
        "results": results,
        "weakest": failing[0] if failing else None,   # dependency order = block order
        "fix_first": failing,
        "passes": not failing,
    }

if __name__ == "__main__":
    report = {
        "prompt_in_git": True,
        "tests_run_in_ci": True,
        "rollback_documented": False,
        "reviewed_commits_pct": 90,
        "adr_count": 3,
        "alerts_have_owners": True,
        "secrets_in_manager": True,
    }
    result = audit(report)
    for r in result["results"]:
        print("PASS" if r["ok"] else "FAIL", r["evidence"])
    print("WEAKEST", result["weakest"], "| FIX FIRST", result["fix_first"])
