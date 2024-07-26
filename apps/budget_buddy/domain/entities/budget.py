from .expense import Expense
from ..utils import DomainEntry

class Budget(DomainEntry):
    name: str
    categories: list[str]
    expenses: list[Expense]

    def __init__(
        self,
        name: str,
        categories: list[str],
        expenses: list[Expense],
        id: str | None = None,
    ) -> None:
        super().__init__(id)
        self.name = name
        self.categories = categories
        self.expenses = expenses

    def add_expense(self, expense: Expense):
        if any(expense.match_category(category) for category in self.categories):
            self.expenses.append(expense)

    def reproduce(self) -> "Budget":
        return Budget(name=self.name, categories=self.categories, expenses=[])
