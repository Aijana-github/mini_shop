from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()


    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    types = (
        ('classic', 'classic'),
        ('sport', 'sport'),
        ('dm', 'demi-season'),
        ('winter', 'winter')

    )
    genders = (
        ('male', 'male'),
        ('female', 'female'),
        ('uni', 'uni'),
    )
    sizes = (
        ('child', 'child'),
        ('medium', 'medium'),
        ('large', 'large'),
        ('XL', 'XL'),
    )

    name = models.CharField(max_length=40)
    product_type = models.CharField(max_length=40, choices=types)
    gender = models.CharField(max_length=20, choices=genders)
    product_model = models.CharField(max_length=50)
    price = models.IntegerField()
    size = models.CharField(max_length=20, choices=sizes)
    manufacturer = models.CharField(max_length=15)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.product_model







