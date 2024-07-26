from .expense import Expense
from .budget import Budget
from .metadata import Metadata
from ..utils import DomainEntry

class Pocket(DomainEntry):
    name: str
    budgets: list[Budget]
    total_limit: int
    version: int
    metadata: Metadata

    def __init__(
        self,
        name: str,
        total_limit: int,
        budgets: list[Budget],
        metadata: Metadata,
        id: str | None = None,
    ) -> None:
        super().__init__(id)
        self.name = name
        self.budgets = budgets
        self.total_limit = total_limit
        self.metadata = metadata

    def add_expense(self, expense: Expense):
        for budget in self.budgets:
            budget.add_expense(expense)

    def add_budget(self, budget: Budget):
        self.budgets.append(budget)

    def reproduce(self) -> "Pocket":
        metadata = self.metadata.reproduce()
        budgets = [budget.reproduce() for budget in self.budgets]
        return Pocket(self.name, self.total_limit, budgets=budgets, metadata=metadata)
