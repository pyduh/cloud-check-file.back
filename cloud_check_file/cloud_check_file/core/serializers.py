from django.db import models

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cloud_check_file.core.models import BaseModel


class BaseSerializer(serializers.ModelSerializer):
    @classmethod
    def get_meta(cls):
        return cls.Meta

    @classmethod
    def get_model(cls) -> models.Model:
        return cls.get_meta().model

    def is_valid(self, *args, **kwargs):
        if not super().is_valid(*args, **kwargs):
            raise ValidationError(self.errors)
        #print(vars(self))
        self.assert_integrity()
       
        return True

    def assert_integrity(self, *args, **kwargs):
        """
        Method to verify that fk in this transaction must to be to the same owner.
        """
        if not self.instance:
            return
        
        for column, value in self._validated_data.items():
            if isinstance(value, BaseModel) and value.created_by != self.instance.created_by:
                raise ValidationError({'upload': [f'Element {value.id} does not pertence to you']})
        