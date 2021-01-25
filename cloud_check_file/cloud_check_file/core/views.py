from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response

from cloud_check_file.core.models import BaseModel


class BaseAuth(
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    UpdateAPIView):
    permission_classes = (IsAuthenticated,)


class BaseApiView(BaseAuth):
   
    def get_queryset(self, *args, **kwargs):
        if not self.kwargs.get('created_by', None):
            self.kwargs['created_by'] = self.request.user.id
        return self.serializer_class.get_model().objects.filter(**self.kwargs)

