from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import generics
from rest_framework.response import Response

from auth.serializers import LoginSerializer, InviteSerializer, SignupSerializer, UserSerializer

from cloud_check_file.core.views import BaseApiView
from auth.models import Invites
from files.models import File, Upload


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        object = serializer.save()
      
        if self.request.data.get('invite_id', None):
            Invites.objects.filter(id=self.request.data['invite_id']).update(user=object.id)
      
        return Response(data={'invite_id': object.id}, status=201)


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


class UsersView(BaseApiView):
    serializer_class = UserSerializer
    
    
    def get_queryset(self, *args, **kwargs):
        return self.serializer_class.get_model().objects.filter(id=self.request.user.id)


    def delete(self, request, *args, **kwargs):
        Upload.objects.filter(created_by=self.request.user.id).delete()
        File.objects.filter(created_by=self.request.user.id).delete()

        return super().destroy(request, *args, **kwargs)


class InvitesView(BaseApiView):
    serializer_class = InviteSerializer


    def create(self, request, *args, **kwargs):
        data = {
            'user': None, # Waiting for a user 
            'created_by': self.request.user
            }

        serializer = Invites.objects.create(**data)
       
        serializer.save()
      
        return Response(status=201)

    
    def delete(self, request, *args, **kwargs):
        invite = Invites.objects.filter(id=self.kwargs['pk']).first()
        if not invite: 
            return Response(status=404)
        if invite.created_by.id != self.request.user.id: 
            return Response(status=403)
        
        Upload.objects.filter(created_by=invite.user.id).delete()
        File.objects.filter(created_by=invite.user.id).delete()
        User.objects.filter(id=invite.user.id).delete()
        
        return super().destroy(request, *args, **kwargs)


class VerifyInvitesView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        invite = Invites.objects.filter(id=self.kwargs['pk'], user=None).first()

        if not invite: return Response(status=404)
        
        return Response(status=200)
