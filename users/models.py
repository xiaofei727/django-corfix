from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class CustomUser(AbstractUser):
    role = models.CharField(max_length=16)
    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        app_label = 'users'
        db_table = "users_user"

    def __str__(self):
        return "%s the user" % self.username
    

# class Employee(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)

    def __str__(self):
        return "%s the client" % self.user.username

    

