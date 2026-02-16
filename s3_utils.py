import boto3
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv()


s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

def upload_pdf(file):
    file_key = f"resumes/{uuid4()}.pdf"

    s3.upload_fileobj(
        file,
        os.getenv("AWS_S3_BUCKET"),
        file_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )

    return f"https://{os.getenv('AWS_S3_BUCKET')}.s3.amazonaws.com/{file_key}"
