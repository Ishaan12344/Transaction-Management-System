import logging
from src.transaction_manager import TransactionManager

logging.basicConfig(
    filename="logs/transaction.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    manager = TransactionManager(
        filename="data/transactions.csv",
        initial_balance=1000
    )

    manager.generate_transactions(200)
    summary = manager.process_transactions()

    print("\n------ TRANSACTION SUMMARY ------")
    print("Total Transactions :", summary["total_transactions"])
    print("Total Credit       :", summary["total_credit"])
    print("Total Debit        :", summary["total_debit"])
    print("Final Balance      :", summary["final_balance"])

if __name__ == "__main__":
    main()
