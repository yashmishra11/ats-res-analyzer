import os
import boto3
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()


def get_config_val(key, default=None):
    """Retrieve configuration from Streamlit secrets if available, falling back to environment variables."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


def get_s3_client():
    """Create S3 client on-demand with config from secrets or environment."""
    region = get_config_val("AWS_REGION")
    access_key = get_config_val("AWS_ACCESS_KEY_ID")
    secret_key = get_config_val("AWS_SECRET_ACCESS_KEY")
    
    kwargs = {}
    if region:
        kwargs["region_name"] = region
    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key
        
    return boto3.client("s3", **kwargs)


def upload_pdf(file):
    bucket = get_config_val("AWS_S3_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_BUCKET is not configured in environment or Streamlit secrets.")

    file_key = f"resumes/{uuid4()}.pdf"
    s3_client = get_s3_client()

    s3_client.upload_fileobj(
        file,
        bucket,
        file_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )

    return f"https://{bucket}.s3.amazonaws.com/{file_key}"
