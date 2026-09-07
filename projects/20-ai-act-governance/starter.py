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
    """TODO: return the strictest matching class. Default is minimal."""
    raise NotImplementedError

def assign(cls, role):
    """TODO: duties for this class, tagged provider or deployer by role."""
    raise NotImplementedError

def map_artifacts(duties, artifacts=ARTIFACTS):
    """TODO: map each duty to its evidence. Raise on any unmapped duty."""
    raise NotImplementedError
