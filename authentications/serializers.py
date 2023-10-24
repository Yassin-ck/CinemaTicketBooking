from rest_framework import serializers
from .models import (
    MyUser,
    UserProfile,
    Location,
    RequestLocation,  
    )
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .modules import google
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from authentications.modules.register import register_social_user

class PhoneSerilaizer(serializers.Serializer):
    phone = serializers.CharField()


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    


class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.userprofile.phone:
            token['phone'] = user.phone
        if user.username:
            token['username'] = user.username
        if user.email:
            token['email'] = user.email  
        if user.theatreowner.first() is not None:
            token['is_theatre'] = True         
        
        return token
    
  
 
class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    
    
    def validate_auth_token(self,auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data,'lkkkk')
        try:
            user_data['sub']
            print(user_data)
        except:
            raise serializers.ValidationError(
                'The token is expired or invalid. Please login again.'
            )
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        
        return register_social_user(
            user_id=user_id,email=email,name=name,
        )
  
  
  
  
   
        
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','username','email')


class UserProfileViewSerializer(GeoFeatureModelSerializer):
    user = MyUserSerializer()
    class Meta:
        model = UserProfile
        geo_field = 'location'
        fields = ('user_id','first_name','last_name','address','phone','user')
        
        
    def update(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.address = validated_data.get('address',instance.address)
        
        validated_user_data = validated_data.pop('user',None)       
        if validated_user_data:          
            instance.user.username = validated_user_data.get('username',instance.user.username)
            instance.user.email = validated_user_data.get('email',instance.user.email)
        return instance
        
  
  
class EmailAuthViewSerializer(serializers.Serializer):
    email = serializers.EmailField()
  
  
        
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('country','state','district','place')
        
     
class RequestedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLocation
        exclude = ('current_location','user')
        
    