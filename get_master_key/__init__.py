import json
import azure.functions as func
from azure.data.tables import TableServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    connection_string = os.environ["baycode7storage7account_STORAGE"]
    service = TableServiceClient.from_connection_string(conn_str=connection_string)

    token = req.params.get("token")
    session = service.get_table_client("sessions").get_entity("session", token)

    if not session:
        return func.HttpResponse(
            '{"error": "Invalid token"}',
             status_code=403
        )

    master_key = os.environ["MASTER_PASSWORD_FOR_ENCRYPTION"]
    response = {
        "master_key": master_key
    }

    return func.HttpResponse(
        json.dumps(response),
        status_code=200
    )
