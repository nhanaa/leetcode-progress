import sqlite3
from account import Account

def connect_database(dbName):
  conn = sqlite3.connect(dbName)
  print("Open db successfully")

  return conn


def create_table(conn):
  # Execute a PRAGMA statement to check if the table exists
  c = conn.cursor()
  c.execute("PRAGMA table_info(LC_ACCOUNT)")
  result = c.fetchone()

  # If the result is None, then the table does not exist
  if result is None:
    conn.execute('''CREATE TABLE LC_ACCOUNT
      (ID INT PRIMARY KEY     NOT NULL,
      USERNAME       TEXT     NOT NULL,
      EASY            INT     NOT NULL,
      MEDIUM          INT    NOT NULL,
      HARD            INT    NOT NULL,
      TOTAL           INT    NOT NULL);''')
    print("Table created successfully")
  else:
    print("Table already existed")


def insert_account(conn, account: Account):
  conn.execute(f"INSERT INTO LC_ACCOUNT (ID, USERNAME,EASY,MEDIUM,HARD,TOTAL) \
      VALUES (1, '{account.username}', {account.easy}, {account.medium}, {account.hard}, {account.total})")
  conn.commit()
  print("Insert successfully")


def update_account(conn, account: Account):
  conn.execute(f"UPDATE LC_ACCOUNT set EASY = {account.easy} where ID = 1")
  conn.execute(f"UPDATE LC_ACCOUNT set MEDIUM = {account.medium} where ID = 1")
  conn.execute(f"UPDATE LC_ACCOUNT set HARD = {account.hard} where ID = 1")
  conn.execute(f"UPDATE LC_ACCOUNT set TOTAL = {account.hard} where ID = 1")
  conn.commit()
  print("Update successfully")


def get_account(conn, username):
  try:
    cursor = conn.execute(f"SELECT EASY, MEDIUM, HARD, TOTAL from LC_ACCOUNT where USERNAME='{username}'")
  except sqlite3.OperationalError:
    print(f"Error getting account with username {username}")
    return None

  return cursor
