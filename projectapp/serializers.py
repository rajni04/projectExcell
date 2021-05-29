from  . models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CandiadateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total_score
        fields = ['id', 'first_round', 'second_round','third_round','candidate']


class RegisterUserSerializer(serializers.ModelSerializer):
    #password2=serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = [ 'id', 'username', 'email','password' ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, args):
        email=args.get('email')
        username=args.get('username')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        #if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

        return super().validate(args)

    def create(self,validated_data):
        # user = models.User(
        #     username=validated_data['username'],
        #     email=validated_data['email']
        
        #  )
        # password=self.validated_data['password']
        # #password2=self.validated_data['password2']

        # # if password != password2:
        # #     raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # user.set_password(validated_data['password'])
        #user.save()
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user','address']

