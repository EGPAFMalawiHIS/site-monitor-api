

import random
from django.conf import settings
from djoser.serializers import (
        UserCreateSerializer as BaseUserRegistrationSerializer)
from django.db.models import Max
from rest_framework import serializers
# from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.validators import UniqueTogetherValidator
from .emr_services import *
from .helper_services import *
from .models import *
from .view_services import *

# # CREATE SERIALIZERS HERE ##


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'phone')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'],
                    phone=validated_data['phone'])  # added phone field.
        user.set_password(validated_data['password'])
        user.save()
        # Adding generated verification code to verification table
        Email.send_email(
                self,
                Email.verificationMail(self, validated_data['email'], 'code'))
        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                    email=validated_data['email'],
                    phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        code = VerificationCode.generate(self)
        # Adding generated verification code to verification table
        verify = VerificationCodes.objects.create(
                    code=code, value=code,
                    verification_type=validated_data['verification_type'])
        verify.save()
        verify.user.add(user)
        verify.save()
        code = verify.code
        return user


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                    username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        Email.send_email(
            self,
            Email.verificationMail(self, validated_data['email'], 'code'))
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        code = VerificationCode.generate(self)
        expiration_time = VerificationExpiration.expiration_time(self)
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email'],
                    phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save(verification_code=code)
        user.save(expiration_time=expiration_time)
        user.save()

        if validated_data['verification_type'] == 1:
            Email.send_email(
                self,
                Email.verificationMail(self, validated_data['email'], code))
        elif validated_data['verification_type'] == 2:
            text = SMS.verificationText(self, validated_data['phone'], code)
            SMS.send_text(self, text)
        return user


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    district_id = DistrictSerializer(read_only=True)
    class Meta:
        model = Site
        fields = '__all__'

class SiteSaveSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Site
        fields = '__all__'

class MonitorSerializer(serializers.ModelSerializer):
#site = SiteSerializer(read_only=True) 

    site = SiteSerializer(read_only=True)
    
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorBSerializer(serializers.ModelSerializer):
#site = SiteSerializer(read_only=True) 

    sitecode = SiteSerializer(read_only=True)
    
    class Meta:
        model = Monitor
        fields = '__all__'

class MonitorCSerializer(serializers.Serializer):
    district = serializers.CharField(max_length=200)
    site = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)
    status = serializers.IntegerField()
    last_seen = serializers.CharField(max_length=200)
    longitude = serializers.CharField(max_length=200)
    latitude = serializers.CharField(max_length=200)

