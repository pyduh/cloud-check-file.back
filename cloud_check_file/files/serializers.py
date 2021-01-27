from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from files.models import Upload, File, Check

from cloud_check_file.core.serializers import BaseSerializer
from cloud_check_file.core.models import as_json


class UploadSerializer(BaseSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class FileSerializer(BaseSerializer):
    class Meta:
        model = File
        fields = '__all__'

    upload_object = serializers.SerializerMethodField()
    checks = serializers.SerializerMethodField()

    def get_upload_object(self, obj):
        return UploadSerializer(obj.upload).data

    def get_checks(self, obj):
        checks = Check.objects.filter(file_id=obj.id).all()
        return as_json(checks)

class CheckSerializer(BaseSerializer):
    class Meta:
        model = Check
        fields = '__all__'
