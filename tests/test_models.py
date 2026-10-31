import unittest

from expense_tracker.models import Expense, validate_amount, validate_date


class TestValidation(unittest.TestCase):
    def test_valid_amount(self):
        self.assertEqual(validate_amount("99.5"), 99.5)
        self.assertEqual(validate_amount(250), 250.0)

    def test_amount_must_be_positive(self):
        for bad in (0, -5, "-1"):
            with self.assertRaises(ValueError):
                validate_amount(bad)

    def test_amount_must_be_a_number(self):
        with self.assertRaises(ValueError):
            validate_amount("abc")

    def test_valid_date(self):
        self.assertEqual(validate_date("2026-10-05"), "2026-10-05")

    def test_invalid_date(self):
        for bad in ("05-10-2026", "2026-13-01", "not-a-date", ""):
            with self.assertRaises(ValueError):
                validate_date(bad)

    def test_expense_rejects_empty_category(self):
        with self.assertRaises(ValueError):
            Expense(id=1, amount=10, category="  ", description="x", date="2026-10-01")

    def test_expense_month_property(self):
        e = Expense(id=1, amount=10, category="Food", description="x", date="2026-10-01")
        self.assertEqual(e.month, "2026-10")

    def test_expense_round_trip_dict(self):
        e = Expense(id=3, amount=12.5, category="Food", description="Tea", date="2026-10-01")
        self.assertEqual(Expense.from_dict(e.to_dict()), e)


if __name__ == "__main__":
    unittest.main()
