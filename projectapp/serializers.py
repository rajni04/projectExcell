from  . models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Max,Avg

class CandiadateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email']


class ScoreSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField('get_total')
    class Meta:
        model = Total_score
        fields = ['id', 'first_round', 'second_round','third_round','scoring','candidate','total']


    def validate(self,data): 
        fr=data.get('first_round')
        sr=data.get('second_round')
        tr=data.get('third_round')
        
        if fr >= 10 or fr >= 10 or tr >= 10 :
            raise serializers.ValidationError("No shoud be less than 10")
        return data

    def get_total(self,obj):
        return obj.first_round + obj.second_round + obj.third_round

    def create(self,validated_data):
        return Total_score.objects.create(**validated_data)



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

class ScoreListSerializer(serializers.ModelSerializer):
    maxscore = serializers.SerializerMethodField('get_maxscore')
    # avgscore = serializers.SerializerMethodField('get_avgscore')
    class Meta:
        model = Total_score
        fields = ['id', 'candidate','first_round','second_round','third_round','total','maxscore']
    def get_maxscore(self,obj):
        total_score=Total_score.objects.filter(candidate_id=obj.candidate)
        maxscore=total_score.aggregate(Avg('first_round' or 'second_round' or 'third_round'), Max('first_round' or 'second_round' or 'third_round'))
        return maxscore
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user','address']

