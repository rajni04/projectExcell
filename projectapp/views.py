from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from . import serializers
from rest_framework import generics
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView,
    UpdateAPIView,
)
from projectapp.serializers import CandiadateSerializer,ScoreSerializer,RegisterUserSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from django.contrib.auth import login as loginn
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.utils.decorators import method_decorator


class CandidateCreate(CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = CandiadateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Successfully Created  Canduadate'}, status=status.HTTP_201_CREATED,)

    def perform_create(self, serializer):
        serializer.save()

@method_decorator(csrf_exempt, name='dispatch')
class ScoreCreate(CreateAPIView):

    def post(self, request,*args, **kwargs):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors,status=400) 

   

@csrf_exempt
@api_view(['GET','POST'])                                                                 #functionbased
def user_list(request):
    if request.method=='GET':
        user_info=User.objects.all()
        print("11",user_info)
        serializer=RegisterUserSerializer(user_info,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data)
        serializer=RegisterUserSerializer(data=request.data)
        print('69',serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors,status=400) 

# class RegisterView(APIView):
#     serializer_class=RegisterUserSerializer
#     def post(self, request,*args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,{'message': 'Successfully Inserted Address'}, status=status.HTTP_201_CREATED)
        
    
    
    
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response({'message': 'Successfully Created  Canduadate'}, status=status.HTTP_201_CREATED,)

    # def perform_create(self, serializer):
    #     serializer.save()
# class LoginAPI(APIView):
#     def post(self, request):
#         serializer = LoginUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         loginn(request,user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token':token.key,
#         'username':user.username,
#         'id':user.pk
#          },status=200 )


class LoginAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.username
        })


class UserList(ListAPIView):
    
    serializer_class = RegisterUserSerializer
    def get_queryset(self):
        return User.objects.all()


class ProfileCreate(GenericAPIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,{'message': 'Successfully Inserted Address'}, status=status.HTTP_200_OK)
        return Response(serializer.error,{'message': 'NOT Successfully Inserted Address'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

class ProfileAPIView(RetrieveAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

class UserProfileUpdate(UpdateAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()
