from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Client(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField('created_at', default=timezone.now())
    def __str__(self):
        return self.username
    def set_password(self, password):
        self.password = make_password(password, None, 'md5')
        return self
    def check_password(self, password):
        valid = check_password(password, self.password)
        return valid

