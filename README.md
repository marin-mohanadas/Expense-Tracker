# Expense Tracker CLI

A simple **Command-Line Expense Tracker** built with Python and Pandas.  
This project lets you add, update, delete, list, and summarize your expenses in a CSV file.

This project is based on the [roadmap.sh Expense Tracker project](https://roadmap.sh/projects/expense-tracker).

## Features

- Add new expenses with description and amount
- Update existing expenses by ID
- Delete expenses by ID
- List all expenses in a formatted table
- View total expenses summary
- View expenses summary by month
- Data persistence using CSV (`Data/expenses.csv`)

## Tech Stack

- Python 3.10+
- [pandas](https://pandas.pydata.org/) – for CSV and data manipulation
- [tabulate](https://pypi.org/project/tabulate/) – for pretty CLI tables

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install via setup file:

```bash
pip install .
```

## Generate requirements.txt

If you add new dependencies in the future, you can regenerate `requirements.txt` with:

```bash
pip freeze > requirements.txt
```

This will capture all installed packages with exact versions.

## Usage

The CLI entry point is `expense-tracker`.  
You can run commands like:

### Add an expense
```bash
expense-tracker add --description "Coffee" --amount 4.50
```

### Update an expense
```bash
expense-tracker update --id 1 --description "Latte" --amount 5.00
```

### Delete an expense
```bash
expense-tracker delete --id 1
```

### List all expenses
```bash
expense-tracker list
```

### View summary
```bash
expense-tracker summary
```

### View summary by month
```bash
expense-tracker summary --month 9
```

## Example

```bash
$ expense-tracker add --description "Lunch" --amount 12.5
Expense added successfully (ID: 1)

$ expense-tracker list
+----+-------------+--------+------------+
| ID | Description | Amount | Date       |
+----+-------------+--------+------------+
|  1 | Lunch       | $12.50 | 2025-09-22 |
+----+-------------+--------+------------+
```

## Project Structure

```
expense-tracker/
│── app.py          # CLI entry point
│── expenses.py     # Business logic (add/update/delete/list/summary)
│── utils.py        # Utility functions for CSV I/O and helpers
│── setup.py        # Packaging & installation setup
│── requirements.txt # Dependencies list
│── Data/
│   └── expenses.csv # Auto-created CSV file to store expenses
```

## Roadmap

Future improvements may include:
- Exporting reports to Excel/JSON
- Category tagging (food, travel, etc.)
- Better CLI formatting with colors

## License

This project is open-source and available under the [MIT License](LICENSE).
