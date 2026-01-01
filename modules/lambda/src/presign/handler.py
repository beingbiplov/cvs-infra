import os
import json
import uuid
import boto3

from datetime import datetime, timezone
from botocore.exceptions import ClientError

# Clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Environment variables
TABLE_NAME = os.environ["CERTIFICATE_TABLE"]
BUCKET_NAME = os.environ["CERTIFICATE_BUCKET"]

# Presigned URL expiry
UPLOAD_EXPIRY_SECONDS = 300  # 5 minutes

table = dynamodb.Table(TABLE_NAME)

""" 
Lambda handler to create a presigned URL for uploading a certificate PDF.
Expects a JSON body with "fileName" and optional "contentType".
Records the upload request in DynamoDB with status "PENDING_UPLOAD".
"""
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        file_name = body.get("fileName")
        content_type = body.get("contentType", "application/pdf")

        if not file_name:
            return _response(400, {"message": "Missing fileName"})

        # Basic validation (pre-upload)
        if not file_name.lower().endswith(".pdf"):
            return _response(400, {"message": "Only PDF files are supported"})

        if content_type != "application/pdf":
            return _response(400, {"message": "Invalid content type"})

        # Generate unique ID and S3 key
        file_id = str(uuid.uuid4())
        object_key = f"uploads/{file_id}/{file_name}"

        # Record in DynamoDB as PENDING_UPLOAD
        now = datetime.now(timezone.utc).isoformat()
        table.put_item(
            Item={
                "certificateId": file_id,
                "fileName": file_name,
                "s3Key": object_key,
                "status": "PENDING_UPLOAD",
                "createdAt": now,
            }
        )

        # Generate presigned URL
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": "application/pdf",
            },
            ExpiresIn=UPLOAD_EXPIRY_SECONDS,
        )

        return _response(
            200,
            {
                "upload": {
                    "fileId": file_id,
                    "fileName": file_name,
                    "bucket": BUCKET_NAME,
                    "objectKey": object_key,
                    "expiresInSeconds": UPLOAD_EXPIRY_SECONDS,
                    "uploadUrl": presigned_url,
                },
                "next": "Upload the file using the presigned URL"
            }
        )

    except ClientError as e:
        print("AWS ClientError:", e)
        return _response(500, {"message": "AWS service error"})
    except Exception as e:
        print("Error:", e)
        return _response(500, {"message": "Failed to create upload URL"})

# Helper to format HTTP response
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps(body)
    }
