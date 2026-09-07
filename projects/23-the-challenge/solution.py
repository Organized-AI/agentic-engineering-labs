GATES = ((7, "fluency"), (30, "working knowledge"), (60, "judgment"), (90, "edge"))

class Ledger:
    def __init__(self, bet, date):
        """The dated opening bet every sprint gets graded against."""
        self.bet = bet
        self.date = date
        self.artifacts = {}

    def ship(self, day, artifact):
        """Record an artifact at a gate day. Gates are ordered; earlier ones must hold first."""
        gate_days = [d for d, _ in GATES]
        if day not in gate_days:
            raise ValueError(f"day {day} is not a gate: {gate_days}")
        earlier = [d for d in gate_days if d < day]
        missing = [d for d in earlier if d not in self.artifacts]
        if missing:
            raise ValueError(f"gate {day} cannot ship before gate {missing[0]}")
        if not artifact:
            raise ValueError("no artifact, no level-up")
        self.artifacts[day] = artifact

    def grade(self, day):
        """Report gates cleared, gates open, and the state of the bet."""
        cleared = [(d, name) for d, name in GATES if d in self.artifacts]
        open_gates = [(d, name) for d, name in GATES if d not in self.artifacts and d <= day]
        complete = len(cleared) == len(GATES)
        return {
            "bet": self.bet,
            "bet_date": self.date,
            "cleared": cleared,
            "open": open_gates,
            "complete": complete,
            "verdict": "bet ready to grade" if complete else "bet still gathering evidence",
        }

if __name__ == "__main__":
    ledger = Ledger(bet="RAG beats fine-tuning at our scale", date="2026-09-06")
    ledger.ship(7, "one-page map of open questions")
    ledger.ship(30, "working build + failure log")
    print(ledger.grade(30)["verdict"], "| cleared:", ledger.grade(30)["cleared"])
    try:
        ledger.ship(90, "published benchmark")
    except ValueError as e:
        print("REJECTED skip-ahead -", e)
    ledger.ship(60, "self design-review with trade-offs")
    ledger.ship(90, "published benchmark")
    final = ledger.grade(90)
    print(final["verdict"], "| bet from", final["bet_date"], ":", final["bet"])
