import requests
import argparse
import json

def main():
  parser = argparse.ArgumentParser(
    prog = 'Master Key Client',
    description = 'Fetch the Master Key',
    epilog = 'Confidential information'
  )

  parser.add_argument("--user",  required=False)
  args = parser.parse_args()
  user = args.user

  if not user:
    user = input("user > ")

  password = input("password > ")

  print(f"[*] authenticating {user}" )
  token = requests.post("https://baycodeazurefunctionapp.azurewebsites.net/api/log_in", json={
    "user": user,
    "password": password
  })
  token = json.loads(str(token.content.decode()))["token"]
  
  print("+ authenticated\ntoken: {token}".format(token=token))

  master_key = requests.get("https://baycodeazurefunctionapp.azurewebsites.net/api/get_master_key?token={token}"
    .format(token=token))

  master_key = json.loads(str(master_key.content.decode()))["master_key"]
  print("+ master_key:\n{master_key}".format(master_key=master_key))

if __name__ == "__main__":
  main()