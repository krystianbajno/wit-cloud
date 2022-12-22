from http.server import BaseHTTPRequestHandler, HTTPServer
from uuid import uuid4
import urllib
from smb.SMBHandler import SMBHandler
import tempfile
import json

share = "nas"
user = "Administrator"
password = "testtest"
ip = "192.168.50.50"
server_name = "Win-testtest"

def write_random_smb():
      fileName = str(uuid4())
      fileContent = str(uuid4())

      f = tempfile.TemporaryFile(mode="w+")
      f.write(fileContent)

      client = urllib.request.build_opener(SMBHandler)
      connection_string = "smb://" + user + ":" + password + "@"+ ip + "/" + share + "/" + fileName

      with client.open(connection_string, data=f) as c:
        pass

      return {
        "fileName": fileName,
        "fileContent": fileContent
      }

class FileRandomSMBHandler(BaseHTTPRequestHandler):
  def __init__(self, req, client, addr):
    BaseHTTPRequestHandler.__init__(self, req, client, addr)

  def do_GET(self):
    data = write_random_smb()

    response = json.dumps(data)

    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", len(response))
    self.end_headers()
    self.wfile.write(response.encode(encoding='utf-8'))

def run(server_class=HTTPServer, handler_class=FileRandomSMBHandler):
    server_address = ('', 9999)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
  run()