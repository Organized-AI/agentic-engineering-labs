GATES = ((7, "fluency"), (30, "working knowledge"), (60, "judgment"), (90, "edge"))

class Ledger:
    def __init__(self, bet, date):
        """The dated opening bet every sprint gets graded against."""
        self.bet = bet
        self.date = date
        self.artifacts = {}

    def ship(self, day, artifact):
        """TODO: record an artifact at a gate day. Gates are ordered and required."""
        raise NotImplementedError

    def grade(self, day):
        """TODO: report gates cleared, gates open, and whether the bet still stands."""
        raise NotImplementedError
