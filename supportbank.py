import csv
import json
import logging

def banking(file):
    print("Please enter List All to see all balances, or List [Account] to see the transactions of an individual.")
    option = input("Enter your option: ")[5:]

    if option == "All":
        all_accounts(file)
    else:
        account(file, option)

def all_accounts(file):
    balances = {}
    for row in file:
        debtor = row[2]
        creditor = row[1]
        try:
            amount = float(row[4])
            balances[debtor] = balances.get(debtor, 0) - amount
            balances[creditor] = balances.get(creditor, 0) + amount
        except ValueError:
            logger.error("Invalid amount")
            print("ERROR: Invalid amount in:")
            print(row)
            print("Emitting this entry.")

    for person in balances:
        print(person, ": £", round(balances[person], 2))

def account(file, account):
    for row in file:
        if row[1] == account:
            print(row[0], ": Lent £", row[4], " to ", row[2], " for ", row[3])
        if row[2] == account:
            print(row[0], ": Borrowed £", row[4], " from ", row[1], " for ", row[3])

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Started")

filetype = input("Enter file type: ")

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

        print(f)

        data = []

        for row in f:
            data.append([row['Date'], row['FromAccount'], row['ToAccount'], row['Narrative'], row['Amount']])

        banking(data)

logger.info("Finished")