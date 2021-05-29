from django.contrib import admin
from django.urls import path
from projectapp.views import *
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
   
    path('candidate/', CandidateCreate.as_view(), name="candidate"),
    path('register/',user_list , name="register"),
    path('score/', ScoreCreate.as_view(), name="score"),
    path('scorelist/', ScoreList.as_view(), name="score"),
    #path('register/', RegisterView, name='auth_register'),
    path('registerlist/', UserList.as_view(), name='registerlist'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('profile/', ProfileCreate.as_view(), name='profile'),
    path('profileretrive/<int:pk>/', ProfileAPIView.as_view(), name='profileretrive'),
    path('profileupdate/<int:pk>', UserProfileUpdate.as_view(), name='profileupdate' ),



    
]