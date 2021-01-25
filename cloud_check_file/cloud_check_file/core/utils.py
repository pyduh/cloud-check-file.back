import boto3
import hashlib

from django.conf import settings
from typing import Text


def get_new_s3_session():
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return session


def upload_to_s3(file, file_name=None, *args, **kwargs) -> Text:
    file_name = file_name if file_name else file.name

    s3 = get_new_s3_session().resource('s3')
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=file_name, Body=file)
    return file_name


def download_from_s3(file_path) -> Text:
    return get_new_s3_session().client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_path
        },
    )


def get_key_s3(user_id, file_name, *args, **kwargs):
    return f'{user_id}/{file_name}'


def get_file_hash(file, mode='md5', *args, **kwargs) -> Text:
    hash_function = hashlib.new(mode)
    hash_function.update(file.read())
    return hash_function.hexdigest()


def get_file_size(file, *args, **kwargs) -> Text:
    return f'{file.size}'