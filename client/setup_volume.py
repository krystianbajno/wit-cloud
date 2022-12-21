import subprocess
import os

def get_token(user, password):
  proc = subprocess.Popen(["python", "./master_key_client.py", "--user", user],
    stdout=subprocess.PIPE, stdin=subprocess.PIPE
  )

  proc.stdin.write((password + "\n").encode())
  proc.stdin.flush()

  token = proc.stdout.readlines()[-1]
  proc.stdout.flush()

  proc.wait()

  return token.decode().replace("\r\n", "")

def setup_crypt_volume(password, volume, letter):
  proc = subprocess.Popen(["veracrypt.exe", "/q", "/v", volume, "/p", password, "/l", letter, "/s", "/e"])
  proc.wait()

def setup_smb(name, path, permissions):
  proc = subprocess.Popen(["net", "share", f"{name}={path}", f"/GRANT:{permissions}"])
  proc.wait()


def main():
  print("[*] Running subprocess, fetching token")
  token = get_token(
    os.environ["USER"], 
    os.environ["TOKEN_PASSWORD"]
  )
  print(f"+ {token}")

  print("[*] Running subprocess, setting up volume")
  setup_crypt_volume(token, "r:\ENCRYPTED", "e",)

  print("[*] Setting up SMB share")
  setup_smb("Encrypted", "e:\\", "Everyone,FULL")

if __name__ == "__main__":
  main()