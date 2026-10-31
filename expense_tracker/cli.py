"""Command-line interface for the Personal Expense Tracker."""

from __future__ import annotations

import argparse
import sys
from datetime import date as date_cls

from .analytics import (
    all_categories,
    category_totals,
    filter_by_category,
    filter_by_month,
    monthly_summary,
    total_amount,
)
from .storage import ExpenseStore

DEFAULT_DATA_FILE = "expenses.json"
SUGGESTED_CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Education", "Health", "Entertainment", "Other"]


def _print_table(expenses) -> None:
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Category':<16}{'Amount':>10}  Description")
    print("-" * 75)
    for e in expenses:
        print(f"{e.id:<5}{e.date:<12}{e.category:<16}{e.amount:>10.2f}  {e.description}")
    print("-" * 75)
    print(f"{'Total':<33}{total_amount(expenses):>10.2f}")


def cmd_add(args, store: ExpenseStore) -> int:
    expense_date = args.date or date_cls.today().isoformat()
    expense = store.add(args.amount, args.category, args.description, expense_date)
    print(f"Added expense #{expense.id}: {expense.amount:.2f} [{expense.category}] {expense.description} on {expense.date}")
    return 0


def cmd_list(args, store: ExpenseStore) -> int:
    expenses = store.load_all()
    if args.month:
        expenses = filter_by_month(expenses, args.month)
    if args.category:
        expenses = filter_by_category(expenses, args.category)
    expenses = sorted(expenses, key=lambda e: (e.date, e.id))
    _print_table(expenses)
    return 0


def cmd_delete(args, store: ExpenseStore) -> int:
    if store.delete(args.id):
        print(f"Deleted expense #{args.id}.")
        return 0
    print(f"Error: no expense with ID {args.id} was found.", file=sys.stderr)
    return 1


def cmd_summary(args, store: ExpenseStore) -> int:
    expenses = store.load_all()
    if args.month:
        summary = monthly_summary(expenses, args.month)
        print(f"Summary for {summary['month']}")
        print(f"  Expenses: {summary['count']}")
        print(f"  Total:    {summary['total']:.2f}")
        print(f"  Average:  {summary['average']:.2f} per expense")
        by_category = summary["by_category"]
    else:
        print("Overall summary (all months)")
        print(f"  Expenses: {len(expenses)}")
        print(f"  Total:    {total_amount(expenses):.2f}")
        by_category = category_totals(expenses)
    if by_category:
        print("\nBy category:")
        for category, total in by_category.items():
            print(f"  {category:<16}{total:>10.2f}")
    return 0


def cmd_categories(args, store: ExpenseStore) -> int:
    used = all_categories(store.load_all())
    print("Suggested categories:")
    for category in SUGGESTED_CATEGORIES:
        print(f"  - {category}")
    if used:
        print("\nCategories you have used:")
        for category in used:
            print(f"  - {category}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track personal expenses from the command line.",
    )
    parser.add_argument(
        "--file",
        default=DEFAULT_DATA_FILE,
        help=f"Path to the data file (default: {DEFAULT_DATA_FILE})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new expense")
    p_add.add_argument("--amount", required=True, help="Amount spent, e.g. 250 or 99.50")
    p_add.add_argument("--category", required=True, help="Category, e.g. Food")
    p_add.add_argument("--description", required=True, help="What the expense was for")
    p_add.add_argument("--date", default=None, help="Date in YYYY-MM-DD format (default: today)")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List expenses")
    p_list.add_argument("--month", default=None, help="Only show this month, YYYY-MM")
    p_list.add_argument("--category", default=None, help="Only show this category")
    p_list.set_defaults(func=cmd_list)

    p_delete = sub.add_parser("delete", help="Delete an expense by its ID")
    p_delete.add_argument("--id", required=True, type=int, help="ID of the expense to delete")
    p_delete.set_defaults(func=cmd_delete)

    p_summary = sub.add_parser("summary", help="Show totals and a monthly / category summary")
    p_summary.add_argument("--month", default=None, help="Month to summarise, YYYY-MM (default: all months)")
    p_summary.set_defaults(func=cmd_summary)

    p_categories = sub.add_parser("categories", help="Show suggested and used categories")
    p_categories.set_defaults(func=cmd_categories)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = ExpenseStore(args.file)
    try:
        return args.func(args, store)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
