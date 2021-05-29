from django.db import models
from django.contrib.auth.models import  User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from django.conf import settings
# Create your models here.


class Candidate(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=80)

    def __str__(self):
        return  {self.name} - {self.email}



class Total_score(models.Model):
    first_round=models.IntegerField(blank=True,null=False)
    second_round=models.IntegerField(blank=True,null=False)
    third_round=models.IntegerField(blank=True,null=False)  
    #cal_score=models.IntegerField()
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)   


    def total_score(self):
        total = self.first_round + self.second_round + self.third_round
        return total
    calc_score = models.PositiveIntegerField(total_score) 

    def __str__(self):
        return f"Score {self.first_round} - {self.second_round} - {self.third_round}"


    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, blank=True)

# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance, address="")
