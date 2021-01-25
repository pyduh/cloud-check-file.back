from django.db import models

from cloud_check_file.core.models import BaseModel, get_default_name_for_file


class Upload(BaseModel):
    url = models.TextField(default=None)
    hash = models.TextField(default=None)
    size = models.FloatField(default=0)


class File(BaseModel):
    name = models.CharField(max_length=255, default=get_default_name_for_file)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)


class Check(models.Model):
    file_id = models.IntegerField()
    match = models.BooleanField()
    hash = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

