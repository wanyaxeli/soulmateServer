from rest_framework import serializers
from django.conf import settings
from .models import User,Interests,Profile,ProfileImages,Likes,Messages
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
user=settings.AUTH_USER_MODEL
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
    def validate_password(self,value):
        if value is not None:
            return make_password(value) 
        else :
            return serializers.ValidationError('password is null') 


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        # ...

        return token
class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interests
        fields='__all__'
        extra_kwargs = {'user': {'required': False}} 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'          

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Messages
#         fields='__all__'          