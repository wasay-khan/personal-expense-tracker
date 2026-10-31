# Personal Expense Tracker

A command-line application written in Python to record daily expenses, organise them by category, and view monthly and category-wise summaries. Data is stored locally in a JSON file, so expenses are saved between runs without needing a database or an internet connection.

This is a learning project built to practise clean code structure — separating the data model, file storage, summary calculations, and the command-line interface into small modules that can be tested independently.

## Features

- Add an expense with an amount, category, description, and date (today's date is used if none is given)
- List all expenses, or filter them by month or category
- Delete an expense by its ID
- Monthly summary: number of expenses, total, average per expense, and category-wise totals
- Overall summary across all months with category-wise totals
- Suggested categories (Food, Transport, Bills, Shopping, Education, Health, Entertainment, Other) plus any custom category
- Input validation with clear error messages — for example, negative amounts and wrongly formatted dates are rejected with an explanation
- Data stored in a human-readable JSON file

## Tech Used

- **Python 3.10+** — standard library only (`argparse`, `json`, `dataclasses`, `datetime`, `pathlib`)
- **unittest** — Python's built-in testing framework, so the tests also run with no extra installs
- No external packages are required (see `requirements.txt`)

## Project Structure

```
.
├── main.py                  # Entry point — run the app from here
├── expense_tracker/
│   ├── __init__.py
│   ├── models.py            # Expense dataclass and input validation
│   ├── storage.py           # Reading/writing expenses to a JSON file
│   ├── analytics.py         # Totals, monthly summaries, category breakdowns
│   └── cli.py               # Command-line interface (argparse)
├── tests/
│   ├── test_models.py       # Validation and Expense model tests
│   ├── test_storage.py      # File storage tests (temporary files)
│   └── test_analytics.py    # Summary / totals logic tests
├── sample_data/
│   └── expenses.json        # Sample data file to try the app with
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

No installation is needed beyond Python itself.

1. Make sure Python 3.10 or newer is installed:

   ```bash
   python --version
   ```

2. Download or clone this project and open a terminal in the project folder.

There are no dependencies to install — the project uses only the Python standard library.

## Usage

All commands are run through `main.py`. By default, data is stored in a file called `expenses.json` in the current folder. A different file can be chosen with `--file`, which appears **before** the command, for example:

```bash
python main.py --file sample_data/expenses.json list
```

### Add an expense

```bash
python main.py add --amount 450 --category Food --description "Groceries" --date 2026-10-02
```

Output:

```
Added expense #1: 450.00 [Food] Groceries on 2026-10-02
```

The `--date` option can be omitted, in which case today's date is used.

### List expenses

```bash
python main.py list
```

Output:

```
ID   Date        Category            Amount  Description
---------------------------------------------------------------------------
1    2026-10-02  Food                450.00  Groceries
2    2026-10-03  Transport           200.00  Rickshaw to university
3    2026-10-05  Education          1500.00  Python course book
4    2026-10-05  Food                300.00  Lunch with friends
---------------------------------------------------------------------------
Total                               2450.00
```

Filters are also available:

```bash
python main.py list --month 2026-10
python main.py list --category Food
```

### Monthly summary

```bash
python main.py summary --month 2026-10
```

Output:

```
Summary for 2026-10
  Expenses: 4
  Total:    2450.00
  Average:  612.50 per expense

By category:
  Education          1500.00
  Food                750.00
  Transport           200.00
```

Running `python main.py summary` with no `--month` shows an overall summary for all months.

### Delete an expense

```bash
python main.py delete --id 2
```

Output:

```
Deleted expense #2.
```

### Invalid input

Invalid values are rejected with a clear error message and a non-zero exit code, for example:

```
$ python main.py add --amount -50 --category Food --description "Test"
Error: Amount must be greater than zero.

$ python main.py add --amount 100 --category Food --description "Test" --date 05-10-2026
Error: Invalid date '05-10-2026'. Please use YYYY-MM-DD format, e.g. 2026-10-05.
```

Run `python main.py --help` or `python main.py add --help` to see all commands and options.

## Running the Tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

The test suite (24 tests) covers:

- Input validation in the model layer (amounts, dates, empty fields)
- Storage behaviour — adding, loading, deleting, ID allocation, and handling a corrupted data file
- Analytics logic — totals, month/category filtering, category totals, and monthly summaries (including an empty month)

## What I Learned / Skills Demonstrated

- Organising a Python program into a package with separate modules, each with one responsibility
- Using `@dataclass` to model data, with validation in `__post_init__`
- Reading and writing JSON files with the standard library, including handling a missing or corrupted file
- Building a command-line interface with `argparse` subcommands
- Writing unit tests for business logic (storage and analytics) using temporary files, instead of only checking printed output
- Raising and handling `ValueError` to give the user helpful error messages instead of tracebacks

## Future Improvements

- Export a monthly report to CSV
- Add monthly budgets per category and warn when a budget is exceeded
- Add an edit command to fix a mistake in an existing expense
- Search expenses by description keyword
- Store data in SQLite for larger datasets
- Add charts for spending over time (for example with `matplotlib`)

## License

This project is released under the MIT License — see the [LICENSE](LICENSE) file for details.
