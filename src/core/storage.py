import boto3

from config import settings
from logger import get_logger

logger = get_logger(__name__)


class StorageService:
    bucket_name = settings.BUCKET_NAME

    client = boto3.client(
        "s3",
        aws_access_key_id=settings.ACCESS_KEY,
        aws_secret_access_key=settings.SECRET_KEY,
        region_name=settings.AWS_REGION,
    )

    @classmethod
    def store(cls, file_path: str) -> None:
        file_key = f"summaries/{file_path.split('/')[-1]}"
        logger.info(f"Uploading file {file_key} to bucket")

        cls.client.upload_file(file_path, settings.BUCKET_NAME, file_key)
        logger.info("File upload successfully")

        presigned_url = cls.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.BUCKET_NAME, "Key": file_key},
            ExpiresIn=3600,
        )
        logger.info(f"Generated presigned URL: {presigned_url}")
        return presigned_url
