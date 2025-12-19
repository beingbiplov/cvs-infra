import json

def handler(event, context):
   # return dummy data for now.
    return {
        "statusCode": 200,
        "body": json.dumps({
            "student_name": "John Doe",
            "course_name": "Cloud Computing",
            "issue_date": "2025-01-01",
            "institution": "Demo University"
        })
    }
