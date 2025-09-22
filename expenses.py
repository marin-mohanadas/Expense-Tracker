"""
ExpensesManager handles business logic (add/update/delete/list).
"""

from datetime import datetime

import pandas as pd


class ExpensesManager:
    def __init__(self, util_manager):
        self.util = util_manager

    def list_expenses(self) -> pd.DataFrame:
        df = self.util.load_expenses()
        df.rename(
            columns={
                "expense_id": "ID",
                "description": "Description",
                "amount": "Amount",
                "date": "Date",
            },
            inplace=True)

        df["Amount"] = df["Amount"].apply(lambda x: f"${x:.2f}")
        return df.sort_values(by=["ID"])

    def add_expenses(self, description: str, amount: float) -> dict:
        expense_id = self.util.generate_expense_id()
        current_timestamp = datetime.now()

        expenses_dict = {
            expense_id: {
                "description": description,
                "amount": amount,
                "date": current_timestamp.strftime("%Y-%m-%d")
            }
        }

        self.util.store_expenses(expenses_dict)
        return expenses_dict

    def update_expenses(self, expense_id: int, description: str | None, amount: float | None) -> bool:
        df = self.util.load_expenses()
        if expense_id not in df["expense_id"].values:
            return False

        idx = df["expense_id"] == expense_id

        if description is not None:
            df.loc[idx, "description"] = description
        if amount is not None:
            df.loc[idx, "amount"] = amount

        df.loc[idx, "date"] = datetime.now().strftime("%Y-%m-%d")

        self.util.save_dataframe(df)
        return True

    def delete_expenses(self, expense_id: int) -> bool:
        df = self.util.load_expenses()
        if expense_id not in df["expense_id"].values:
            return False

        # Drop the row(s) where expense_id matches
        df = df.loc[df['expense_id'] != expense_id]

        self.util.save_dataframe(df)
        return True

    def view_summary(self) -> float:
        df = self.util.load_expenses()
        return df["amount"].sum()

    def view_summary_by_month(self, month: int) -> tuple[float, str] | None:
        if not 1 <= month <= 12:
            return None

        df = self.util.load_expenses()
        # Get the month
        get_month = pd.to_datetime(df["date"]).dt.month.astype(int)
        total_amt = df.loc[get_month == month, "amount"].sum()

        month_name = pd.to_datetime(f"2025-{month}-01").strftime("%B")
        return_tuple = (total_amt, month_name)
        return return_tuple
