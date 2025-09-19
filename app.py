import argparse
import os
import sys
from datetime import datetime

import pandas as pd
from tabulate import tabulate

csv_file = 'Data/expenses.csv'


def load_expenses() -> pd.DataFrame:
    if not os.path.exists(csv_file):
        return pd.DataFrame(columns=["expense_id", "description", "amount", "date"])
    return pd.read_csv(csv_file)


def add_expenses(description: str, amount: float):
    all_expenses = dict()
    expense_id = generate_expense_id()
    current_timestamp = datetime.now()

    all_expenses[expense_id] = {
        "description": description,
        "amount": amount,
        "date": current_timestamp.strftime("%Y-%m-%d"),
    }

    store_expenses(all_expenses)
    print(f"Expense added successfully (ID: {expense_id})")


def update_expenses(expense_id: int, description: str | None, amount: float | None):
    expenses_df = pd.read_csv(csv_file)

    if expense_id not in expenses_df["expense_id"].values:
        print(f"Error: Expense ID {expense_id} not found.")
        return

    idx = expenses_df["expense_id"] == expense_id

    if description is not None:
        expenses_df.loc[idx, "description"] = description
    if amount is not None:
        expenses_df.loc[idx, "amount"] = amount

    expenses_df.loc[idx, "date"] = datetime.now().strftime("%Y-%m-%d")

    expenses_df.to_csv(csv_file, index=False)
    print(f"Expense updated successfully (ID: {expense_id})")


def delete_expenses(expense_id: int):
    expenses_df = load_expenses()

    # Drop the row(s) where expense_id matches
    get_record = expenses_df.loc[expenses_df['expense_id'] != expense_id]

    # Save back to CSV (overwrite)
    get_record.to_csv(csv_file, index=False)
    print(f"Expense deleted successfully")


def view_expenses():
    view_all_expenses = show_all_expenses().sort_values("ID")
    print(
        tabulate(
            view_all_expenses,
            headers="keys",
            tablefmt="pretty",
            showindex=False
        )
    )


def view_summary():
    expenses_df = load_expenses()
    total_amt = expenses_df["amount"].sum()
    print(f"Total expenses: ${format(total_amt, '.2f')}")


def view_summary_by_month(month: int):
    # Exit if the month is out of range
    if not 1 <= month <= 12:
        print(f"Invalid month: {month}")
        sys.exit(1)

    # Get the month
    expenses_df = load_expenses()
    get_month = pd.to_datetime(expenses_df["date"]).dt.month.astype(int)
    total_amt = expenses_df.loc[get_month == month, "amount"].sum()

    month_name = pd.to_datetime(f"2025-{month}-01").strftime("%B")
    print(f"Total expenses for {month_name}: ${format(total_amt, '.2f')}")


# Generate expenses ID
def generate_expense_id() -> int:
    if not os.path.exists(csv_file):  # If file doesn’t exist yet
        return 1

    expenses_df = load_expenses()
    if expenses_df.empty:
        return 1
    return expenses_df["expense_id"].max() + 1


# Store all expenses in a cvs file
def store_expenses(expenses_list):
    df = pd.DataFrame.from_dict(expenses_list, orient="index").reset_index()
    df.rename(columns={"index": "expense_id"}, inplace=True)

    # Append to file if it exists, otherwise write with header
    df.to_csv(csv_file, mode="a", header=not os.path.exists(csv_file), index=False)
    print("Expenses successfully stored.")


# Get data from csv
def show_all_expenses(format_for_display=True) -> pd.DataFrame:
    expenses_df = load_expenses()
    expenses_df.rename(
        columns={
            "expense_id": "ID",
            "description": "Description",
            "amount": "Amount",
            "date": "Date",
        },
        inplace=True)

    # Format Amount with $ when needed
    if format_for_display:
        expenses_df["Amount"] = expenses_df["Amount"].apply(lambda x: f"${x:.2f}")
    return expenses_df


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI Tool")

    subparsers = parser.add_subparsers(dest="command")

    # Adding expenses
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", "-desc", type=str, help="Description of the expense")
    add_parser.add_argument("--amount", "-a", type=float, help="Amount of the expense")

    # Update
    add_parser = subparsers.add_parser("update", help="Update a new expense")
    add_parser.add_argument("--id", "-id", type=int, help="Id to update")
    add_parser.add_argument("--description", "-desc", type=str, help="Update the description", required=False)
    add_parser.add_argument("--amount", "-a", type=float, help="Update the amount", required=False)

    # Delete
    add_parser = subparsers.add_parser("delete", help="Delete an expense")
    add_parser.add_argument("--id", "-id", type=int, help="Id to delete")

    # List expenses
    subparsers.add_parser("list", help="List all expense")

    # Summary
    add_parser = subparsers.add_parser("summary", help="Get summary of the expense")
    add_parser.add_argument("--month", "-m", type=int, help="Get total amount of expense for the month")

    # Help
    add_parser = subparsers.add_parser("help", help="Get help", add_help=False)
    add_parser.add_argument("--help", "-h", type=str, help="Get help")

    args = parser.parse_args()

    match args.command:
        case "add":
            if args.description is None or args.amount is None:
                print("Error: Description and amount are required for adding an expense")
                sys.exit(1)
            add_expenses(args.description, args.amount)
        case "update":
            if args.id is None or (args.description is None and args.amount is None):
                print("Error: Description or amount is required for updating an existing expense")
                sys.exit(1)
            update_expenses(args.id, args.description, args.amount)
        case "delete":
            if args.id is None or args.description is None or args.amount is None:
                print("Error: Id is required to delete an expense")
                sys.exit(1)
            delete_expenses(args.id)
        case "list":
            view_expenses()
        case "summary":
            if args.month or args.month == 0:
                view_summary_by_month(args.month)
            else:
                view_summary()
        case "help":
            parser.print_help()
        case _:
            print(f"Unknown command: {args.command}")
            sys.exit(1)


if __name__ == "__main__":
    main()
