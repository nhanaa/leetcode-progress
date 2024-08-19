from account import Account
import json

path = "./data/data.json"

def insert_account(account: Account):
  print(f"Inserting account {account.username}")
  with open(path, "r") as file:
    accounts = json.load(file)

  accounts.append(account.to_dict())

  with open(path, "w") as file:
    json.dump(accounts, file)


def update_account(account: Account):
  print(f"Updating account {account.username}")
  with open(path, "r") as file:
    accounts = json.load(file)

  for i, acc in enumerate(accounts):
    if acc["username"] == account.username:
      accounts[i] = account.to_dict()
      break
  with open(path, "w") as file:
    json.dump(accounts, file)


def get_account(username: str):
  with open(path, "r") as file:
    accounts = json.load(file)
    print(accounts)

  for account in accounts:
    if account["username"] == username:
      return Account(account["username"], account["easy"], account["medium"], account["hard"])
