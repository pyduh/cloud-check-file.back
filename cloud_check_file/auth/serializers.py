from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Invites
from cloud_check_file.core.models import as_json
from cloud_check_file.core.serializers import BaseSerializer


class LoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # Add custom claims
        invite = Invites.objects.filter(user=user).first()
        if invite:
            token['invite'] = True

        token['username'] = user.username
        token['id'] = user.id


        return token


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'invites')

    invites = serializers.SerializerMethodField()

    def get_invites(self, obj):
        return InviteSerializer(Invites.objects.filter(created_by=obj.id).all(), many=True, ).data
        #return [{**model_to_dict(object), 'email': object.user.username} for object in as_json(Invites.objects.filter(created_by=obj.id).all())]


class InviteSerializer(BaseSerializer):
    class Meta:
        model = Invites
        fields = '__all__'
        depth = 2
   
