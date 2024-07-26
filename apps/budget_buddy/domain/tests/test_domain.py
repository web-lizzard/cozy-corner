from apps.budget_buddy.domain import (
    DomainEntry,
    Budget,
    Expense,
    Pocket,
    Metadata,
    DummyCalculator,
)
from datetime import datetime, timedelta
from typing import cast
from uuid import UUID
import pytest


class TestDomain:
    def test_domain_entry_should_have_default_uuid(self):
        domain_entry = DomainEntry()

        assert domain_entry.id is not None
        assert cast(UUID, domain_entry.id)

    class TestExpense:
        def test_match_expense_should_check_if_expense_is_the_same_category(self):
            expense = Expense(value=2000, category_id="1")

            assert expense.match_category("1")
            assert not expense.match_category("3")

    class TestBudget:
        def test_adding_expense_should_append_it_to_the_list(self):
            expense = Expense(value=300, category_id="1")
            budget = Budget(name="Meals", categories=["1"], expenses=[])

            budget.add_expense(expense=expense)

            assert expense in budget.expenses
            assert len(budget.expenses) == 1

        def test_reproducing_budget_should_copy_its_data_without_id_and_expenses(self):
            expense = Expense(value=300, category_id="1")
            budget = Budget(name="Meals", categories=["1"], expenses=[expense])

            reproduced_budget = budget.reproduce()

            assert budget != reproduced_budget
            assert budget.id != reproduced_budget
            assert len(reproduced_budget.expenses) == 0
            assert budget.name == budget.name

    class TestMetaData:
        def test_reproduce_metadata_should_copy_it(self):
            metadata = Metadata(
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                calculator=DummyCalculator(),
            )

            reproduced_metadata = metadata.reproduce()

            assert reproduced_metadata.id != metadata
            assert reproduced_metadata.id != metadata.id
            assert reproduced_metadata.start_date > metadata.start_date
            assert reproduced_metadata.end_date > metadata.end_date

    class TestPocket:
        def test_adding_expense_to_pocket_should_add_it_budgets(self):
            budgets = [
                Budget(name="Meals", categories=["1", "2", "3"], expenses=[]),
                Budget(name="Tools", categories=["1"], expenses=[]),
                Budget(name="Books", categories=["4"], expenses=[]),
            ]
            expense = Expense(category_id="1", value=300)
            metadata = Metadata(
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                calculator=DummyCalculator(),
            )
            pocket = Pocket(
                name="My Monthly Pocket",
                budgets=budgets,
                total_limit=100000,
                metadata=metadata,
            )

            pocket.add_expense(expense)

            assert expense in budgets[0].expenses
            assert expense not in budgets[2].expenses

        def test_pocket_reproduce_should_reproduce_its_content_without_id(self):
            expense = Expense(category_id="5", value=300)
            budgets = [
                Budget(name="Meals", categories=["1", "2", "3"], expenses=[expense])
            ]
            metadata = Metadata(
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                calculator=DummyCalculator(),
            )
            pocket = Pocket(
                name="My Monthly Pocket",
                budgets=budgets,
                total_limit=100000,
                metadata=metadata,
            )

            reproduced_pocket = pocket.reproduce()

            assert reproduced_pocket.id != pocket.id
            assert reproduced_pocket.metadata != pocket.metadata
            assert reproduced_pocket.budgets[0].name == pocket.budgets[0].name
            assert len(reproduced_pocket.budgets[0].expenses) == 0
