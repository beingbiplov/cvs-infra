import os
import boto3

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
PDF_MAGIC = b"%PDF-"

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["CERTIFICATE_TABLE"]
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    object_key = record["object"]["key"]

    print(f"Parser triggered for {bucket}/{object_key}")

    try:
        # uploads/{certificateId}/{fileName}
        parts = object_key.split("/")
        if len(parts) < 3:
            print("Invalid object key format")
            return

        certificate_id = parts[1]
        file_name = parts[-1]

        # fetch record
        item = table.get_item(
            Key={"certificateId": certificate_id}
        ).get("Item")

        if not item:
            print("No DynamoDB record found, skipping")
            return

        if item.get("status") in ("PROCESSING", "PROCESSED"):
            print("Already processed or processing, skipping")
            return

        # Mark PROCESSING
        table.update_item(
            Key={"certificateId": certificate_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "PROCESSING"},
        )

        # (size + metadata)
        head = s3.head_object(Bucket=bucket, Key=object_key)
        size = head["ContentLength"]

        if size > MAX_FILE_SIZE_BYTES:
            return _fail(certificate_id, "File exceeds 50MB limit")

        if not file_name.lower().endswith(".pdf"):
            return _fail(certificate_id, "Invalid file extension")

        # magic number check
        magic = s3.get_object(
            Bucket=bucket,
            Key=object_key,
            Range="bytes=0-4"
        )["Body"].read()

        if magic != PDF_MAGIC:
            return _fail(certificate_id, "Invalid PDF magic number")

        # Passed validation
        table.update_item(
            Key={"certificateId": certificate_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": "PROCESSED"},
        )

        print("PDF parsing successful")

    except Exception as e:
        print("Parser error:", str(e))
        _fail(certificate_id, "Unhandled parser error")


def _fail(certificate_id, reason):
    print("Validation failed:", reason)
    table.update_item(
        Key={"certificateId": certificate_id},
        UpdateExpression="SET #s = :s, failureReason = :r",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={
            ":s": "FAILED",
            ":r": reason
        },
    )
