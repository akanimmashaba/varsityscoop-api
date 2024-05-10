from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from .models import CustomUser,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = fields = ('email', "first_name","last_name",'password',)

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = []

class UserSerializer(DjoserUserSerializer):
    profile = ProfileSerializer()
    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + ('profile',)
