import os
import json
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["CERTIFICATE_TABLE"]
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    certificate_id = event["pathParameters"]["certificateId"]

    response = table.get_item(
        Key={"certificateId": certificate_id}
    )

    item = response.get("Item")

    if not item:
        return _response(404, {"message": "Certificate not found"})

    return _response(200, {
        "certificateId": certificate_id,
        "status": item.get("status"),
        "extractedData": json.loads(item["extractedData"])
            if "extractedData" in item else None,
        "processedAt": item.get("processedAt"),
        "failureReason": item.get("failureReason")
    })


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }
