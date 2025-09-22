"""
UtilsManager handles CSV I/O only.
"""
import os

import pandas as pd


class UtilsManager:
    def __init__(self, csv_file='Data/expenses.csv'):
        self.csv_file = csv_file

    def load_expenses(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_file):
            return pd.DataFrame(columns=["expense_id", "description", "amount", "date"])
        df = pd.read_csv(self.csv_file)

        # Ensure amount is numeric so formatting / sums work
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        return df

    # Generate expenses ID
    def generate_expense_id(self) -> int:
        df = self.load_expenses()
        if df.empty:
            return 1
        return int(df["expense_id"].max()) + 1

    # Store all expenses in a CSV file
    def store_expenses(self, expenses_list):
        df = pd.DataFrame.from_dict(expenses_list, orient="index").reset_index()
        df.rename(columns={"index": "expense_id"}, inplace=True)

        # Append to file if it exists, otherwise write with header
        return df.to_csv(self.csv_file, mode="a", header=not os.path.exists(self.csv_file), index=False)

    def save_dataframe(self, df: pd.DataFrame):
        df.to_csv(self.csv_file, index=False)
