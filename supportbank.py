import csv
import json
import logging

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Started")

class Transaction:
    def __init__(self, date, debtor, creditor, narrative, amount):
        self.date = date
        self.debtor = debtor
        self.creditor = creditor
        self.narrative = narrative
        self.amount = amount

class Account:
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def display_own_transactions(self, transactions):
        for t in transactions:
            if t.debtor == self.name:
                print(t.date, ": Borrowed £", t.amount, " from ", t.creditor, " for ", t.narrative)
            elif t.creditor == self.name:
                print(t.date, ": Lent £", t.amount, " to ", t.debtor, " for ", t.narrative)

    def calculate_balance(self, transactions):
        for t in transactions:
            if t.debtor == self.name:
                self.balance -= t.amount
            elif t.creditor == self.name:
                self.balance += t.amount


filetype = input("Enter file type: ")

def banking(data):
    transactions, accounts = process_data(data)

    print("Please enter List All to see all balances, or List [Account] to see the transactions of an individual.")
    option = input("Enter your option: ")[5:]

    if option == "All":
        for a in accounts:
            a.calculate_balance(transactions)
            print(a.name, ": £", round(a.balance, 2))
    else:
        for a in accounts:
            if option == a.name:
                a.display_own_transactions(transactions)

def process_data(data):
    transactions = []
    names = set()
    accounts = []
    for row in data:
        try:
            amount = float(row[4])
            transactions.append(Transaction(row[0], row[1], row[2], row[3], float(row[4])))
        except ValueError:
            logger.error("Invalid amount")
            print("ERROR: Invalid amount in:")
            print(row)
            print("Emitting this entry.")
        names.add(row[1])
        names.add(row[2])
    for n in names:
        accounts.append(Account(n))
    return transactions, accounts

if filetype == "csv":
    with open("DodgyTransactions2015.csv", mode='r') as csvfile:
        f = csv.reader(csvfile)
        logger.info("Reading csv file")

        next(f)

        banking(f)

elif filetype == "json":
    with open ("Transactions2013.json", 'r') as jsonfile:
        f = json.load(jsonfile)
        logger.info("Reading json file")

        data = [

        for row in f:
            data.append([row['Date'], row['FromAccount'], row['ToAccount'], row['Narrative'], row['Amount']])

        banking(data)

logger.info("Finished")