import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

def get_dynamodb_client():
    try:
        return boto3.resource("dynamodb", region_name="sa-east-1", aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY"))
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(e)
        raise e