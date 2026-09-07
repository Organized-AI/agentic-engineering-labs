"""Turn Loop Harness - implement assemble(), policy_check(), and run_turn()."""

BUDGET = 4096
APPROVED_RECIPIENTS = {"ops-team", "organizer"}


class StubModel:
    def __init__(self, proposals):
        self.proposals = list(proposals)
        self.seen_contexts = []

    def complete(self, context, tools):
        self.seen_contexts.append(context)
        return self.proposals.pop(0) if self.proposals else {"calls": [], "final_text": "done"}


def assemble(messages, budget=BUDGET):
    """Pack messages newest-first until the budget (in chars) is full."""
    raise NotImplementedError


def policy_check(call):
    """The single choke point: every effect passes here."""
    raise NotImplementedError


def run_turn(runtime, user_message):
    raise NotImplementedError


