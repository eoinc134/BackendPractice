# Load envitonment variables from .env file
import os
import io
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT_URL"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

def get_storage():
    return minio_client

# Upload a file and return the object key for PostGreSQL storage
def upload_file(file, bucket_name, object_name):
    # Check if the bucket exists, create it if it doesn't
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Upload the file to the specified bucket
    minio_client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=io.BytesIO(file.file),
        length=len(file.file)
    )

    return object_name
          