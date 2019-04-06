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
    company = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    address2 = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=200, default='')
    region = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=200, default='')
    postal_code = models.CharField(max_length=200, default='')
    main_phone = models.CharField(max_length=20, default='')
    main_phone_extension = models.CharField(max_length=10, default='')
    alt_phone = models.CharField(max_length=20, default='')
    alt_phone_extension = models.CharField(max_length=10, default='')
    fax = models.CharField(max_length=100, default='')
    business_email = models.CharField(max_length=200, default='')
    industry = models.CharField(max_length=200, default='')
    is_trial = models.BooleanField(default=False)

    def __str__(self):
        return "%s the client" % self.user.username

    



