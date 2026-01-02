import boto3

textract = boto3.client("textract")

def extract_text(bucket: str, key: str) -> str:
    """
    Extracts all text from a PDF in S3 using Amazon Textract.

    Args:
        bucket: S3 bucket name
        key: S3 object key

    Returns:
        All extracted text as a single string.
    """

    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Name": key}}
    )

    lines = [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]

    return "\n".join(lines)
