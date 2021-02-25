from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return self.name




