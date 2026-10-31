"""Summary calculations over a list of expenses (pure logic, easy to test)."""

from __future__ import annotations

from .models import Expense


def total_amount(expenses: list[Expense]) -> float:
    return round(sum(e.amount for e in expenses), 2)


def filter_by_month(expenses: list[Expense], month: str) -> list[Expense]:
    """month is YYYY-MM."""
    return [e for e in expenses if e.month == month]


def filter_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    return [e for e in expenses if e.category.lower() == category.lower()]


def category_totals(expenses: list[Expense]) -> dict[str, float]:
    """Return {category: total} sorted by total, highest first."""
    totals: dict[str, float] = {}
    for expense in expenses:
        totals[expense.category] = round(totals.get(expense.category, 0.0) + expense.amount, 2)
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def monthly_summary(expenses: list[Expense], month: str) -> dict:
    """Summary for one month: total, count, average and per-category totals."""
    month_expenses = filter_by_month(expenses, month)
    total = total_amount(month_expenses)
    count = len(month_expenses)
    return {
        "month": month,
        "count": count,
        "total": total,
        "average": round(total / count, 2) if count else 0.0,
        "by_category": category_totals(month_expenses),
    }


def all_categories(expenses: list[Expense]) -> list[str]:
    """Unique category names, alphabetically sorted (case-insensitive)."""
    return sorted({e.category for e in expenses}, key=str.lower)
