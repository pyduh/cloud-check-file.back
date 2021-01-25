from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from files.models import Upload, File

from cloud_check_file.core.serializers import BaseSerializer
from pprint import pprint


class UploadSerializer(BaseSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class FileSerializer(BaseSerializer):
    class Meta:
        model = File
        fields = '__all__'

    upload_object = serializers.SerializerMethodField()

    def get_upload_object(self, obj):
        return UploadSerializer(obj.upload).data


class CheckSerializer(BaseSerializer):
    class Meta:
        model = File
        fields = '__all__'
