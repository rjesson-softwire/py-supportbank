import csv

def all_accounts(file):
    balances = {}
    for row in file:
        debtor = row[2]
        creditor = row[1]
        amount = float(row[4])
        balances[debtor] = balances.get(debtor, 0) - amount
        balances[creditor] = balances.get(creditor, 0) + amount

    for person in balances:
        print(person, ": £", round(balances[person], 2))

def account(file, account):
    for row in file:
        if row[1] == account:
            print(row[0], ": Lent £", row[4], " to ", row[2], " for ", row[3])
        if row[2] == account:
            print(row[0], ": Borrowed £", row[4], " from ", row[1], " for ", row[3])

with open("DodgyTransactions2015.csv", mode='r') as csvfile:
    f = csv.reader(csvfile)

    next(f)

    print("Please enter List All to see all balances, or List [Account] to see the transactions of an individual.")
    option = input("Enter your option: ")[5:]

    if option == "All":
        all_accounts(f)
    else:
        account(f, option)