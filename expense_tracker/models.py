"""Data model for a single expense."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def validate_date(date_str: str) -> str:
    """Return the date string if it is a valid YYYY-MM-DD date, else raise ValueError."""
    try:
        parsed = datetime.strptime(date_str, DATE_FORMAT)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid date '{date_str}'. Please use YYYY-MM-DD format, e.g. 2026-10-05.")
    return parsed.strftime(DATE_FORMAT)


def validate_amount(amount) -> float:
    """Return the amount as a positive float rounded to 2 decimals, else raise ValueError."""
    try:
        value = float(amount)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid amount '{amount}'. Please enter a number, e.g. 250 or 99.50.")
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(value, 2)


@dataclass
class Expense:
    """One expense entry."""

    id: int
    amount: float
    category: str
    description: str
    date: str  # YYYY-MM-DD

    def __post_init__(self):
        self.amount = validate_amount(self.amount)
        self.date = validate_date(self.date)
        self.category = str(self.category).strip()
        if not self.category:
            raise ValueError("Category cannot be empty.")
        self.description = str(self.description).strip()
        if not self.description:
            raise ValueError("Description cannot be empty.")

    @property
    def month(self) -> str:
        """The YYYY-MM month this expense belongs to."""
        return self.date[:7]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            description=str(data["description"]),
            date=str(data["date"]),
        )
