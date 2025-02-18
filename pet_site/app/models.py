from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Category(models.Model):
#     categories=models.TextField()

class PetType(models.Model):
    Pet_Type = models.TextField()    

class Pet(models.Model):
    Pet_Type=models.ForeignKey(PetType,on_delete=models.CASCADE)
    p_name=models.TextField()
    p_dis=models.TextField()
    breed=models.TextField()
    p_age=models.IntegerField()
    price=models.IntegerField()
    p_img=models.FileField() 
       




class Otp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.TextField() 