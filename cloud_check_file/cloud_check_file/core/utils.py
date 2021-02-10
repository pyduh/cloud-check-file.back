import boto3
import hashlib
import six
import os

from datetime import datetime
from django.conf import settings
from google.cloud import datastore, storage as google_cloud_storage
from typing import Text


def upload(file, file_name=None, *args, **kwargs) -> Text:
    if settings.CLOUD_PROVIDER == "GOOGLE":
        return _upload_to_cloud_storage(file, file_name=file_name, *args, **kwargs)
    if settings.CLOUD_PROVIDER == "AWS":
        return _upload_to_s3(file, file_name=file_name, *args, **kwargs)

    raise NotImplementedError("Verify the Cloud Provider")


def download(upload, *args, **kwargs) -> Text:
    if settings.CLOUD_PROVIDER == "GOOGLE":
        return _generate_cloud_storage_presigned_url(upload.url)
    if settings.CLOUD_PROVIDER == "AWS":
        return _generate_s3_presigned_url(upload.url)

    raise NotImplementedError("Verify the Cloud Provider")


def get_file_name(user_id, file_name) -> Text:
    return f'{user_id}/{file_name}'


def get_new_s3_session():
    session = boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return session


def create_or_update_cache(file):
    datastore_client = datastore.Client.from_service_account_json(settings.GOOGLE_AUTH)
    # The kind for the new entity
    kind = "cloud-check-file-cache"

    entity = datastore.Entity(key=datastore_client.key(kind, file.id))
    entity["hash"] = "Buy milk"

    datastore_client.put(entity)


def get_cache(file):
    datastore_client = datastore.Client.from_service_account_json(settings.GOOGLE_AUTH)

    # TODO get the file on google datastore


def _upload_to_s3(file, file_name=None, *args, **kwargs) -> Text:
    file_name = file_name if file_name else file.name

    s3 = get_new_s3_session().resource('s3')
    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=file_name, Body=file)
    return file_name


def _upload_to_cloud_storage(file, file_name=None, *args, **kwargs) -> Text:
    client = google_cloud_storage.Client.from_service_account_json(settings.GOOGLE_AUTH)
    bucket = client.bucket(settings.GOOGLE_STORAGE_BUCKET)
    blob = bucket.blob(file_name)

    blob.upload_from_file(
        file,
        content_type=file.content_type
    )
    
    blob.make_private()

    return file_name

    url = blob.p

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url


def _generate_s3_presigned_url(file_path) -> Text:
    return get_new_s3_session().client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Key': file_path
        },
    )


def _generate_cloud_storage_presigned_url(file_path) -> Text:
    client = google_cloud_storage.Client.from_service_account_json(settings.GOOGLE_AUTH)
    bucket = client.bucket(settings.GOOGLE_STORAGE_BUCKET)
    blob = bucket.blob(file_path)

    return blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
    )


def get_file_hash(file, mode='md5', *args, **kwargs) -> Text:
    hash_function = hashlib.new(mode)
    hash_function.update(file.read())
    return hash_function.hexdigest()


def get_file_size(file, *args, **kwargs) -> Text:
    return f'{file.size}'


def _check_extension(filename, allowed_extensions):
    file, ext = os.path.splitext(filename)
    if (ext.replace('.', '') not in allowed_extensions):
        raise BadRequest(
            '{0} has an invalid name or extension'.format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing
    objects in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    basename, extension = filename.rsplit('.', 1)
    return "{0}-{1}.{2}".format(basename, date, extension)