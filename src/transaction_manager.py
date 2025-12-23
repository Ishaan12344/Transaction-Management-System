import csv
import random
import logging
from src.file_handler import FileHandler


class TransactionManager:
    def __init__(self, filename, initial_balance=1000):
        self.filename = filename
        self.balance = initial_balance

    # -------------------------------------------------
    # Generate random transactions and store in CSV
    # -------------------------------------------------
    def generate_transactions(self, count=20):
        with FileHandler(self.filename, "w") as file:
            writer = csv.writer(file)

            # CSV header
            writer.writerow(["sr_no", "transaction_type", "amount", "balance"])

            for sr_no in range(1, count + 1):
                txn_type = random.choice(["CREDIT", "DEBIT"])

                # Prevent debit when balance is zero
                if txn_type == "DEBIT" and self.balance == 0:
                    txn_type = "CREDIT"

                if txn_type == "CREDIT":
                    amount = random.randint(100, 500)
                    self.balance += amount
                else:
                    amount = random.randint(1, self.balance)
                    self.balance -= amount

                writer.writerow([sr_no, txn_type, amount, self.balance])

    # -------------------------------------------------
    # Generator: Read transactions lazily from CSV
    # -------------------------------------------------
    def read_transactions(self):
        with FileHandler(self.filename, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    yield {
                        "id": int(row["sr_no"]),
                        "type": row["transaction_type"],
                        "amount": float(row["amount"]),
                        "balance": float(row["balance"])
                    }
                except (ValueError, KeyError) as e:
                    logging.error(f"Invalid record skipped: {row} | Error: {e}")
                    continue

    # -------------------------------------------------
    # Process transactions and compute summary
    # -------------------------------------------------
    def process_transactions(self):
        total_transactions = 0
        total_credit = 0
        total_debit = 0
        final_balance = 0

        for txn in self.read_transactions():
            total_transactions += 1

            if txn["type"] == "CREDIT":
                total_credit += txn["amount"]
            elif txn["type"] == "DEBIT":
                total_debit += txn["amount"]

            final_balance = txn["balance"]

        return {
            "total_transactions": total_transactions,
            "total_credit": total_credit,
            "total_debit": total_debit,
            "final_balance": final_balance
        }
