import os
import boto3

from datetime import datetime, timezone
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

BUCKET_NAME = os.environ["CERTIFICATE_BUCKET"]
TABLE_NAME = os.environ["CERTIFICATE_TABLE"]

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    record = event['Records'][0]['s3']
    object_key = record['object']['key']
    file_id = object_key.split("/")[1]

    now = datetime.now(timezone.utc).isoformat()

    try:
        # TODO: real PDF parsing logic here
        extracted_data = {
            "name": "John Doe",
            "course": "AWS Certified Developer",
            "issuer": "Amazon Web Services"
        }

        # Update DynamoDB on success
        table.update_item(
            Key={"certificateId": file_id},
            UpdateExpression="SET #status = :s, extracted = :e, processedAt = :p",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":s": "PROCESSED",
                ":e": extracted_data,
                ":p": now
            }
        )

        print(f"Certificate {file_id} processed successfully.")

    except Exception as e:
        print(f"Error processing certificate {file_id}:", e)
        # Update DynamoDB with failed status
        table.update_item(
            Key={"certificateId": file_id},
            UpdateExpression="SET #status = :s, errorMessage = :e, processedAt = :p",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":s": "FAILED",
                ":e": str(e),
                ":p": now
            }
        )
