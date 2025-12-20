import os
import json
import uuid
import base64

TMP_DIR = "/tmp"

# Lambda handler
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        file_base64 = body.get("fileBase64")
        file_name = body.get("fileName")

        if not file_base64 or not file_name:
            return _response(
                400,
                {"message": "Missing fileBase64 or fileName"}
            )

        # Decode PDF
        pdf_bytes = base64.b64decode(file_base64)

        # Write to /tmp
        file_id = str(uuid.uuid4())
        file_path = os.path.join(TMP_DIR, f"{file_id}-{file_name}")

        with open(file_path, "wb") as f:
            f.write(pdf_bytes)

        # Dummy extracted data (for now)
        extracted_data = {
            "name": "John Doe",
            "course": "AWS Certified Developer",
            "issuer": "Amazon Web Services"
        }

        return _response(
            200,
            {
                "uploaded": True,
                "fileName": file_name,
                "fileSizeBytes": len(pdf_bytes),
                "fileId": file_id,
                "extracted": extracted_data
            }
        )

    except Exception as e:
        print("Error:", str(e))
        return _response(
            500,
            {"message": "Failed to process PDF"}
        )

# Helper to format HTTP response
def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }
