import boto3
import json

bedrock = boto3.client("bedrock-runtime")

MODEL_ID = "amazon.titan-text-express-v1"

def structure_certificate_text(raw_text: str) -> dict:
    """
    Calls LLM to structure raw text into JSON with keys:
    documentType, issuer, issuedDate, confidenceScore
    """

    print("Calling LLM to structure certificate data")

    prompt = f"""
        You extract structured data from certificates.

        Rules:
        - Do NOT guess or infer missing values
        - If a field is not clearly present, return null
        - Return ONLY valid JSON (no explanations)

        Extract the following fields:
        - documentType: always "CERTIFICATE"
        - issuer: organization or authority issuing the certificate
        - recipientName: full name of the person the certificate is issued to
        - issuedDate: date of issue in YYYY-MM-DD format if present
        - confidenceScore: number from 0 to 100 indicating confidence in extraction

        Certificate text:
        {raw_text}
        """

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 500,
            "temperature": 0,
            "topP": 1
        }
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    output_text = response_body["results"][0]["outputText"]

    print("LLM raw output:", output_text)

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {
            "error": "INVALID_JSON_FROM_LLM",
            "rawOutput": output_text
        }
