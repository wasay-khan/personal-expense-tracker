import tempfile
import unittest
from pathlib import Path

from expense_tracker.storage import ExpenseStore


class TestExpenseStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "expenses.json"
        self.store = ExpenseStore(self.file)

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_file_loads_empty(self):
        self.assertEqual(self.store.load_all(), [])

    def test_add_and_load(self):
        added = self.store.add(250, "Food", "Lunch", "2026-10-05")
        self.assertEqual(added.id, 1)
        loaded = self.store.load_all()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].description, "Lunch")
        self.assertEqual(loaded[0].amount, 250.0)

    def test_ids_increase(self):
        first = self.store.add(10, "Food", "a", "2026-10-01")
        second = self.store.add(20, "Food", "b", "2026-10-02")
        self.assertEqual((first.id, second.id), (1, 2))

    def test_add_rejects_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.store.add(-10, "Food", "Lunch", "2026-10-05")

    def test_add_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            self.store.add(10, "Food", "Lunch", "05/10/2026")

    def test_delete_existing(self):
        added = self.store.add(10, "Food", "a", "2026-10-01")
        self.assertTrue(self.store.delete(added.id))
        self.assertEqual(self.store.load_all(), [])

    def test_delete_missing_returns_false(self):
        self.assertFalse(self.store.delete(999))

    def test_data_survives_new_store_instance(self):
        self.store.add(10, "Food", "a", "2026-10-01")
        reloaded = ExpenseStore(self.file).load_all()
        self.assertEqual(len(reloaded), 1)

    def test_corrupted_file_raises_helpful_error(self):
        self.file.write_text("{ not json", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.store.load_all()


if __name__ == "__main__":
    unittest.main()
