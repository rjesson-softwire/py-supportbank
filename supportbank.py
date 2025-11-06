import csv
import json
from bs4 import BeautifulSoup
import logging
import datetime
import re

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
        output = ""
        for t in transactions:
            if t.debtor == self.name:
                output += str(t.date) + ": Borrowed £" + str(t.amount) + " from " + t.creditor + " for " + t.narrative + "\n"
            elif t.creditor == self.name:
                output += str(t.date) + ": Lent £" + str(t.amount) + " to " + t.debtor + " for " + t.narrative + "\n"
        return output

    def calculate_balance(self, transactions):
        for t in transactions:
            if t.debtor == self.name:
                self.balance -= t.amount
            elif t.creditor == self.name:
                self.balance += t.amount

def banking(data):
    transactions, accounts = process_data(data)

    print("Please enter List All to see all balances, or List [Account] to see the transactions of an individual.")
    option = input("Enter your option: ")[5:]

    output = ""

    if option == "All":
        for a in accounts:
            a.calculate_balance(transactions)
            text = a.name + ": £" + str(round(a.balance, 2))
            output += text + "\n"
    elif option != "":
        for a in accounts:
            if option == a.name:
                output += a.display_own_transactions(transactions)
    else:
        return

    print(output)


def process_data(data):
    transactions = []
    names = set()
    accounts = []
    for row in data:
        try:
            amount = float(row[4])
            transactions.append(Transaction(str(row[0]), row[1], row[2], row[3], amount))
        except ValueError:
            logger.error("Invalid amount")
            print("ERROR: Invalid amount in:")
            print([str(row[0]), row[1], row[2], row[3], row[4]])
            print("Emitting this entry.")
        names.add(row[1])
        names.add(row[2])
    for n in names:
        accounts.append(Account(n))
    return transactions, accounts

def excel_date_to_date(serial_date):
    base_date = datetime.date(1899,12,30)
    return base_date + datetime.timedelta(days = int(serial_date))

filetype = input("Enter file type: ")

if filetype == "csv":
    with open("DodgyTransactions2015.csv", mode='r') as csvfile:
        f = csv.reader(csvfile)
        logger.info("Reading csv file")

        next(f)

        data = []

        for row in f:
            date = row[0]
            date_pattern = re.compile("\d{2}\/\d{2}\/\d{4}")
            if re.match(date_pattern, date):
                date = datetime.date(int(date[6:10]), int(date[3:5]), int(date[0:2]))
            else:
                logger.error("Invalid date")
                print("ERROR: Invalid date in:")
                print(row)
                print("Emitting this entry.")
                continue

            data.append([date, row[1], row[2], row[3], row[4]])

        banking(data)
elif filetype == "json":
    with open ("Transactions2013.json", 'r') as jsonfile:
        f = json.load(jsonfile)
        logger.info("Reading json file")

        data = []

        for row in f:
            data.append([row['Date'][:10], row['FromAccount'], row['ToAccount'], row['Narrative'], row['Amount']])

        banking(data)
elif filetype == "xml":
    with open("Transactions2012.xml", 'r') as xmlfile:
        f = xmlfile.read()
        logger.info("Reading xml file")

        bs_data = BeautifulSoup(f, "lxml")

        bs_transactions = bs_data.find_all('supporttransaction')

        data = []

        for t in bs_transactions:
            serial_date = t.get('date')
            date = excel_date_to_date(serial_date)
            narrative = t.find('description').text
            parties = t.find('parties')
            to_account = parties.find('to').text
            from_account = parties.find('from').text
            try:
                amount = t.find('value').text
            except AttributeError:
                logger.error("No value on transaction")
                print("ERROR: No value on transaction:")
                amount = 0
                print(date, ":", "from", from_account, "to", to_account, "for", narrative)

            data.append([date, from_account, to_account, narrative, amount])

        banking(data)

logger.info("Finished")