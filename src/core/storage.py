from config import settings


class StorageService:
    bucket_name = settings.BUCKET_NAME

    @classmethod
    def store(cls, file_path: str) -> None:
        pass
