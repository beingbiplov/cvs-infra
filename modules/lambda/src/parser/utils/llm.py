import boto3
import json

bedrock = boto3.client("bedrock")

def structure_certificate_text(raw_text: str) -> dict:
    """
    Calls LLM to structure raw text into JSON with keys:
    documentType, issuer, issuedDate, confidenceScore
    """

    prompt = f"""
    Extract the following fields from the certificate text and return as JSON:
    - documentType
    - issuer
    - issuedDate (YYYY-MM-DD)
    - confidenceScore (0-100)

    Certificate Text:
    {raw_text}

    Output strictly as JSON.
    """

    response = bedrock.invoke_model(
        modelId="amazon.titan-text", 
        contentType="application/json",
        body=json.dumps({"prompt": prompt, "max_tokens": 500})
    )
    
    ## for debugging
    print("LLM response received", response)

    result = json.loads(response['body'].read())
    return result
