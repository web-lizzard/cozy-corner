from ..utils import DomainEntry

class Expense(DomainEntry):
    value: int
    category_id: str

    def __init__(self, value: int, category_id: str, id: str | None = None) -> None:
        super().__init__(id)
        self.category_id = category_id
        self.value = value

    def match_category(self, category_id: str) -> bool:
        return self.category_id == category_id
