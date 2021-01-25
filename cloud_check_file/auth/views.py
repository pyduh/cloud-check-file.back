from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import generics
from rest_framework.response import Response

from auth.serializers import LoginSerializer, SignupSerializer, UserSerializer

from cloud_check_file.core.views import BaseApiView
from files.models import File, Upload


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer


class UsersView(BaseApiView):
    serializer_class = UserSerializer
    
    def get_queryset(self, *args, **kwargs):
        return self.serializer_class.get_model().objects.filter(id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        Upload.objects.filter(created_by=self.request.user.id).delete()
        File.objects.filter(created_by=self.request.user.id).delete()

        return super().destroy(request, *args, **kwargs)
        

class PasswordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        user = User.objects.filter(id=self.request.user.id).first()

        if not user.check_password(request.data['password']):
            return Response(status=403)
        
        user.set_password(request.data['new_password'])
        user.save()

        return Response(status=200)