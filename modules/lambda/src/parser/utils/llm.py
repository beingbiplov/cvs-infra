import boto3
import json

bedrock = boto3.client("bedrock-runtime")

MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

def structure_certificate_text(raw_text: str) -> dict:
    """
    Calls LLM to structure raw text into JSON with keys:
    documentType, issuer, issuedDate, confidenceScore
    """

    print("Calling LLM to structure certificate data")

    prompt = f"""
        You are a system that extracts structured data from certificates.

        Extract the following fields and return ONLY valid JSON:
        - documentType
        - issuer
        - issuedDate (YYYY-MM-DD if possible)
        - confidenceScore (0-100)

        Certificate Text:
        {raw_text}
        """

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    output_text = response_body["content"][0]["text"]

    print("LLM raw output:", output_text)

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {
            "error": "INVALID_JSON_FROM_LLM",
            "rawOutput": output_text
        }
