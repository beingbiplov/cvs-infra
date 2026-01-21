import os
import json
import boto3
import base64
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["CERTIFICATE_TABLE"]
INDEX_NAME = os.environ.get("USER_INDEX_NAME", "userId-createdAt-index")

table = dynamodb.Table(TABLE_NAME)

def _get_user_id(event):
    headers = event.get("headers") or {}
    auth = headers.get("Authorization") or headers.get("authorization")
    if not auth:
        return None

    token = auth.split(" ")[-1]
    parts = token.split(".")
    if len(parts) < 2:
        return None

    payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("utf-8")))
        return payload.get("sub")
    except Exception:
        return None

def lambda_handler(event, context):
    user_id = _get_user_id(event)
    if not user_id:
        return _response(401, {"message": "Unauthorized"})

    try:
        resp = table.query(
            IndexName=INDEX_NAME,
            KeyConditionExpression=boto3.dynamodb.conditions.Key("userId").eq(user_id),
            ScanIndexForward=False,  # newest first
            Limit=100,
        )

        items = resp.get("Items", [])

        for it in items:
            if isinstance(it.get("extractedData"), str):
                try:
                    it["extractedData"] = json.loads(it["extractedData"])
                except Exception:
                    pass

        return _response(200, {"items": items})
    except Exception as e:
        print("List error:", str(e))
        return _response(500, {"message": "Internal error"})

def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(body, default=_json_default),
    }
    
def _json_default(o):
    if isinstance(o, Decimal):
        if o % 1 == 0:
            return int(o)
        return float(o)
    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")