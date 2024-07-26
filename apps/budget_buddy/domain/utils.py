from uuid import uuid4
from typing import Protocol
from datetime import datetime, timedelta


class DomainEntry:
    id: str

    def __init__(self, id: str | None = None) -> None:
        self.id = id if id else str(uuid4())


class DateTimeCalculator(Protocol):
    def calculate(self, old_date: datetime) -> tuple[datetime, datetime]:
        ...


class DummyCalculator:
    def calculate(self, old_date: datetime) -> tuple[datetime, datetime]:
        new_date = old_date + timedelta(days=30)

        return old_date, new_date
