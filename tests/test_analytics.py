import unittest

from expense_tracker.analytics import (
    all_categories,
    category_totals,
    filter_by_category,
    filter_by_month,
    monthly_summary,
    total_amount,
)
from expense_tracker.models import Expense


def make_expenses():
    return [
        Expense(id=1, amount=450, category="Food", description="Groceries", date="2026-10-02"),
        Expense(id=2, amount=200, category="Transport", description="Rickshaw", date="2026-10-03"),
        Expense(id=3, amount=300, category="Food", description="Lunch", date="2026-10-05"),
        Expense(id=4, amount=1500, category="Education", description="Book", date="2026-09-15"),
    ]


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.expenses = make_expenses()

    def test_total_amount(self):
        self.assertEqual(total_amount(self.expenses), 2450.0)
        self.assertEqual(total_amount([]), 0.0)

    def test_filter_by_month(self):
        october = filter_by_month(self.expenses, "2026-10")
        self.assertEqual(len(october), 3)
        self.assertTrue(all(e.month == "2026-10" for e in october))

    def test_filter_by_category_is_case_insensitive(self):
        food = filter_by_category(self.expenses, "food")
        self.assertEqual(len(food), 2)

    def test_category_totals_sorted_highest_first(self):
        totals = category_totals(self.expenses)
        self.assertEqual(totals["Food"], 750.0)
        self.assertEqual(totals["Education"], 1500.0)
        self.assertEqual(list(totals)[0], "Education")

    def test_monthly_summary(self):
        summary = monthly_summary(self.expenses, "2026-10")
        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["total"], 950.0)
        self.assertEqual(summary["average"], round(950 / 3, 2))
        self.assertEqual(summary["by_category"]["Food"], 750.0)

    def test_monthly_summary_empty_month(self):
        summary = monthly_summary(self.expenses, "2026-12")
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["average"], 0.0)

    def test_all_categories(self):
        self.assertEqual(all_categories(self.expenses), ["Education", "Food", "Transport"])


if __name__ == "__main__":
    unittest.main()
