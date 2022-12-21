import json
import os
import azure.functions as func
from azure.data.tables import TableServiceClient
import base64
import bcrypt
from datetime import timedelta, date
import hashlib
import random

def main(req: func.HttpRequest) -> func.HttpResponse:
    connection_string = os.environ["baycode7storage7account_STORAGE"]
    service = TableServiceClient.from_connection_string(conn_str=connection_string)

    body = req.get_body()
    body = body.decode("utf-8")
    body = json.loads(body)

    entity = service.get_table_client("users").get_entity("user", body["user"])

    if not entity:
        return func.HttpResponse(
            '{"error": "Invalid user"}',
             status_code=401
        )

    entity_password = base64.b64decode(entity["password"])
    if not bcrypt.hashpw(body["password"].encode(), entity_password) == entity_password:
        return func.HttpResponse(
             '{"error": "Enter password"}',
             status_code=400
        )

    s = hashlib.sha256(str(random.random()).encode()).hexdigest()
    service.get_table_client("sessions").create_entity({
        "PartitionKey": "session",
        "RowKey": s,
        "expires": (date.today() + timedelta(days=2)).strftime('%Y/%m/%d')
    })
    
    response = {
        "token": s
    }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200
    )
