from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PetType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pet(models.Model):
    pet_name = models.CharField(max_length=100)
    pet_description = models.TextField()
    pet_age = models.IntegerField()
    pet_image = models.ImageField(upload_to='pet_images/')
    pet_price = models.IntegerField()
    pet_breed = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} ({self.pet_breed})"

   
from django.db import models

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    building_no = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)  
    mobile_no = models.CharField(max_length=15)  

    def __str__(self):
        return f"{self.name}, {self.building_no}, {self.street}, {self.state}, {self.district} - {self.pincode}"

       




class Otp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.TextField() 