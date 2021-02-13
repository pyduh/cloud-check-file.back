from django.db import models
from django.contrib.auth.models import User

from cloud_check_file.core.models import BaseModel, get_default_name_for_file


class Invites(BaseModel):
    user = models.ForeignKey(User, null=True, related_name='user_invited', on_delete=models.CASCADE)


class Phones(BaseModel):
    value = models.TextField(null=False)