"""JSON file storage for expenses.

Data file format:
{
  "next_id": 4,
  "expenses": [ {expense}, ... ]
}
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Expense


class ExpenseStore:
    """Loads, saves and modifies expenses stored in a JSON file."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    # -- internal helpers -------------------------------------------------
    def _read_raw(self) -> dict:
        if not self.file_path.exists():
            return {"next_id": 1, "expenses": []}
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(
                f"Data file '{self.file_path}' is corrupted (not valid JSON). "
                "Fix it by hand or delete it to start fresh."
            )
        if not isinstance(data, dict) or "expenses" not in data:
            raise ValueError(f"Data file '{self.file_path}' has an unexpected format.")
        return data

    def _write_raw(self, data: dict) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # -- public API --------------------------------------------------------
    def load_all(self) -> list[Expense]:
        data = self._read_raw()
        return [Expense.from_dict(item) for item in data["expenses"]]

    def add(self, amount, category, description, date) -> Expense:
        data = self._read_raw()
        expense = Expense(
            id=int(data.get("next_id", 1)),
            amount=amount,
            category=category,
            description=description,
            date=date,
        )
        data["expenses"].append(expense.to_dict())
        data["next_id"] = expense.id + 1
        self._write_raw(data)
        return expense

    def delete(self, expense_id: int) -> bool:
        """Delete an expense by id. Returns True if one was removed."""
        data = self._read_raw()
        before = len(data["expenses"])
        data["expenses"] = [e for e in data["expenses"] if int(e["id"]) != int(expense_id)]
        if len(data["expenses"]) == before:
            return False
        self._write_raw(data)
        return True

    def clear(self) -> None:
        """Remove all expenses (used mainly by tests)."""
        self._write_raw({"next_id": 1, "expenses": []})
