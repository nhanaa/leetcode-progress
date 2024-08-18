import requests
import json
from account import Account
import database
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

_ = load_dotenv()


url = "https://leetcode.com/graphql"

def get_query(username):
  query = f"""
  {{
    matchedUser(username: "{username}") {{
      username
      submitStats: submitStatsGlobal {{
        acSubmissionNum {{
          difficulty
          count
          submissions
        }}
      }}
    }}
  }}"""

  return query


def get_info(username):
  query = get_query(username)
  print(query)
  res = requests.post(url, json={"query": get_query(username)})
  print("Status Code " + str(res.status_code))

  json_data = json.loads(res.text)

  print(json_data)

  return json_data


def compare_stats_and_send_email(prevAcc: Account, currAcc: Account):
  email_address = os.environ.get("EMAIL_ADDRESS")
  email_password = os.environ.get("EMAIL_PASSWORD")
  email_recipent = os.environ.get("RECIPENT_EMAIL")

  # Create the email
  msg = EmailMessage()
  msg["Subject"] = "Progress for yesterday"
  msg["From"] = email_address
  msg["To"] = email_recipent

  easyDone = currAcc.easy - prevAcc.easy
  mediumDone = currAcc.medium - prevAcc.medium
  hardDone = currAcc.hard - prevAcc.hard

  msg.set_content(f"Progress!!!\nEasy Done = {easyDone}\nMedium Done = {mediumDone}\nHard Done = {hardDone}")

  # Send email
  # with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
  #   smtp.login(email_address, email_password)
  #   smtp.send_message(msg)

  print("Email sent")


def main():
  username = os.environ.get("USERNAME")
  data = get_info(username)["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
  print(data)

  easyCount = data[1]["count"]
  mediumCount = data[2]["count"]
  hardCount = data[3]["count"]

  currAcc = Account(username, easyCount, mediumCount, hardCount)

  print(easyCount, mediumCount, hardCount)

  dbConnection = database.connect_database("lc.db")

  database.create_table(dbConnection)

  cursor = database.get_account(dbConnection, username)

  # If account does not exist
  if not cursor:
    print("No such account in db")
    database.insert_account(dbConnection, currAcc)

  prevAcc = None
  for row in cursor:
    prevAcc = Account(username, row[0], row[1], row[2])

  compare_stats_and_send_email(prevAcc, currAcc)

if __name__ == "__main__":
  main()
