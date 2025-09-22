import argparse
import sys

from tabulate import tabulate

from expenses import ExpensesManager
from utils import UtilsManager

util_manager = UtilsManager()
expenses_manager = ExpensesManager(util_manager)


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

            result = expenses_manager.add_expenses(args.description, args.amount)
            current_id = next(iter(result))
            print(f"Expense added successfully (ID: {current_id})")
        case "update":
            if args.id is None or (args.description is None and args.amount is None):
                print("Error: Description or amount is required for updating an existing expense")
                sys.exit(1)

            is_updated = expenses_manager.update_expenses(args.id, args.description, args.amount)
            if is_updated:
                print(f"Expense updated successfully (ID: {args.id})")
            else:
                print(f"Error: Expense ID {args.id} not found.")
        case "delete":
            if args.id is None:
                print("Error: Id is required to delete an expense")
                sys.exit(1)
            is_deleted = expenses_manager.delete_expenses(args.id)
            if is_deleted:
                print(f"Expense deleted successfully (ID: {args.id})")
            else:
                print(f"Error: Expense ID {args.id} not found.")
        case "list":
            view_all_expenses = expenses_manager.list_expenses()
            print(
                tabulate(
                    view_all_expenses,
                    headers="keys",
                    tablefmt="pretty",
                    showindex=False)
            )
        case "summary":
            if args.month or args.month == 0:
                result = expenses_manager.view_summary_by_month(args.month)
                if result is None:
                    print(f"Invalid month: {args.month}")
                else:
                    total_amt, month_name = result
                    print(f"Total expenses for {month_name}: ${format(total_amt, '.2f')}")
            else:
                total_amt = expenses_manager.view_summary()
                print(f"Total expenses: ${format(total_amt, '.2f')}")
        case "help":
            parser.print_help()
        case _:
            print(f"Unknown command: {args.command}")
            sys.exit(1)


if __name__ == "__main__":
    main()
