import copy

from django.contrib.auth.models import User
from django.db import transaction, models

from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import AllowAny

from files.serializers import UploadSerializer, FileSerializer
from files.models import Upload, File, Check

from cloud_check_file.core.views import BaseApiView
from cloud_check_file.core.utils import download, upload, get_file_name, get_file_hash, get_file_size, create_or_update_cache, get_cache
from cloud_check_file.core.models import as_json


class GenericUploadApiView(BaseApiView):
    parser_classes = [MultiPartParser]


class PublicUploadApiView(GenericUploadApiView):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        match = False
        hash = get_file_hash(self.request.data['file'])

        cache = get_cache(self.request.data['id'])

        if cache:
            match = cache['hash'] == hash   

        else:
            file = File.objects.filter(id=self.request.data['id']).first()

            if file:
                match = file.upload.hash == hash

        Check(file_id=self.request.data['id'], match=match, hash=hash).save()

        return Response(data={'hash': hash, 'file': self.request.data['id'], 'match': match}, status=200)


class UploadApiView(GenericUploadApiView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        file = self.request.data['file']

        data = {
            'size': get_file_size(self.request.data['file']),
            'hash': get_file_hash(copy.deepcopy(self.request.data['file'])),
            'url': upload(self.request.data['file'], get_file_name(self.request.user.id, file.name)),
            'created_by': self.request.user.id
            }

        serializer = UploadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        self._upload_id = serializer.save().id

        return Response(data={'upload': self._upload_id}, status=201)


class DownloadApiView(BaseApiView):

    def get(self, request, *args, **kwargs):
        upload = Upload.objects.filter(id=kwargs['pk']).first()

        return Response({ 'url': download(upload) }, status=200)


class FileApiSet(BaseApiView):
    serializer_class = FileSerializer


    def create(self, request, *args, **kwargs):
        data = {
            'upload': self.request.data.get('upload', None), 
            'name': self.request.data.get('name', None),
            'created_by': self.request.user.id
            }

        serializer = FileSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        object = serializer.save()

        create_or_update_cache(object.id, hash=object.upload.hash)
        
        return Response(data={'file_id': object.id}, status=201)


    def delete(self, request, *args, **kwargs):
        file = File.objects.filter(id=kwargs['pk'], created_by=self.request.user.id).first()
        file.upload.delete()
        file.delete()

        upload = Upload.objects.filter(id=kwargs['pk']).first()

        return Response(status=200)


class DashboardApiSet(BaseApiView):

    def get(self, request, *args, **kwargs):
        size = Upload.objects.filter(created_by=self.request.user.id).aggregate(models.Sum('size'))['size__sum']
        checks = Check.objects.filter(file_id__in=File.objects.filter(created_by=self.request.user.id)).all()

        data = {
            'results': {
                'files': File.objects.filter(created_by=self.request.user.id).count(),
                'last_checks': as_json(checks), 
                'size': size if size else 0,
                'checks': len(checks)
            }
        }
        
        return Response(data=data, status=201)

