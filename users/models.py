from django.db import models
from django.utils import timezone
import datetime
# Create your models here.
class Client(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField('created_at', default=datetime.datetime.now())
    def __str__(self):
        return self.username
