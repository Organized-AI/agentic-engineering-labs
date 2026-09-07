from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    name: str
    scores_people: bool      # eligibility, credit, hiring-style decisions
    manipulates: bool        # subliminal or exploitative techniques
    generates_content: bool  # user-facing generated text or media

RULES = {
    "unacceptable": lambda p: p.manipulates,
    "high": lambda p: p.scores_people,
    "limited": lambda p: p.generates_content,
}

DUTIES = {
    "unacceptable": ("prohibited: do not deploy",),
    "high": ("risk management", "data governance", "human oversight", "conformity assessment"),
    "limited": ("transparency disclosure",),
    "minimal": (),
}

ARTIFACTS = {
    "risk management": "chapters/06 evaluations: release-gate reports",
    "data governance": "chapters/09 retention: persistence inventory",
    "human oversight": "chapters/15 oversight: approval queue audit",
    "conformity assessment": "chapters/20 governance: this memo, dated",
    "transparency disclosure": "chapters/02 foundations: generated-content labels",
}

def classify(profile, rules=RULES):
    """The strictest matching class wins; default is minimal."""
    for cls in ("unacceptable", "high", "limited"):
        if rules[cls](profile):
            return cls
    return "minimal"

def assign(cls, role):
    """Duties for the class, tagged with who carries them."""
    if role not in ("provider", "deployer"):
        raise ValueError("role must be provider or deployer")
    return [{"duty": d, "role": role} for d in DUTIES[cls]]

def map_artifacts(duties, artifacts=ARTIFACTS):
    """Map each duty to its evidence artifact. Unmapped duties fail the memo."""
    index = {}
    for item in duties:
        duty = item["duty"]
        if duty.startswith("prohibited"):
            index[duty] = "no artifact: deployment stops here"
            continue
        if duty not in artifacts:
            raise KeyError(f"no artifact evidences duty: {duty}")
        index[duty] = artifacts[duty]
    return index

if __name__ == "__main__":
    profile = Profile("event-ops assistant", scores_people=False, manipulates=False, generates_content=True)
    cls = classify(profile)
    print("CLASS", cls)
    duties = assign(cls, role="deployer")
    for duty, artifact in map_artifacts(duties).items():
        print(f"  {duty} -> {artifact}")
    dark = Profile("dark-pattern bot", scores_people=False, manipulates=True, generates_content=True)
    print("CLASS", classify(dark))
