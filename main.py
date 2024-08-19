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

  json_data = json.loads(res.text)

  return json_data


def compare_stats_and_send_email(prevAcc: Account, currAcc: Account):
  email_address = os.environ.get("EMAIL_ADDRESS")
  email_password = os.environ.get("EMAIL_PASSWORD")
  email_recipient = os.environ.get("EMAIL_TARGET")

  print(email_address, email_password, email_recipient)

  # Create the email
  msg = EmailMessage()
  msg["Subject"] = f"{currAcc.username}'s leetcode progress for yesterday"
  msg["From"] = email_address
  msg["To"] = email_recipient

  easyDone = currAcc.easy - prevAcc.easy
  mediumDone = currAcc.medium - prevAcc.medium
  hardDone = currAcc.hard - prevAcc.hard

  msg.set_content(f"Progress!!!\nEasy Done = {easyDone}\nMedium Done = {mediumDone}\nHard Done = {hardDone}")

  # Send email
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_address, email_password)
    smtp.send_message(msg)

  print("Email sent")


def main():
  username = os.environ.get("USERNAME")
  data = get_info(username)["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]

  easyCount = data[1]["count"]
  mediumCount = data[2]["count"]
  hardCount = data[3]["count"]

  currAcc = Account(username, easyCount, mediumCount, hardCount)

  prevAcc = database.get_account(username)

  if prevAcc:
    compare_stats_and_send_email(prevAcc, currAcc)
    database.update_account(currAcc)
  else:
    database.insert_account(currAcc)


if __name__ == "__main__":
  main()
