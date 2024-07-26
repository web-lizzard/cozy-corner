from datetime import datetime
from ..utils import DomainEntry, DateTimeCalculator

class Metadata(DomainEntry):
    calculator: DateTimeCalculator
    start_date: datetime
    end_date: datetime

    def __init__(
        self,
        calculator: DateTimeCalculator,
        start_date: datetime,
        end_date: datetime,
        id: str | None = None,
    ) -> None:
        super().__init__(id)
        self.calculator = calculator
        self.start_date = start_date
        self.end_date = end_date

    def reproduce(self) -> "Metadata":
        start_date, end_date = self.calculate_next_dates()
        return Metadata(
            calculator=self.calculator, start_date=start_date, end_date=end_date
        )

    def calculate_next_dates(self) -> tuple[datetime, datetime]:
        return self.calculator.calculate(self.end_date)