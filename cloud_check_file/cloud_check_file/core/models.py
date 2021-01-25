from django.contrib.auth.models import User
from django.db import models


def get_default_name_for_file():
    return 'File'


def as_json(data):
    return [{field.attname: getattr(object, field.attname) for field in object._meta.fields} for object in data]


class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    @classmethod
    def from_request(cls, request, *args, **kwargs):
        return cls(created_by=request.user.id, *args, **kwargs)
    

