"""Entry point for the Personal Expense Tracker.

Run from this folder, for example:
    python main.py add --amount 250 --category Food --description "Lunch" --date 2026-10-05
"""

from expense_tracker.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
